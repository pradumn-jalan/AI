with open("en-ud-train.conllu","rb") as f, open("train.txt","w") as f1:
    for i in f:
        f1.writelines(i)

x=0                     #total no. of training statements
d={}                    #prior state probabilities
cl= [str(j) for j in range(0,10)]
with open("train.txt","r") as f1:
    for i in f1:
        if i[0] in cl:
            l=i.split("\t")
            if i[0]=="1" and i[1]=="\t":
                x=x+1
                if(l[3] in d.keys()):
                     d[l[3]]+=1
                else:
                     d[l[3]]=1
            if(l[3] not in d.keys()):
                    d[l[3]] = 0    
                
for i in d.keys():
    d[i]=d[i]/float(x)
    #i=prev, j=current, Tj=current tag, Ti=prev tag, W=current word  
s=d.keys()    
ep={}       #emission     ep[Tj][Wj] =  p(Wj & Tj)/p(Tj)
tp={}       #transition     tp[Ti][Tj] =  p(Tj & Ti)/p(Ti)
#w={}        #count for total no. of occurance of each word
for i in s:
    ep[i]={}

for i in s:
    tp[i]={}
    for j in s:
        tp[i][j]=0

with open("train.txt","rb") as f1:
    for i in f1:
        if(i[0]=="#"):
            p=""
        if(i[0].isdigit()):
            l=i.split("\t")
            if(l[1] not in ep["ADV"]):
                for j in s:
                    ep[j][l[1]]=0               #insert new word in ep matrix
            ep[l[3]][l[1]]+=1                    
        #transition matrix starts      
            if(p!=""):
                tp[p][l[3]]+=1
            p=l[3]
            
for i in ep:
    sm=sum(ep[i].values())
    for j in ep[i]:
        ep[i][j]=ep[i][j]/float(sm)
            

for i in tp:
    sm=sum(tp[i].values())
    if s!=0:
        for j in tp[i]:
            tp[i][j]=tp[i][j]/float(sm)


y=ep["VERB"].keys()

import pandas as pd

j=raw_input("Enter the line\n")
l=j.strip().split(" ")
#em=pd.DataFrame(ep)
#tm=pd.DataFrame.from_dict(tp)
pp=pd.Series(d)
tags=pp.index.tolist()
df=pd.DataFrame(0.0,index=tags,columns=l)
df=df.astype('object')
start=df.columns[0]
#for i in tags:
    df.at[i,start]=[float(pp[i]*(ep[i][start])),i]
#
#d1={}
#for i in tags:
#    d1[i]=0.0
#vit=[]    
#for i in l:
#    vit.append([i,d1.copy()])
#
#for i in tags:
#       vit[0][1][i]=float(pp[i]*(ep[i][vit[0][0]]))
#
#
#hold=0
#for i in range(1,len(l)):
#    for current in tags:
#        hold=0.0
#        for prev in tags:
#            vit[i][1][current]=max(hold,vit[i-1][1][prev]*tp[prev][current]*ep[current][vit[i][0]])
#            hold=vit[i][1][current]
#        

    
in_words=list(df.columns[1:])
flag=0
for i in in_words:
    for j in tags:
        new=pd.Series()
        for k in tags:
            new[k]=float(tp[k][j]*(df.at[k,l[flag]][0]))
        df.at[j,i]=[float(new.max()*(ep[j][i])),new.argmax()]
    flag=flag+1
    
#printing the conclusions from dataframe df    
rl=l[:]
rl.reverse()
mx=df[rl[0]].max()
amx=''
for i in tags:
    if df[rl[0]][i][0]==mx[0]:
        amx=i

print rl[0]+'\t'+amx
for i in rl[1:]:
    print i+'\t'+mx[1]
    mx=df.at[mx[1],i]
