from abc import ABCMeta, abstractmethod

## An abstract base class for recursion tree crawlers.
# This class outlines the structure of derived crawler
# classes which compute various bessel integrals by
# recursive decompositions to base-case integrals with
# closed forms. The values of the integrals at the nodes
# of the recursion tree are stored in a dictionary, indexed
# by tuple keys.
# Such flexible storage of the recursion tree allows for 
# idempotent calculation of multiple integrals belonging
# to the same tree. That is to say, the crawler checks
# to see if a node dependency has been previously computed
# before recursing.
# Note: each crawler object allows computations of a tree of 
# integrals at *one* set of parameters. For example, if one
# wishes to compute Kln(x; alpha,beta) at multiple pairs (l,n) (indices) 
# for a single tuple (x; alpha,beta) (parameters), they need only one 
# crawler object. If one wishes to compute at multiple parameter tuples,
# they can use one of the CrawlerArray classes defined in each child Crawler
# source file. These store dictionaries of Crawler objects using parameter
# tuple keys. In this way, one can calculate over multiple parameter values
# without re-computing crawler trees from scratch. 

class Crawler(object):

	__metaclass__ = ABCMeta

	## The Constructor
	# The recursion tree dictionary is initialized,
	# and the integral parameters are stored as a member
	# variable.
	# @param _params a tuple of integral parameters.
	# For example, the integral Kln(x; alpha,beta) has an 
	# argument tuple (x,alpha,beta). The tuple (l,n) constitutes
	# the index of this integral node in the tree of Kln(x;alpha,beta)
	# at each (l,n).

	def __init__(self, _params):
		self.tree = dict()
		self.params = _params

	## The master crawler function.
	# This function specifies the logic of the recursion.
	# If the index tuple is found in the tree, that node
	# has already been calculated, and the function returns.
	# If not, it checks whether the integral is a base-case
	# (whether the node is a "leaf" on the tree). The base-case
	# conditions are specified by IsLeaf(index). If so, the leaf
	# integral is calculated by CalcLeaf(index). If the node is
	# not a leaf, then Branch(index) is called, which calls Crawl
	# to calculate the nodes on which this node depends. In this
	# case, CalcNode(index) is then called to compute the node 
	# integral using the specified recursion relation and the 
	# dependency nodes.
	# Importantly, none of these results are passed between functions.
	# All node integral values are read from and written to the self.tree
	# dictionary directly. Only the index tuples pass betwen these funcions.
	#
	# As an example, if we call Crawl((0,0)) for the first time
	# in the Kln crawler child class (KCrawler), IsLeaf((0,0)) will 
	# return True, and CalcLeaf((0,0)) will compute K00(x;alpha,beta), 
	# store that value in the (0,0) entry of self.tree, and Crawl will return.
	# If we call Crawl((1,1)) for the first time, IsLeaf(1,1) will return 
	# False, and Branch((1,1)) will call Crawl((0,-1)) and Crawl((0,1)).
	# These calls will evaluate those base cases and fill the corresponding
	# entries of self.tree. CalcNode((1,1)) will then be called, and it will
	# perform a linear combination of the (0,1) and (0,-1) entries of self.tree,
	# together with some closed form terms, to produce K11(x;alpha,beta). 
	# This value will then be stored in self.tree.
	# @param index a tuple indexing the node of the tree to be calculated.

	def Crawl(self,index):
		if index not in self.tree:
			if self.IsLeaf(index):
				self.CalcLeaf(index)
			else:
				self.Branch(index)
				self.CalcNode(index)

	## The external interface function used to calculate a node integral.
	# Internally, this begins the recursive sequence of calls to self.Crawl().
	# Once these calls have all finished, and self.tree has been populated 
	# with the desired node and all dependent nodes, GetEntry(index) returns
	# the (index) entry of self.tree
	# @param index a tuple indexing the node of the tree to be calculated.
	# @return the desired integral, an entry from the populated self.tree at (index)
	
	def GetEntry(self,index):
		self.Crawl(index)
		return self.tree[index]		

	## Determines whether the index tuple corresponds to a leaf of the recursion tree.
	# Abstract method: specified by child crawler classes.
	# @param index a tuple indexing the node of the tree to be checked for leaf conditions.

	@abstractmethod
	def IsLeaf(self,index):
		pass

	## Calculates the integral at a given leaf.
	# Abstract method: specified by child crawler classes.
	# The recursion of Crawl() terminates here, but this method may 
	#	call other recursive methods, as in the case of the K leaves 
	#	calling the GetEntry() method of the X crawler.
	# @param index a tuple indexing the leaf to be calculated.

	@abstractmethod
	def CalcLeaf(self,index):
		pass

	## Calls one or more Crawl() functions with suitably decremented (index) tuples.
	# Abstract method: specified by child crawler classes.
	#	The choice of which indices to call Crawl() with  determines the 
	#	structure of the recursion tree. For example, the X tree is 
	#	a simple chain, so its Branch() function makes a single call to Crawl()
	# with decremented index. The K tree, on the other hand is a binary tree.
	# Its Branch() function makes two calls to Crawl() with two differently 
	# decremented (index) tuples.
	# @param index is the index of the current node. This tuple is decremented for calls to subsequent Crawl() functions.

	@abstractmethod
	def Branch(self,index):
		pass
	
	## Calculates the integral at a given node.
	# Abstract method: specified by child crawler classes.
	# Combines the integrals at lower nodes using the child-specific
	# recursion relation to produce the desired integral at node (index).
	# This integral is stored in self.tree[index]. Because this funciton
	# is called after Branch(), its dependencies (lower node integrals)
	# have already been computed recursively and stored in self.tree.
	# @param index is the index at which to compute the node integral. 
	
	@abstractmethod
	def CalcNode(self,index):
		pass

## An abstract base class for crawler dictionary classes.
# This is essentially a dictionary of crawlers with an associated 
# idempotent calcuation funciton GetEntry(). The crawler objects are indexed
# by parameter tuple keys. One can compute integrals at one parameter 
# tuple for a few different indices, go and compute at other parameter tuples,
# and then return and continue computations at the original parameters without
# recreating the crawler tree from scratch.

class CrawlerDict(object):

	__metaclass__ = ABCMeta

	## The constructor.
	#  
	# Initializes the self.crawler_dict dictionary. If there are any 
	# dependent objects (like an XYCrawlerDict used to compute leaves
	# of KCrawler trees inside a KCrawlerDict child class), they are 
	# passed to the object or initialized here.

	@abstractmethod
	def __init__(self):
		pass

	## The idempotent crawler creation/calculation function.
	# Checks to see if self.crawler_dict has a crawler entry at
	# the (params) tuple. If so, calls the GetEntry(index) of that
	# crawler. If not, a crawler is insantiated with the (params) tuple,
	# and then its GetEntry(index) function is called. 
	# @param params is the parameter tuple of the requested integral.
	# @param index is the index tuple of the requested integral.
	# @return the requested integral.

	@abstractmethod
	def GetEntry(self,params,index):
		pass

