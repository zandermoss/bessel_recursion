#! /usr/bin/python
import recursive_covariance as rc
import numpy as np

xlow=2.0
xhigh=4.0
alpha=2
beta=3
l=4
n=3

#Generate a dictionary of Xn. This will fill as Xn(x) are requested.
#These calls are also idempotent, so no values are calculated twice.	
xca = rc.XCrawlerArray()

#Generate a dictionary of Kln. This has the same dynamic and idempotent
#properties as the XCrawlerArray, but the indexing is more complicated
#because the Kln recursion tree is binary, and the Xn tree is unary.
kca = rc.KCrawlerArray(xca)

#Calculate Kln at a given x, alpha, beta, l, and n.
#The dictionary in KCrawlerArray, like the dictionary in XCrawlerArray,
#is a dictionary of KCrawler (resp. XCrawler) objects. The KCrawler 
#objects contain dictionaries which store trees in (l,n) indices, as
#well as methods to crawl down these trees and fill in the nodes without
#redundant calculation.

#Calculating at two x values and comparing the difference to a numerical
#integral in mathematica over the [xlow,xhigh] interval.

ylow = kca.GetEntry((xlow,alpha,beta),(l,n))
yhigh = kca.GetEntry((xhigh,alpha,beta),(l,n))
print "Integral: ",yhigh-ylow
