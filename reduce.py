import pandas as pd 
import pickle
import sys
from nltk.tokenize import sent_tokenize
import numpy as np
import os

import sys

#start=int(sys.argv[1])

def filt(sents, filt):
    ret=[]
    for s in sents:
        if len(s)>filt:
            ret.append(s)
    return ret


books=pd.read_csv("sub_books.csv")
bio=pd.read_csv("bio_auth_books.csv")
bio2=pd.read_csv("bio_auth_books2.csv")
bio=pd.concat((bio,bio2),axis=0)
books=pd.concat((bio,books),axis=0)
books=books.drop_duplicates(subset=["title"])

'''
torun=[]
for b in books["id"]:
    if not os.path.exists('filt_vect/'+b+'.pickle'):
        torun.append(b)
torun=torun[start:start+1000]
'''


for id in books["id"]:
    if os.path.exists('filt_vect/'+id+'.pickle'):
        continue

    try:
        file = open('vectors/'+id+'.pickle', 'rb')
        emb = pickle.load(file)
        file.close()
        file = open('clean/'+id+'.txt', "r", encoding="utf-8")
        text=file.read()
        file.close()
    except:
        continue
    sents = filt(sent_tokenize(text), 15)
    if len(sents)!=len(emb):
        sents = filt(sent_tokenize(text), 20)
    new_sent=[]
    delete=[]


    for i in range(0, len(sents)):
        if len(sents[i])<45:
            delete.append(i)
        else:
            new_sent.append(sents[i])
    try:
        emb=np.delete(emb, delete, axis=0)
    except:
        continue

    with open('filt_text/'+id+'.pickle', 'wb') as handle:
        pickle.dump(sents, handle, protocol=pickle.HIGHEST_PROTOCOL)
    with open('filt_vect/'+id+'.pickle', 'wb') as handle:
        pickle.dump(emb, handle, protocol=pickle.HIGHEST_PROTOCOL)