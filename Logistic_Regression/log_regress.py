f1=open("diabetes.arff","r") 
f2=open("diabetes.txt","w")
for i in f1:
    f2.writelines(i)
        
f2.close()
f3=open("diabetes.txt","r")

features_list=[]
ftype_list=[]
f=0
data_list=[]
y_text=[]
y_value=[]
for i in f3:
    if i[0:len('@attribute')]=='@attribute':
        l=i.strip().split(" ")
        features_list.append(l[1])
        ftype_list.append(l[2])
        f=1
    elif f==1 and i[0]!='@':
        l=i.strip().split(',')
        data_list.append(l[:-1])
        y_text.append(l[-1])
        if l[-1]=='tested_positive':
            y_value.append(1)
        else:
            y_value.append(0)
        
import pandas as pd
df=pd.DataFrame(data_list,columns=features_list[:-1])

import numpy as np

#df        dataframe  768 X 9
#x         np ndarray  768 X 9
#y         np array 9 X 1 label value
#theta     np array 9 X 1 coefficient of x's
#dsize     INT
#fsize     int



df=df.astype('float')

df.insert(0,'intercept',1.0)                
 
theta=np.zeros(shape=len(df.columns),dtype=float)

x=np.array(df)
y=np.array(y_value)

dsize=len(y)
fsize=len(theta)

def display(th5):
    for i in range(fsize):
        print th5[i]

from math import exp
hi=0
def hypo():
    global hi
    hi=np.array(map(lambda x:1/(1+exp(-x)), x.dot(theta)))
    
def cost():
    hypo()
    global hi
    return (y_value*(np.log2(hi))+(np.ones(dsize)-y_value)*np.log2(np.ones(dsize)-hi)).sum()

def ga():               #gradient ascent
    global theta
    it=100000
    alpha=.0002
    for l in range(it):
        theta_new=np.copy(theta)
        for i in range(fsize):
            hypo()
            k=(y-hi).dot(x[:,i])
            theta_new[i]=theta_new[i] + alpha*k/dsize
        theta=np.copy(theta_new)   
        if l%(it/10)==0:
            print "COST---------"+str(cost())
#ga()
#theta_new=np.array([ -3.72375300e+00,   1.15204766e-01,   2.24667679e-02,
 #       -2.06102460e-02,   6.77746680e-04,  -1.36459583e-04,
  #       3.53422179e-02,   4.74200298e-01,  -1.83368826e-04])
theta=theta_new
hypo()

c=0
z=0
o=0
aa=[]
bb=[]
ab=[]
ba=[]

for i in range(dsize):
    if hi[i]<0.5:
        v=0
        z=z+1
        aa.append(x[i,3])
        ba.append(x[i,4])
    else:
        v=1
        o=o+1
        ab.append(x[i,3])
        bb.append(x[i,4])
    if v==y[i]:
        c=c+1
        
accuracy=c/float(dsize)
import matplotlib.pyplot as plt
import matplotlib

plt.plot(ab,bb,'rx',aa,ba,'bx')
#len(y[y==0])           #500
#len(y[y==01])          #268

