from scipy.special import spherical_jn
from Crawler import Crawler
from XYCrawler import XYCrawler, XYCrawlerArray

class ICrawler(Crawler):

	def __init__(self,_params,_xy_crawler_array):
		super(ICrawler,self).__init__(_params)
		self.xy_crawler_array = _xy_crawler_array	

		#Parse params tuple
		self.x = self.params

		#Node coefficients
		self.C = dict()


	#Idempotent calculation of node coefficients
	def GetC(self,l):
		if l not in self.C:
			self.C[l] = spherical_jn(l-1,self.x)		
		return self.C[l]

	def IsLeaf(self,index):
		if index[0]==0:
			return True
		else:
			return False

	def CalcLeaf(self,index):
		n=index[1]
		self.tree[index] = self.xy_crawler_array.GetEntry(self.x, (n-1,"X"))

	def Branch(self,index):
		self.Crawl((index[0]-1,index[1]-1))

	def CalcNode(self,index):
		l = index[0]
		n = index[1]
		val = (l+n-1.0)*self.tree[(l-1,n-1)] - (self.x)**n*(self.GetC(l))
		self.tree[index] = val

class ICrawlerArray(object):
	def __init__(self, _xy_crawler_array):
		self.crawler_dict = dict()
		self.xy_crawler_array = _xy_crawler_array	

	def GetEntry(self,params,index):
		if params not in self.crawler_dict:
			self.crawler_dict[params] = ICrawler(params,self.xy_crawler_array)
		return self.crawler_dict[params].GetEntry(index)
