#!/usr/bin/python3.4
# Learning Automata Clusteing (LAC) parameter selection
# (c) Mohammad H. Mofrad, 2016
# (e) hasanzadeh@cs.pitt.edu

import numpy as np
from utils import *

# Read and store the input data
PERFIX = 'dataset/'
#FILE = 'iris.data.txt'
#FILE = 'glass.data.txt'
FILE = PERFIX + 'breast-cancer-wisconsin.data.txt'
# Read input file
# using the utils.py
[x, y] = read(FILE)

f=open('foo.csv','wb')

# Initliaze parameters
[n, d] = np.shape(x)
k = len(np.unique(y))

numactions = k
alpha = 0.9
beta = 0.01
acc = np.zeros(3)
A = np.concatenate((np.arange(0,0.1,0.01), np.arange(0.1,1,0.05), np.array([1])))
for alpha_ind in A:
   for beta_ind in A:
#      print(alpha_ind, beta_ind)
      alpha = alpha_ind
      beta = beta_ind
      for ii in range(3):

         action = np.zeros((k, n)) # LA action set
         probability = np.tile(1/numactions, (numactions, n)) # LA prob. set

         mi = np.min(x, axis=0) # Minimum
         ma = np.max(x, axis=0) # Maximum
         di = ma - mi           # Difference
         stop = 0               # Stopping criterion

         c = np.zeros(n)        # LA     cluster membership
         cc = np.zeros(n)       # kmeans cluster membership
         me = np.random.rand(k, d) * np.ones((k, d)) # Clusters mean
         me = me * di
         me = me + mi
         me_t = np.zeros(np.shape(me)) # Copy of clusters mean

         imax = 100
         for i in range(imax):
            # Select an action based on prob.
            # update clusters membership 
            action = actionselection(action, probability, numactions, n)
            signal   = np.ones(n)
            for j in range(k):
               a = np.arange(n)
               c[action[j,:] == 1] = j
   
            me_t = np.copy(me)
            # Calculate minimum Euclidean distance and
            # update kmeands clusters membership 
            for j in range(n):
               dist = np.sqrt(np.sum(np.power(x[j,:] - me,2), axis=1))
               idx = np.argmin(dist)
               val = np.min(dist)
               cc[j] = idx

            # Calculate kmeans cluster membership and
            # update kmeans clusters mean
            for j in range(k):
               a = np.arange(n)
               idx = a[c == j] # Current cluster
               l = len(idx)    # #cluster elements
               if l:
                  me[j,:] = np.sum(x[idx,:], axis=0)/len(x[idx,:])
               else:
                  me[j,:] = me[j,:] + (np.random.rand(d) * di)
   
            # Compute reinforcement signal   
            for j in range(n):
               if c[j] == cc[j]:
                  signal[j] = 0
            # Update probability vector
            probability = probabilityupdate(action, probability, numactions, n, signal, alpha, beta)

            # Check against stopping criterion
            stop = np.sum(np.sum(np.power(me - me_t,2), axis=0))
            if(stop <= 0) or (i >= imax):
               break

         # Calculate accuracy and
         # Silhouette Coefficient
         # using the utils.py
         acc[ii] = accuracy(c, y, k)
         #sil = silhouette(x, c, me)
#      print(alpha_ind, beta_ind, acc, sil)
      ac = np.mean(acc)
      foo = np.array([[alpha, beta, ac]])
      print(foo)
      np.savetxt(f, foo, fmt='%1.9f')
# delimiter=' '
f.close()
