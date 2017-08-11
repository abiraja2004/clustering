#!/usr/bin/python3.4
# Utility functions
# (c) Mohammad H. Mofrad, 2017
# (e) hasanzadeh@cs.pitt.edu

import numpy as np
import os

# Debug level
VERBOSE = False

# Read input text file and
# create x matrix as the input data and
# create y column vector as data labels
def read(FILE):
   if os.path.isfile(FILE):
      file = open(FILE, 'r')
      lines = tuple(file)
      file.close()
      data = []
      for line in lines:
         data.append(line.rstrip().split(","))
         if VERBOSE:
            print(data[-1])
   else:
      print(FILE, 'does not exist')
      exit(0)

   data = np.array(data)
   x = data[:,0:-1]
   x = x.astype(np.float)

   y = np.zeros(len(data))
   uniq = np.unique(data[:,-1])
   for i in range(0,len(uniq)):
      idx = (data[:,-1] == uniq[i])
      if any(idx):
         y[idx] = i

   return(x, y)

# Calculate the accuracy of centroid-based clusting algorithms
def accuracy(c, y, k):
   if VERBOSE:
      print(c)
      print(y)

   n = len(y)
   kk = np.zeros(k)
   o = 0
   e = 0
   idxx = []
   for i in range(k):
      a = np.arange(n)
      idxa = a[y == i]
      for j in range(len(idxa)):
         kk[int(c[j+o])] = kk[int(c[j+o])] + 1
      if idxx:
          for l in idxx:
             kk[l] = 0
      o = o + len(idxa)
      idx = np.argmax(kk)
      idxx.append(idx)
      val = kk[idx]
      e = e + (val/len(y[y == i]))
      kk = np.zeros(k)
   e = e/k
   return(e)

# Calculate the accuracy of density-based clusting algorithms
# @param  c: Cluster asignment 
# @param  y: Data labels
# @param k1: True number of clusters
# @param k2: Estimated number of clusters
def accuracy_(c, y, k1, k2):
   if VERBOSE:
      print(c)
      print(y)

   n = len(y)
   kk = np.zeros(k2)
   o = 0
   e = 0
   idxx = []
   for i in range(k1):
      a = np.arange(n)
      idxa = a[y == i]
      for j in range(len(idxa)):
         kk[int(c[j+o])] = kk[int(c[j+o])] + 1
      if idxx:
          for l in idxx:
             kk[l] = 0
      o = o + len(idxa)
      idx = np.argmax(kk)
      idxx.append(idx)	  
      val = kk[idx]	  
      e = e + (val/len(y[y == i]))
      kk = np.zeros(k2)
   e = e/k1
   return(e)   
   
# Silhouette Coefficient
def silhouette(x, c, me):
   if VERBOSE:
      print(c)
      print(y)
   
   n = len(c)
   s = np.zeros((n,3))
   for i in range(n):
      dist = np.sqrt(np.sum(np.power(x[i,:] - me,2), axis=1))
      dd = np.argsort(dist)
      aa = np.arange(n)
      for j in range(2):
         aa = np.arange(n)
         idx = aa[c == dd[j]]
         l = len(idx)
         if l:
            for o in idx:
               s[o,j] = s[o,j] + np.sqrt(np.sum(np.power(x[i,:] - x[o,:] ,2)))
            s[o,j] = s[o,j]/l
   s = np.mean((s[:,0] - s[:,1])/np.amax(s[:,0:2], axis=1))
   return(s)

# Learning Automata action selection
def actionselection(action, probability, numactions, numdims):
   for i in range(numdims):
      a = np.random.choice(np.arange(0, numactions), p = probability[:,i])
      mask = np.zeros(numactions,dtype=bool)
      #print(i, a, mask)
      mask[a] = True
      action[mask,i] = 1
      action[~mask,i] = 0
   return(action)

# Learning Automata probability update
def probabilityupdate(action, probability, numactions, numdims, signal, alpha, beta):
   if(numactions > 1):
      for i in range(numdims):
         a = np.where(action[:,i] == 1)
         mask = np.zeros(numactions,dtype=bool)
         mask[a] = True
         #if not signal: # for single value reinforcement signals
         if not signal[i]:
            probability[mask,i] = probability[mask,i] + alpha * (1 - probability[mask,i])
            probability[~mask,i] = (1 - alpha) * probability[~mask,i]
         else:
            probability[mask,i] = (1 - beta) * probability[mask,i]
            probability[~mask,i] = (beta/(numactions-1)) + (1-beta) * probability[~mask,i]		 
   return(probability)

