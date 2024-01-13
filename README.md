# darwin-novelty

Current code is very messy. Scripts run the pipeline in a semi-automated fashion to download, preprocess, vectorize, and search. 

*ner.ipynb: read in digitized journal articles to extract author names with spacy NER
*author_matches.ipynb: use authors for each discipline to query IA api for matching books 
*download_ia.py: uses book metadata to download full text from IA api and clean text
*vectorize_books.py: uses sentence_transformers to vectorize each sentence 
*build_faiss.py: adds all sentence vectors to FAISS indices. Divides into multiple to prevent out of memory errors.
*find_matches.py: for a list of book embeddings, queries all FAISS indices to identify matches based on cosine similarity
*results.ipynb: generates visualizations from match results.

Jupyter notebooks generally deal with the initial data download, author extraction, and post pipeline analysis/visualization
