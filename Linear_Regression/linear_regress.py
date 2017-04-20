f1=open("housing.arff","r") 
f2=open("clean.txt","w")
for i in f1:
    f2.writelines(i)
        
f2.close()
f3=open("clean.txt","r")

features_list=[]
ftype_list=[]
f=0
data_list=[]
for i in f3:
    if i[0:len('@attribute')]=='@attribute':
        l=i.strip().split(" ")
        features_list.append(l[1])
        ftype_list.append(l[2])
        f=1
    elif f==1 and i[0]!='@':
        l=i.strip().split(',')
        data_list.append(l)
        

import pandas as pd
df=pd.DataFrame(data_list,columns=features_list)

import numpy as np


df=df.astype('float')

df.insert(0,'intercept',1.0)                

y=np.array(df['class']) 
df=df.drop('class',axis=1)

theta=np.zeros(shape=len(df.columns),dtype=float)

dsize=len(y)
fsize=len(theta)

x=np.array(df)

x1=np.asmatrix(x)
y1=np.asmatrix(y)
th=((((x1.T)*x1).I)*(x1.T))*(y1.T)      

theta=np.zeros(shape=len(df.columns),dtype=float)       #initial parameters
th2=np.zeros(shape=len(df.columns),dtype=float)         #final parameters


def J():                #cost function
    global theta
    return ((np.square(x.dot(theta).flatten()-y)).sum())/(2*float(dsize))

def gd():               #gradient descent
    global theta
    for l in range(1000000): 
        k=0
        for j in range(fsize):
            k=((x.dot(theta).flatten()-y)*x[:,j]).sum()/(2*float(dsize))
    #        print k
            th2[j]=th2[j]-0.02*k/len(y1)
        theta=np.copy(th2)
        if l%100000==0:
            print "-------------COST " +str(J())
            
def display(th5):       #dispay the parameters
    for i in range(fsize):
        print th5[i]
def err(th5):
    er=((np.square(x.dot(th5).flatten()-y)).sum())/(float(dsize))
    er=np.sqrt(er)
    return er
def abs_err(th5):
    return (np.abs(x.dot(th5).flatten()-y)).sum()/dsize


