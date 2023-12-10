import pandas as pd 
import pickle
from nltk.tokenize import sent_tokenize
import numpy as np
import glob

def filt(sents):
    ret=[]
    for s in sents:
        if len(s)>=45:
            ret.append(s)
    return ret

'''
f = open("oos.txt", "r", encoding="utf-8")
text=f.read()
f.close()
text=text.replace("\n"," ")
text=text.split("When on board H.M.S. ‘Beagle,’ as naturalist,")[1]
text=text.split("from so simple a beginning endless forms most beautiful and most wonderful have been, and are being, evolved.")[0]
text+="from so simple a beginning endless forms most beautiful and most wonderful have been, and are being, evolved."
text=text.strip()

oos = filt(sent_tokenize(text))
'''
f = open("filt_text/echoesfrombackwo00levi_0.pickle", "rb")
oos = pickle.load(f)

matches=pd.read_csv("matches/echoesfrombackwo00levi_0/0.csv")

for m in matches.itertuples():
    id=m[3]

    try:
        f = open("filt_text/"+id+".pickle", "rb")
        sents = pickle.load(f)
    except:
        continue
    print(oos[int(m[2])])

    
    

    print(sents[int(m[4])])
    print(m[5])
    print()
