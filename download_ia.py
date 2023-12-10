import sys

import pandas as pd
import os
import glob
from internetarchive import get_item, download, search_items

books=pd.read_csv("sub_books.csv")
start=int(sys.argv[1])

torun=[]
for b in books["id"]:
    if not os.path.exists('books/'+b):
        torun.append(b)


torun=torun[start:start+5000]

def filt(sents):
    ret=[]
    for s in sents:
        if len(s)>15:
            ret.append(s)
    return ret
def clean(str):

    text = str.replace('\r', ' ').replace('\n', ' ')
    #text=re.sub(r'[^a-zA-Z. ]+', '', text)
    text=" ".join(text.split())
    text=text.strip()
    return text


for b in torun:
    if os.path.exists('books/'+b):
        continue

    try:
        download(b, verbose=False, glob_pattern='*txt', destdir="books/")
    except:
        continue
    path=glob.glob('books/'+b+'/*djvu.txt')

    try:
        f = open(path[0], "r", encoding="utf-8")
        text=f.read()
    except:
        continue
    
    if len(text)<1000:
        continue
    text=clean(text)
    out = open("clean/"+b+".txt", "w", encoding="utf-8")
    out.write(text)
    f.close() 