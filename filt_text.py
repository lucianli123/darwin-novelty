import pandas as pd 
import pickle
from nltk.tokenize import sent_tokenize
import os
import sys

start=int(sys.argv[1])
books=pd.read_csv("sub_books.csv")
bio=pd.read_csv("bio_auth_books.csv")
bio2=pd.read_csv("bio_auth_books2.csv")
bio=pd.concat((bio,bio2),axis=0)
books=pd.concat((bio,books),axis=0)
books=books.drop_duplicates(subset=["title"])
def filt(sents):
    ret=[]
    for s in sents:
        if len(s)>=45:
            ret.append(s)
    return ret

torun=books[start:start+5000]

for id in torun["id"]:
    if not os.path.exists('filt_vect/'+id+'.pickle'):
        continue
    if os.path.exists('filt_text/'+id+'.pickle'):
        continue
    try:
        file = open('clean/'+id+'.txt', "r", encoding="utf-8")
        text=file.read()
        file.close()
    except:
        continue
    sents = filt(sent_tokenize(text))
    with open('filt_text/'+id+'.pickle', 'wb') as handle:
        pickle.dump(sents, handle, protocol=pickle.HIGHEST_PROTOCOL)
