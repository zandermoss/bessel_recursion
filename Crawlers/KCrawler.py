from numpy import sin,cos
from scipy.special import spherical_jn, sici
from Crawler import Crawler, CrawlerDict
from XYCrawler import XYCrawler, XYCrawlerDict

class KCrawler(Crawler):

	def __init__(self,_params,_xy_crawler_dict):
		super(KCrawler,self).__init__(_params)
		self.xy_crawler_dict = _xy_crawler_dict	

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
		self.C4 = dict()

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

	#Idempotent calculation of node coefficients
	def GetC4(self,l):
		if l not in self.C4:
			T1 = self.beta*spherical_jn(l,self.alpha*self.x)*spherical_jn(l-1,self.beta*self.x)
			T2 = self.alpha*spherical_jn(l-1,self.alpha*self.x)*spherical_jn(l,self.beta*self.x)
			self.C4[l] = T1-T2	
		return self.C4[l] 

	def IsLeaf(self,index):
		l=index[0]
		n=index[1]

		if n==2:
			return True
		if l==0:
			return True
		else:
			return False

	def CalcLeaf(self,index):
		l=index[0]
		n=index[1]

		if n==2:
			val = (self.x**2/(self.alpha**2 - self.beta**2))*self.GetC4(l)
		else:
			y_sum = self.xy_crawler_dict.GetEntry((self.alpha+self.beta)*self.x, (n-2,"Y"))
			y_diff = self.xy_crawler_dict.GetEntry((self.alpha-self.beta)*self.x, (n-2,"Y"))
			val = (1.0/(self.alpha-self.beta)**(n-1))*y_diff
			val -= (1.0/(self.alpha+self.beta)**(n-1))*y_sum
			val *= (1.0/(2*self.alpha*self.beta))		

		self.tree[index] = val		

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


class KCrawlerDict(CrawlerDict):
	def __init__(self, _xy_crawler_dict):
		self.crawler_dict = dict()
		self.xy_crawler_dict = _xy_crawler_dict	

	def GetEntry(self,params,index):
		if params not in self.crawler_dict:
			self.crawler_dict[params] = KCrawler(params,self.xy_crawler_dict)
		return self.crawler_dict[params].GetEntry(index)

