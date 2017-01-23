from abc import ABCMeta, abstractmethod

class Crawler(object):

	__metaclass__ = ABCMeta

	def __init__(self, _params):
		self.tree = dict()
		self.params = _params

	def Crawl(self,index):
		if index not in self.tree:
			if self.IsLeaf(index):
				self.CalcLeaf(index)
			else:
				self.Branch(index)
				self.CalcNode(index)

	def GetEntry(self,index):
		self.Crawl(index)
		return self.tree[index]		

	@abstractmethod
	def IsLeaf(self,index):
		''' Determines whether the index tuple corresponds to
				a leaf of the recursion tree. '''
		pass

	@abstractmethod
	def CalcLeaf(self,index):
		''' Calculates the value at a given leaf. The recursion of this
				tree terminates here, but this method may call other recursive
				methods, as in the case of the K leaves calling the GetEntry
				method of the X crawler. '''
		pass

	@abstractmethod
	def Branch(self,index):
		''' Recursively calls multiple crawlers. The choice of which
				indices to call determines the structure of the recursion
				tree. In this case, the X tree is a simple chain, and 
				the K tree is a binary tree. Stores the result in tree[index] '''
		pass
				
	@abstractmethod
	def CalcNode(self,index):
		''' Calculates the value at a given node using the values of 
				lower nodes. This dependence is specified in the Branch()
				method. Stores the result in tree[index]. '''
		pass
	
