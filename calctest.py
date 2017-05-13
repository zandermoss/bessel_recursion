#! /usr/bin/python
import numpy as np
import matplotlib.pyplot as plt

from Crawlers import Integrator

l=8
n=1

intg = Integrator()
vec_CalcK = np.vectorize(intg.IntegrateK)
vec_CalcH = np.vectorize(intg.IntegrateH)

x=np.linspace(0.0,100.0,10000)
yK = vec_CalcK(0,x,3.0,3.01,l,n)
yH = vec_CalcH(0,3.0*x,l,n)
yH/=(3.0)**(n+1)
plt.plot(x,yK,'b-')
plt.plot(x,yH,'-',color='orange')
plt.show()
