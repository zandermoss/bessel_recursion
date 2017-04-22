#! /usr/bin/python
import numpy as np
import matplotlib.pyplot as plt

from Crawlers import ICrawlerDict, HCrawlerDict, KCrawlerDict, XYCrawlerDict
from scipy.special import spherical_jn
from scipy import integrate

class Integrator(object):

	def FirstRoot(self,l):
		#Using a linear interpolation of j_l(x) roots for l between 0 and 100
		return 4.75 + 1.05*l
	
	def IInt(self,x,l,n):
	  return x**n*spherical_jn(l,x)

	def HInt(self,x,l,n):
	  return x**n*spherical_jn(l,x)**2

	def KInt(self,x,alpha,beta,l,n):
	  return x**n*spherical_jn(l,alpha*x)*spherical_jn(l,beta*x)
	
	def	__init__(self):

		#Instantiate a CrawlerDict of XYn. This will fill as Xn/Yn(x) are requested.
		#These calls are also idempotent, so no values are calculated twice.	
		self.XYcrawldict = XYCrawlerDict()

		self.Icd = ICrawlerDict(self.XYcrawldict)
		self.Hcd = HCrawlerDict(self.XYcrawldict)
		self.Kcd = KCrawlerDict(self.XYcrawldict)


	def IntegrateI(self,xlow,xhigh,l,n):
		xroot = self.FirstRoot(l)
	
		if (xlow < xroot) and (xhigh < xroot):
			val, err = integrate.quad(self.IInt, xlow, xhigh, args=(l,n))
		elif (xlow < xroot) and (xhigh > xroot):
			toroot, err = integrate.quad(self.IInt, xlow, xroot, args=(l,n))
			antiroot = self.Icd.GetEntry(xroot,(l,n))
			antihigh = self.Icd.GetEntry(xhigh,(l,n))
			fromroot = antihigh-antiroot
			val = toroot + fromroot
		elif (xlow > xroot) and (xhigh > xroot):
			antilow = self.Icd.GetEntry(xlow,(l,n))
			antihigh = self.Icd.GetEntry(xhigh,(l,n))
			val = antihigh-antilow
		else:
			print "Integral limits out of order!"
		return val

	def IntegrateH(self,xlow,xhigh,l,n):
		xroot = self.FirstRoot(l)
	
		if (xlow < xroot) and (xhigh < xroot):
			val, err = integrate.quad(self.HInt, xlow, xhigh, args=(l,n))
		elif (xlow < xroot) and (xhigh > xroot):
			toroot, err = integrate.quad(self.HInt, xlow, xroot, args=(l,n))
			antiroot = self.Hcd.GetEntry(xroot,(l,n))
			antihigh = self.Hcd.GetEntry(xhigh,(l,n))
			fromroot = antihigh-antiroot
			val = toroot + fromroot
		elif (xlow > xroot) and (xhigh > xroot):
			antilow = self.Hcd.GetEntry(xlow,(l,n))
			antihigh = self.Hcd.GetEntry(xhigh,(l,n))
			val = antihigh-antilow
		else:
			print "Integral limits out of order!"
		return val

	def IntegrateK(self,xlow,xhigh,alpha,beta,l,n):
		xroot = self.FirstRoot(l)/max([alpha,beta])
	
		if (xlow < xroot) and (xhigh < xroot):
			val, err = integrate.quad(self.KInt, xlow, xhigh, args=(alpha,beta,l,n))
		elif (xlow < xroot) and (xhigh > xroot):
			toroot, err = integrate.quad(self.KInt, xlow, xroot, args=(alpha,beta,l,n))
			antiroot = self.Kcd.GetEntry((xroot,alpha,beta),(l,n))
			antihigh = self.Kcd.GetEntry((xhigh,alpha,beta),(l,n))
			fromroot = antihigh-antiroot
			val = toroot + fromroot
		elif (xlow > xroot) and (xhigh > xroot):
			antilow = self.Kcd.GetEntry((xlow,alpha,beta),(l,n))
			antihigh = self.Kcd.GetEntry((xhigh,alpha,beta),(l,n))
			val = antihigh-antilow
		else:
			print "Integral limits out of order!"
		return val
