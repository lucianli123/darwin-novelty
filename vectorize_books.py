from nltk.tokenize import sent_tokenize
import pandas as pd
import glob
import re
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('thenlper/gte-small', device='cpu')
import pickle

import os

import numpy as np

import sys

books=pd.read_csv("sub_books.csv")
start=int(sys.argv[1])

torun=[]
for b in books["id"]:
    if not os.path.exists('vectors/'+b+'.pickle'):
        torun.append(b)

torun=torun[start:start+500]

def filt(sents):
    ret=[]
    for s in sents:
        if len(s)>45:
            ret.append(s)
    return ret


for id in torun:
    if os.path.exists('vectors/'+id+'.pickle'):
        continue
    path=glob.glob('clean/'+id+'.txt')
    try:
        f = open(path[0], "r", encoding="utf-8")
        text=f.read()
    except:
        continue
        

    f.close()
    sents = filt(sent_tokenize(text))
    emb = model.encode(sents)
    emb=np.array(emb)
    
    with open('vectors/'+id+'.pickle', 'wb') as handle:
        pickle.dump(emb, handle, protocol=pickle.HIGHEST_PROTOCOL)
        
        

    