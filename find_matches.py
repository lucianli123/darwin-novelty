from nltk.tokenize import sent_tokenize
import pandas as pd 
import faiss
import pickle

import numpy as np
import sys
import os
i=int(sys.argv[1])





embs=["echoesfrombackwo00levi_0","formofhorseasitl00cars","paper-doi-10_1098_rspl_1859_0004"]

file = open('indexes/'+str(i)+'.pickle', 'rb')
index = pickle.load(file)
file = open('mapping/'+str(i)+'.pickle', 'rb')
book_map = pickle.load(file)


for e in embs:
    out=[]
    try:
        os.mkdir("matches/"+e)
    except:
        pass
    file = open('filt_vect/'+e+'.pickle', 'rb')
    emb = pickle.load(file)
    lims,D,I=index.range_search(emb, 0.9)
    for i in range(0,len(emb)):
        
        for j in range(lims[i],lims[i+1]):
            row=[]
            row.append(i)
            #print(oos[I[i][j]])
            match=book_map[I[j]]
            row.append(match[0])
            row.append(match[1])
            row.append(D[j])
            out.append(row)
    write=pd.DataFrame(out)
    write.columns=["orig_index", "match_id", "match_ind", "score"]
    write.to_csv("matches/"+e+"/"+str(start)+".csv")

