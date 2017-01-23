from scipy.special import spherical_jn, sici
from math import log
from Crawler import Crawler
from XYCrawler import XYCrawler, XYCrawlerArray

class HCrawler(Crawler):

	def __init__(self,_params,_xy_crawler_array):
		super(HCrawler,self).__init__(_params)
		self.xy_crawler_array = _xy_crawler_array	

		#Parse params tuple
		self.x = self.params

		#Node coefficients
		self.si2x, self.ci2x = sici(2.0*self.x)
		self.logx = log(self.x)
		self.J = dict()


	#Idempotent calculation of node coefficients
	def GetJ(self,l):
		if l not in self.J:
			self.J[l] = spherical_jn(l,self.x)		
		return self.J[l]

	def IsLeaf(self,index):
		if index[0]==0:
			return True
		else:
			return False

	def CalcLeaf(self,index):
		n=index[1]
		if n==1:
			val = 0.5*(self.logx - self.ci2x) 
		else:
			y2x = self.xy_crawler_array.GetEntry(2.0*self.x, (n-2,"Y"))
			val = (self.x**(n-1))/(2.0*(n-1.0)) - (1.0/(2.0**n))*y2x
		self.tree[index] = val

	def Branch(self,index):
		l=index[0]
		n=index[1]
		self.Crawl((l-1,n))
		self.Crawl((l-1,n-2))

	def CalcNode(self,index):
		l = index[0]
		n = index[1]
		val = self.tree[(l-1,n)]
		val += 0.5*(n-2)*(2*l+n-3)*self.tree[(l-1,n-2)]
		val += (1.0-n/2.0)*(self.x**(n-1.0))*self.GetJ(l-1)**2
		val -= (self.x**n)*self.GetJ(l-1)*self.GetJ(l)
		self.tree[index] = val

class HCrawlerArray(object):
	def __init__(self, _xy_crawler_array):
		self.crawler_dict = dict()
		self.xy_crawler_array = _xy_crawler_array	

	def GetEntry(self,params,index):
		if params not in self.crawler_dict:
			self.crawler_dict[params] = HCrawler(params,self.xy_crawler_array)
		return self.crawler_dict[params].GetEntry(index)
