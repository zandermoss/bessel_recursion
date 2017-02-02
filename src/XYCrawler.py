from numpy import sin,cos
from scipy.special import spherical_jn, sici

from Crawler import Crawler, CrawlerDict

class XYCrawler(Crawler):
	def __init__(self,_params):
		super(XYCrawler,self).__init__(_params)

		#Params is not a tuple in this case, just a real number
		self.x = self.params

		#Calculation specific coefficient computations and initializations.
		self.si, self.ci = sici(self.x)
		self.sinx = sin(self.x)
		self.cosx = cos(self.x)

	def IsLeaf(self,index):
		m=index[0]
		if m in (-1,0):
			return True
		else:
			return False

	def CalcLeaf(self,index):
		m = index[0]
		XY_type = index[1]
		if XY_type == "X":
			if m==-1:
				val = self.si
			else:
				val = (-1.0)*self.cosx
		else:
			if m==-1:
				val = self.ci
			else:
				val = self.sinx
		self.tree[index] = val

	def Branch(self,index):
		m = index[0]
		XY_type = index[1]
		if XY_type == "X":
			if m<0:
				self.Crawl((m+1,"Y"))
			else:
				self.Crawl((m-1,"Y"))
		else:
			if m<0:
				self.Crawl((m+1,"X"))
			else:
				self.Crawl((m-1,"X"))

	def CalcNode(self,index):
		m = index[0]
		XY_type = index[1]
		if XY_type == "X":
			if m<0:
				val = (1.0/(m+1))*((self.x)**(m+1)*self.sinx - self.tree[(m+1,"Y")])
			else:
				val = m*self.tree[(m-1,"Y")] - (self.x)**m*self.cosx
		else:
			if m<0:
				val = (1.0/(m+1))*((self.x)**(m+1)*self.cosx + self.tree[(m+1,"X")])
			else:
				val = (self.x)**m*self.sinx - m*self.tree[(m-1,"X")]
		self.tree[index] = val


class XYCrawlerDict(CrawlerDict):
	def __init__(self):
		self.crawler_dict = dict()

	def GetEntry(self,params,index):
		if params not in self.crawler_dict:
			self.crawler_dict[params] = XYCrawler(params)
		return self.crawler_dict[params].GetEntry(index)
