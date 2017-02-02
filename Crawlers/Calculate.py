#! /usr/bin/python
import numpy as np
from Crawlers import ICrawlerDict
from Crawlers import XYCrawlerDict
from scipy.special import spherical_jn
from scipy import integrate

xlow=2
xhigh=4
l=4
n=3


def AboveFirstRoot(x,l):
	#Using a linear interpolation of j_l(x) roots for l between 0 and 100
	#to determine whether the j_l(x) argument lies above the first root.
	if (x > (4.75 + 1.05*l)):
		return True
	else:
		return False

def IInt(x,l,n):
  return x**n*spherical_jn(l,x)

#Generate a dictionary of XYn. This will fill as Xn/Yn(x) are requested.
#These calls are also idempotent, so no values are calculated twice.	
xyca = XYCrawlerDict()

#Generate a dictionary of Iln. 
ca = ICrawlerDict(xyca)

ylow = ca.GetEntry(xlow,(l,n))
yhigh = ca.GetEntry(xhigh,(l,n))

if (AboveFirstRoot(x,l)==True):
	#Calculating at two x values and comparing the difference to a numerical
	#integral in mathematica over the [xlow,xhigh] interval.
	val = yhigh-ylow
	print "ABOVE"
else:
	val, err = integrate.quad(IInt, xlow, xhigh, args=(l,n))
	print "BELOW"

print "Testing I Integration"
print "X in [{},{}]".format(xlow,xhigh)
print "l=",l
print "n=",n
print "Recursive Integral: ",yhigh-ylow
print "Switched Integral: ",val
