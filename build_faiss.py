import pandas as pd 
import faiss
import pickle
import numpy as np
import sys
import os 


index=faiss.IndexFlatIP(384) #intitialize with vector size

start=int(sys.argv[1])

books=pd.read_csv("sub_books.csv")
bio=pd.read_csv("bio_auth_books.csv")
bio2=pd.read_csv("bio_auth_books2.csv")
bio=pd.concat((bio,bio2),axis=0)
books=pd.concat((bio,books),axis=0)
books=books.drop_duplicates(subset=["title"])
id=["OnTheOriginOfSpeciesCharlesDarwin1859","B-001-004-417", "rmcg0005", "onoriginspeciesf00darw", "descentmanandse06darwgoog", "descentman00darwgoog", "in.ernet.dli.2015.44749", "in.ernet.dli.2015.23341", "dli.bengal.10689.8900",'ost-biology-cu31924024737805', 'principlesbiolo00spengoog', 'principlesbiolo06spengoog', 'principlesofsoci0000herb', 'cu31924016915872', 'ecclesiasticalin00spenuoft', 'p2principlesofso01spenuoft', 'politicalinstitu00spenuoft', 'politicalinstitu00spen', 'B-001-004-418', '101619491.nlm.nih.gov', '60820090R.nlm.nih.gov', 'b2129303x', 'b28086065', 'bub_gb_SmFEAAAAcAAJ', 'cu31924090296199', 'dli.ministry.18241', 'onoriginofspeci00darw', 'onoriginofspecie00indarw', 'originofspecie01darw', 'originofspecies0000unse', 'originofspecies00dar', 'originofspeciesb00darw', 'originofspeciesb00darw_3', 'originofspeciesb01darw', 'originofspeciesb02darwuoft', 'originofspeciesb1888darw', 'originspecies01darwgoog', 'descentofmansele0000char', '60820040R.nlm.nih.gov', 'b21293028', 'b21303137', 'b21525043', 'b24765715', 'cu31924022559334', 'descentmanandse03darwgoog', 'descentofmansele00darwuoft', "echoesfrombackwo00levi_0","formofhorseasitl00cars","paper-doi-10_1098_rspl_1859_0004"]
books=books[~books['id'].isin(id)]
torun=[]
for b in books["id"]:
    if os.path.exists('filt_vect/'+b+'.pickle'):
        torun.append(b)
torun=torun[start:start+5000] #create 5000 books FAISS indicies bc of ram limits


count=0
book_map=dict()
sets=0
book_ct=0

for id in torun:

    try:
        file = open('filt_vect/'+id+'.pickle', 'rb')
        emb = pickle.load(file)

        #store mapping of book and sentence metadata
        for e in range(0,len(emb)):
            book_map[count]=(id,e)
            count+=1
        
        faiss.normalize_L2(emb) #cosine distance
        index.add(emb)
        book_ct+=1
    except:
        continue

##search with book embeddings
embs=["spen"]#,"oos","spen", "soc"]

for e in embs:
    out=[]
    file = open('vec_'+e+'.pickle', 'rb')
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


with open('indexes/'+str(start)+'.pickle', 'wb') as handle:
    pickle.dump(index, handle, protocol=pickle.HIGHEST_PROTOCOL)
with open('mapping/'+str(start)+'.pickle', 'wb') as handle:
    pickle.dump(book_map, handle, protocol=pickle.HIGHEST_PROTOCOL)
