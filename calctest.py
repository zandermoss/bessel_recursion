#! /usr/bin/python
import numpy as np
import matplotlib.pyplot as plt

from Crawlers import ICrawlerDict
from Crawlers import XYCrawlerDict
from scipy.special import spherical_jn
from scipy import integrate

xlow=0
xhigh=1000
l=8
n=3


def FirstRoot(l):
	#Using a linear interpolation of j_l(x) roots for l between 0 and 100
	return 4.75 + 1.05*l

def IInt(x,l,n):
  return x**n*spherical_jn(l,x)

#Generate a dictionary of XYn. This will fill as Xn/Yn(x) are requested.
#These calls are also idempotent, so no values are calculated twice.	
xyca = XYCrawlerDict()

#Generate a dictionary of Iln. 
ca = ICrawlerDict(xyca)


def Calc(xlow,xhigh,l,n):
	print "XLO: ",xlow, "  XHI: ",xhigh
	xroot = FirstRoot(l)
	print xroot
	if (xlow < xroot) and (xhigh < xroot):
		val, err = integrate.quad(IInt, xlow, xhigh, args=(l,n))
	elif (xlow < xroot) and (xhigh > xroot):
		toroot, err = integrate.quad(IInt, xlow, xroot, args=(l,n))
		antiroot = ca.GetEntry(xroot,(l,n))
		antihigh = ca.GetEntry(xhigh,(l,n))
		fromroot = antihigh-antiroot
		val = toroot + fromroot
	elif (xlow > xroot) and (xhigh > xroot):
		antilow = ca.GetEntry(xlow,(l,n))
		antihigh = ca.GetEntry(xhigh,(l,n))
		val = antihigh-antilow
	else:
		print "Integral limits out of order!"
	return val
"""	
	print "Testing I Integration"
	print "X in [{},{}]".format(xlow,xhigh)
	print "l=",l
	print "n=",n
	#print "Recursive Integral: ",yhigh-ylow
	print "Switched Integral: ",val
"""

vec_Calc = np.vectorize(Calc)

x=np.linspace(0.0,30.0,10000)
y = vec_Calc(x,30.0,l,n)
plt.plot(x,y)
plt.show()
