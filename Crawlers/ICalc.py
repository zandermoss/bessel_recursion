#! /usr/bin/python
import numpy as np
from Crawlers import XYCrawlerDict
from Crawlers import ICrawlerDict
from scipy.special import spherical_jn
from scipy import integrate

class ICalc(object):

	def __init__(self):
		self.xyca = XYCrawlerDict()
		self.ica = ICrawlerDict(self.xyca)

	def IInt(self,x,l,n,alpha):
		return x**n*spherical_jn(l,x*alpha)

	def DetZero(self,x):
		epsilon = 1e-12 #FIXME
		if abs(x-0.0) < epsilon:
			return True	
		else:
			return False

	def IZero(self,x,l,n):
 	 if l!=0:
 		 return 0.0
 	 else:
 		 return (1.0/(n+1))*x**(n+1)

	def FirstRoot(self,l):
		#Using a linear interpolation of j_l(x) roots for l between 0 and 100
		return (4.75+1.05*l)

	def AboveFirstRoot(self,x,l):
		#Determine whether the j_l(x) argument lies above the first root.
		if (x > self.FirstRoot(l)):
			return True
		else:
			return False
	
	def AnalyticCalculate(self,kpair,l,n,alpha):
		intvals=[0.0,0.0]
		for j in range(2):
			intvals[j]= (1.0/alpha)**(n+1.0)*self.ica.GetEntry((alpha*kpair[j]),(l,n))
		delta = intvals[1] - intvals[0]
		return delta

	def Calculate(self,kpair,l,n,alpha):

		azero=self.DetZero(alpha)
		if azero:
			intvals=[0.0,0.0]
		 	for j in range(2):
				intvals[j] = self.IZero(kpair[j],n)
			delta = intvals[1] - intvals[0]
		else:

			FR = self.FirstRoot(l)	
			AFR1 = self.AboveFirstRoot(alpha*kpair[0],l)
			AFR2 = self.AboveFirstRoot(alpha*kpair[1],l)

			if (not AFR1) and (not AFR2):
 			 	delta, err = integrate.quad(self.IInt, kpair[0], kpair[1], args=(l,n,alpha))
			elif (not AFR1) and AFR2:
				kroot = FR/alpha
				toroot, err = integrate.quad(self.IInt, kpair[0], kroot, args=(l,n,alpha))		
				fromroot = self.AnalyticCalculate([kroot,kpair[1]], l,n,alpha)
				delta = toroot+fromroot
			else:
				delta = self.AnalyticCalculate(kpair,l,n,alpha)	

		"""
		delcheck, err = integrate.quad(self.IInt, kpair[0], kpair[1], args=(l,n,alpha))
		if abs(delcheck-delta)>1e-6:
			print "BAD INTEGRATION, ICALC"
			print "Numerics: ",delcheck
			print "Analytics: ",delta
			print "---------Parameters---------"
			print "K:(",kpair[0],",",kpair[1],")"
			print "l=",l," n=",n," alpha=",alpha
			print "----------------------------"
			print
		"""

		return delta



