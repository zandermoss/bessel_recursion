#! /usr/bin/python

from abc import ABCMeta, abstractmethod

from numpy import sin,cos
from scipy.special import spherical_jn, sici

class KCrawlerArray(object):
	def __init__(self, _x_crawler_array):
		self.crawler_dict = dict()
		self.x_crawler_array = _x_crawler_array	

	def GetEntry(params,index):
		if params not in self.crawler_dict:
			crawler_dict[params] = KCrawler(params,self.x_crawler_array)
		return crawler_dict[params].GetEntry(index)

#-------------------------------------------------------------------------#

class XCrawlerArray(object):
	def __init__(self):
		self.crawler_dict = dict()

	def GetEntry(params,index):
		if params not in self.crawler_dict:
			crawler_dict[params] = XCrawler(params)
		return crawler_dict[params].GetEntry(index)

#-------------------------------------------------------------------------#

class Crawler(object):

	def __init__(self, _params):
		self.tree = dict()
		self.params = _params

	def Crawl(index):
		if index not in tree:
			if IsLeaf(index):
				CalcLeaf(index)
			else:
				Branch(index)
				CalcNode(index)

	def GetEntry(index):
		Crawl(index)
		return tree[index]		

	@abstractmethod
	def IsLeaf(index):
		''' Determines whether the index tuple corresponds to
				a leaf of the recursion tree. '''
		pass

	@abstractmethod
	def CalcLeaf(index)
		''' Calculates the value at a given leaf. The recursion of this
				tree terminates here, but this method may call other recursive
				methods, as in the case of the K leaves calling the GetEntry
				method of the X crawler. '''
		pass

	@abstractmethod
	def Branch(index):
		''' Recursively calls multiple crawlers. The choice of which
				indices to call determines the structure of the recursion
				tree. In this case, the X tree is a simple chain, and 
				the K tree is a binary tree. Stores the result in tree[index] '''
		pass
				
	@abstractmethod
	def CalcNode(index):
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
		self.x = params[0]
		self.alpha = params[1]
		self.beta = params[2]

		#Calculation specific coefficient computations and initializations.
		#Leaf coefficients
		self.D0 = sin((self.alpha-self.beta)*self.x)/(self.alpha-self.beta) - sin((self.alpha+self.beta)*self.x)/(self.alpha+self.beta)

		#Node coefficients
		self.C0 = 1.0/(2*self.alpha*self.beta)
		self.C1 = (self.alpha**2 + self.beta**2)
		self.C2 = dict()
		self.C3 = dict()

	#Idempotent calculation of node coefficients
	def GetC2(l):
		if l not in self.C2:
			self.C2[l] = spherical_jn(l-1,self.alpha*self.x)*spherical_jn(l-1,self.beta*self.x)
		return self.C2[l] 
	
	#Idempotent calculation of node coefficients
	def GetC3(l):
		if l not in self.C3:
			T1 = self.beta*spherical_jn(l-1,self.alpha*self.x)*spherical_jn(l,self.beta*self.x)
			T2 = self.alpha*spherical_jn(l-1,self.beta*self.x)*spherical_jn(l,self.alpha*self.x)
			self.C3[l] = T1+T2	
		return self.C3[l] 

	def IsLeaf(index):
		if index[0]==0:
			return True
		else:
			return False

	def CalcLeaf(index):
		n=index[1]
		x_sum = x_crawler_array.GetEntry((self.alpha+self.beta)*self.x, n-3)
		x_diff = x_crawler_array.GetEntry((self.alpha-self.beta)*self.x, n-3)
		val = (self.x**(n-2)/2.0)*self.D0
		val += (-1.0)*((n-2.0)/2.0)*(1.0/(self.alpha-self.beta)^(n-1))*x_diff
		val += ((n-2.0)/2.0)*(1.0/(self.alpha+self.beta)^(n-1))*x_sum
		self.tree[index] = val
		
	def Branch(index):
		Crawl((index[0]-1,index[1]))
		Crawl((index[0]-1,index[1]-2))

	def CalcNode(index):
		l = index[0]
		n = index[1]
		val = self.C1*self.tree[(l-1,n)]
		val += (n-2.0)*(n+2.0*l-3.0)*self.tree[(l-1,n-2)]
		val += (2.0-n)*self.x**(n-1)*GetC2(l)
		val += (-1.0)*self.x**n*GetC3(l)
		self.tree[index] = self.C0*val

#-------------------------------------------------------------------------#

class XCrawler(Crawler):
	def __init__(self,_params):
		super(XCrawler,self).__init__(_params)
		
		#Parse params tuple
		self.x = self.params[0]

		#Calculation specific coefficient computations and initializations.
		self.si, self.ci = sici(self.x)
		self.sinx = sin(self.x)
		self.cosx = cos(self.x)

	def IsLeaf(index):
		if index[0] in (-2,-1,0,1):
			return True
		else:
			return False

	def CalcLeaf(index):
		m = index[0]
		if m==-2:
			val = self.ci - (self.sinx)/self.x
		elif m==-1:
			val = self.si
		elif m==0:
			val = (-1.0)*self.cosx
		elif m==1:
			val = self.sinx - (self.x)*(self.cosx)
		self.tree[index] = val

	def Branch(index):
		m = index[0]
		if m<0:
			Crawl((m+2))
		else:
			Crawl((m-2))

	def CalcNode(index):
		m = index[0]
		if m<0:
			val = (m+2)*(self.x)**(m+1)*(self.sinx)
			val += (-1.0)*(self.x)**(m+2)*(self.cosx)
			val += (-1.0)*(self.tree[(m+2)])
			val *= 1.0/((m+2.0)*(m+1.0))
		else:
			val = m*(self.x)**(m-1)*(self.sinx)
			val += (-1.0)*(self.x)**m*(self.cosx)
			val += (-1.0)*m*(m-1)*(self.tree[(m-2)])
		return val

