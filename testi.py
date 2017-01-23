#! /usr/bin/python
import numpy as np
from crawlers import ICrawlerArray
from crawlers import XYCrawlerArray

xlow=2
xhigh=4
l=4
n=3

#Generate a dictionary of XYn. This will fill as Xn/Yn(x) are requested.
#These calls are also idempotent, so no values are calculated twice.	
xyca = XYCrawlerArray()

#Generate a dictionary of Iln. 
ica = ICrawlerArray(xyca)

#Calculating at two x values and comparing the difference to a numerical
#integral in mathematica over the [xlow,xhigh] interval.
ylow = ica.GetEntry(xlow,(l,n))
yhigh = ica.GetEntry(xhigh,(l,n))

print "X in [{},{}]".format(xlow,xhigh)
print "l=",l
print "n=",n
print "Integral: ",yhigh-ylow
