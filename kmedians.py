#!/usr/bin/python3.4
# K-medians implementation
# (c) Mohammad H. Mofrad, 2017 
# (e) mohammad.hmofrad@pitt.edu

import numpy as np
from utils import *

# Read and store the input data
# using the utils.py
PERFIX = 'dataset/'
#FILE = PERFIX + 'balance-scale.data.txt'
#FILE = PERFIX + 'breast-cancer-wisconsin.data.txt'
#FILE = PERFIX + 'sonar.all-data.txt'
#FILE = PERFIX + 'cmc.data.txt'
#FILE = PERFIX + 'glass.data.txt'
#FILE = PERFIX + 'hayes-roth.data.txt'
#FILE = PERFIX + 'ionosphere.data.txt'
#FILE = PERFIX + 'iris.data.txt'
#FILE = PERFIX + 'pima-indians-diabetes.data.txt'
#FILE = PERFIX + 'wine.data.txt'
#FILE = PERFIX + 'drift.data.txt'
FILE = PERFIX + 'har.data.txt'

[x, y] = read(FILE)

# Initliaze parameters
[n, d] = np.shape(x)   # [#samples, #dimensions]
k = len(np.unique(y))  #  #clusters

mi = np.min(x, axis=0) # Minimum
ma = np.max(x, axis=0) # Maximum
di = ma - mi           # Difference
stop = 0               # Stopping criterion 

c = np.zeros(n)        # Cluster membership 
med = np.random.rand(k, d) * np.ones((k, d)) # Clusters median
med = med * di
med = med + mi
med_t = np.copy(med) # Copy of clusters median

imax = 100
for i in range(imax):
   med_t = np.copy(med)
  
   # Calculate minimum Euclidean distance and
   # update clusters membership
   for j in range(n):
      dist = np.sqrt(np.sum(np.power(x[j,:] - med, 2), axis=1))
      idx = np.argmin(dist)
      val = np.min(dist)
      c[j] = idx
   
   # Calculate cluster membership and
   # update clusters median
   for j in range(k):
      a = np.arange(n)
      idx = a[c == j] # Current cluster
      l = len(idx)    # #cluster elements
      if l:
         med[j,:] = np.median(x[idx,:], axis=0)
      else:
         med[j,:] = med[j,:] + (np.random.rand(d) * di)

   # Check against stopping criterion
   stop = np.sum(np.sum(np.power(med - med_t,2), axis=0))
   if(stop <= 0) or (i >= imax):
      break

# Calculate accuracy and
# Silhouette Coefficient
# using the utils.py
acc = accuracy(c, y, k)
sil = silhouette(x, c, med)
print(acc, sil)
