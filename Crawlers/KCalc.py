#! /usr/bin/python
import numpy as np
from Crawlers import XYCrawlerDict
from Crawlers import KCrawlerDict
from Crawlers import ICalc
from scipy.special import spherical_jn
from scipy import integrate

from timeit import default_timer as timer


class KCalc(object):

	def __init__(self):
		self.xyca = XYCrawlerDict()
		self.kca = KCrawlerDict(self.xyca)
		self.icalc = ICalc.ICalc()

	def KInt(self,x,l,n,alpha,beta):
		return x**n*spherical_jn(l,x*alpha)*spherical_jn(l,x*beta)

	def DetZero(self,x):
		epsilon = 1e-12 #FIXME
		if abs(x-0.0) < epsilon:
			return True	
		else:
			return False

	def K2Zero(self,x,l,n):
 	 if l!=0:
 		 return 0.0
 	 else:
 		 return (1.0/(n+1))*x**(n+1)

	def K1Zero(self,kpair,l,n,coeff):
 	 if l!=0:
 		 return 0.0
 	 else:
 		 return self.icalc.Calculate(kpair,l,n,coeff)



	def FirstRoot(self,l):
		#Using a linear interpolation of j_l(x) roots for l between 0 and 100
		return (4.75+1.05*l)

	def AboveFirstRoot(self,x,l):
		#Determine whether the j_l(x) argument lies above the first root.
		if (x > self.FirstRoot(l)):
			return True
		else:
			return False

	def AnalyticCalculate(self,kpair,l,n,alpha,beta):
		intvals=[0.0,0.0]
		for j in range(2):
			intvals[j]= self.kca.GetEntry((kpair[j],alpha,beta),(l,n))
		delta = intvals[1] - intvals[0]
		return delta

	def Calculate(self,kpair,l,n,alpha,beta):
		azero=self.DetZero(alpha)
		bzero=self.DetZero(beta)

		if azero and bzero:
			intvals=[0.0,0.0]
			for j in range(2):
				intvals[j] = self.K2Zero(kpair[j],n)
			delta = intvals[1] - intvals[0]
		elif azero and (not bzero):
			delta = self.K1Zero(kpair,l,n,beta)
		elif (not azero) and bzero:
			delta = self.K1Zero(kpair,l,n,alpha)
		else:
			FR = self.FirstRoot(l)

			AFR1 = self.AboveFirstRoot(kpair[0],l)
			AFR2 = self.AboveFirstRoot(kpair[1],l)
		

			if (not AFR1) and (not AFR2):
				delta, err = integrate.quad(self.KInt, kpair[0], kpair[1], args=(l,n,alpha,beta))
			elif (not AFR1) and AFR2:
				toroot, err = integrate.quad(self.KInt, kpair[0], FR, args=(l,n,alpha,beta))	
				fromroot = self.AnalyticCalculate([FR,kpair[1]], l,n,alpha,beta)
				delta = toroot+fromroot
			else:
				delta = self.AnalyticCalculate(kpair,l,n,alpha,beta)

		"""
		delcheck, err = integrate.quad(self.KInt, kpair[0], kpair[1], args=(l,n,alpha,beta))
		end=timer()
		numtime= end-start
		start=timer()
		ana_delta = self.AnalyticCalculate(kpair,l,n,alpha,beta)
		end=timer()
		anatime = end-start
		if abs(delcheck-delta)>1e-6:
			print "BAD INTEGRATION, KCALC"
			print	"Mode: "+mode 
			print "AFR1",AFR1
			print "AFR2",AFR2
			print "FirstRoot: k=",FR
			print "Result: ",delta
			print "Time: ", hybtime
			print "Numerics: ",delcheck
			print "Numeric Time: ", numtime
			print "Pure Analytics: ",ana_delta
			print "Analytic Time: ",anatime
			print "---------Parameters---------"
			print "K:(",kpair[0],",",kpair[1],")"
			print "l=",l," n=",n," alpha=",alpha," beta=",beta
			print "----------------------------"
			print 
		"""

		return delta
