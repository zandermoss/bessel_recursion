#! /usr/bin/python
import numpy as np
from Crawlers import KCrawlerDict
from Crawlers import XYCrawlerDict
from scipy.special import spherical_jn
from scipy import integrate

xlow=0.0001
xhigh=4
l=4
n=3
alpha=2.0
beta=1.0

def KInt(x,alpha,beta,l,n):
  return x**n*spherical_jn(l,alpha*x)*spherical_jn(l,beta*x)

print "START NUMINT"
val, err = integrate.quad(KInt, xlow, xhigh, args=(alpha,beta,l,n))
print "END NUMINT"

#Generate a dictionary of XYn. This will fill as Xn/Yn(x) are requested.
#These calls are also idempotent, so no values are calculated twice.	
xyca = XYCrawlerDict()

#Generate a dictionary of Kln. 
ca = KCrawlerDict(xyca)

#Calculating at two x values and comparing the difference to a numerical
#integral in mathematica over the [xlow,xhigh] interval.
print "START ANINT"
ylow = ca.GetEntry((xlow,alpha,beta),(l,n))
yhigh = ca.GetEntry((xhigh,alpha,beta),(l,n))
print "END ANINT"

print "Testing K Integration"
print "X in [{},{}]".format(xlow,xhigh)
print "l=",l
print "n=",n
print "Recursive Integral: ",yhigh-ylow
print "Numerical Integral: ",val," +/- ",err
