#! /usr/bin/python

from abc import ABCMeta, abstractmethod

from numpy import sin,cos
from scipy.special import spherical_jn, sici


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
	
#-------------------------------------------------------------------------#

class KCrawler(Crawler):

	def __init__(self,_params,_x_crawler_array):
		super(KCrawler,self).__init__(_params)
		self.x_crawler_array = _x_crawler_array	

		#Parse params tuple
		self.x = self.params[0]
		self.alpha = self.params[1]
		self.beta = self.params[2]

		#Calculation specific coefficient computations and initializations.
		#Leaf coefficients
		self.D0 = sin((self.alpha-self.beta)*self.x)/(self.alpha-self.beta) - sin((self.alpha+self.beta)*self.x)/(self.alpha+self.beta)

		#Node coefficients
		self.C0 = 1.0/(2*self.alpha*self.beta)
		self.C1 = (self.alpha**2 + self.beta**2)
		self.C2 = dict()
		self.C3 = dict()

	#Idempotent calculation of node coefficients
	def GetC2(self,l):
		if l not in self.C2:
			self.C2[l] = spherical_jn(l-1,self.alpha*self.x)*spherical_jn(l-1,self.beta*self.x)
		return self.C2[l] 
	
	#Idempotent calculation of node coefficients
	def GetC3(self,l):
		if l not in self.C3:
			T1 = self.beta*spherical_jn(l-1,self.alpha*self.x)*spherical_jn(l,self.beta*self.x)
			T2 = self.alpha*spherical_jn(l-1,self.beta*self.x)*spherical_jn(l,self.alpha*self.x)
			self.C3[l] = T1+T2	
		return self.C3[l] 

	def IsLeaf(self,index):
		if index[0]==0:
			return True
		else:
			return False

	def CalcLeaf(self,index):
		n=index[1]
		x_sum = self.x_crawler_array.GetEntry((self.alpha+self.beta)*self.x, n-3)
		x_diff = self.x_crawler_array.GetEntry((self.alpha-self.beta)*self.x, n-3)
		val = ((self.x**(n-2))/2.0)*self.D0
		val += (-1.0)*((n-2.0)/2.0)*(1.0/((self.alpha-self.beta)**(n-1)))*x_diff
		val += ((n-2.0)/2.0)*(1.0/((self.alpha+self.beta)**(n-1)))*x_sum
		self.tree[index] = val/(self.alpha*self.beta)
		
	def Branch(self,index):
		self.Crawl((index[0]-1,index[1]))
		self.Crawl((index[0]-1,index[1]-2))

	def CalcNode(self,index):
		l = index[0]
		n = index[1]
		val = self.C1*self.tree[(l-1,n)]
		val += (n-2.0)*(n+2.0*l-3.0)*self.tree[(l-1,n-2)]
		val += (2.0-n)*self.x**(n-1)*self.GetC2(l)
		val += (-1.0)*self.x**n*self.GetC3(l)
		self.tree[index] = self.C0*val

#-------------------------------------------------------------------------#

class XCrawler(Crawler):
	def __init__(self,_params):
		super(XCrawler,self).__init__(_params)

		#Params is not a tuple in this case, just a real number
		self.x = self.params

		#Calculation specific coefficient computations and initializations.
		self.si, self.ci = sici(self.x)
		self.sinx = sin(self.x)
		self.cosx = cos(self.x)

	def IsLeaf(self,index):
		if index in (-2,-1,0,1):
			return True
		else:
			return False

	def CalcLeaf(self,index):
		m = index
		if m==-2:
			val = self.ci - (self.sinx)/self.x
		elif m==-1:
			val = self.si
		elif m==0:
			val = (-1.0)*self.cosx
		elif m==1:
			val = self.sinx - (self.x)*(self.cosx)
		self.tree[index] = val

	def Branch(self,index):
		m = index
		if m<0:
			self.Crawl((m+2))
		else:
			self.Crawl((m-2))

	def CalcNode(self,index):
		m = index
		if m<0:
			val = (m+2)*(self.x)**(m+1)*(self.sinx)
			val += (-1.0)*(self.x)**(m+2)*(self.cosx)
			val += (-1.0)*(self.tree[(m+2)])
			val *= 1.0/((m+2.0)*(m+1.0))
		else:
			val = m*(self.x)**(m-1)*(self.sinx)
			val += (-1.0)*(self.x)**m*(self.cosx)
			val += (-1.0)*m*(m-1)*(self.tree[(m-2)])
		self.tree[index] = val

#-------------------------------------------------------------------------#

class KCrawlerArray(object):
	def __init__(self, _x_crawler_array):
		self.crawler_dict = dict()
		self.x_crawler_array = _x_crawler_array	

	def GetEntry(self,params,index):
		if params not in self.crawler_dict:
			self.crawler_dict[params] = KCrawler(params,self.x_crawler_array)
		return self.crawler_dict[params].GetEntry(index)

#-------------------------------------------------------------------------#

class XCrawlerArray(object):
	def __init__(self):
		self.crawler_dict = dict()

	def GetEntry(self,params,index):
		if params not in self.crawler_dict:
			self.crawler_dict[params] = XCrawler(params)
		return self.crawler_dict[params].GetEntry(index)

#-------------------------------------------------------------------------#
