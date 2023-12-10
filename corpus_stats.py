import pandas as pd
import os
bio=pd.read_csv("bio_auth_books.csv")
bio2=pd.read_csv("bio_auth_books2.csv")
bio=pd.concat((bio,bio2),axis=0)

all=pd.read_csv("sub_books.csv")
all=pd.concat((all,bio),axis=0)
present=[]
lens=[]
for i in all["id"]:
    try:
        f = open("clean/"+i+".txt", "r", encoding="utf-8")
        text=f.read()
        lens.append(len(text))
    except:
        lens.append(0)
    
    if os.path.exists('filt_vect/'+i+'.pickle'):
        present.append(1)
    else:
        present.append(0)

'''
for genre in set(all["subject"]):
    print(genre)
    sub=all[all["subject"]==genre]
    count=0
    for i in sub["id"]:
        if os.path.exists('filt_vect/'+i+'.pickle'):
            count+=1
        present.append(1)
        else:
            present.append(0)
    print(count)
'''

all["done"]=present
all["lens"]=lens
all.to_csv("meta.csv")