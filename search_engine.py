#Gagan Giri
#UIN: 674925814

import math
import os
import copy
import re
from nltk.corpus import stopwords
from collections import Counter
from nltk.stem import PorterStemmer
import pickle

#The number of webpages crawled and indexed
N = 6001

# Extracting english stop words
stop_words = stopwords.words('english')

# Initializing Porter Stemmer object
st = PorterStemmer()

# Folder to store pickel files
pickle_folder = "./PickleFiles/"
os.makedirs(pickle_folder, exist_ok=True)
wp_idf_dict = {}
max_freq = {}
wp_tf_idf = {}

with open(pickle_folder + '6000_inverted_index.pickle', 'rb') as f:
    inverted_index = pickle.load(f)                   # rename

with open(pickle_folder + '6000_webpages_tokens.pickle', 'rb') as f:
    webpages_tokens = pickle.load(f)                   # rename

with open(pickle_folder + '6000_pages_crawled.pickle', 'rb') as f:
    urls = pickle.load(f)                   # rename

# Function for computing the idf of each token in the collection of webpages

def calc_idf(inverted_index):
    
    idf = {}

    for key in inverted_index.keys():
        df = len(inverted_index[key].keys())
        idf[key] = math.log2(N/df)
    
    return idf
    
# Function to compute the tf-idf weighting value of each token

def calc_tfidf(inverted_index):
    
    # Making a temporary copy of the inverted index
    tf_idf = copy.deepcopy(inverted_index)
    
    for token in tf_idf:
        for page in tf_idf[token]:
            tf = tf_idf[token][page] / max_freq[page]
            tf_idf[token][page] = tf * wp_idf_dict[token]
    
    return tf_idf


def calc_doc_len(doc, doc_tokens):
    doc_len_val = 0
    
    for token in set(doc_tokens):
        
        doc_len_val += wp_tf_idf[token][doc] ** 2
    
    doc_len_val = math.sqrt(doc_len_val)
    
    return doc_len_val

# Calculate document lengths for each fetched webpage

def doc_len_pages(list_of_tokens):
    
    doc_len_dict = {}
    
    for page in list_of_tokens:
        

        doc_len_dict[page] = calc_doc_len(page, list_of_tokens[page])
        
    return doc_len_dict

def calc_cos_sim_scores(query, doc_lens):
    similarity_scores = {}
    query_len = 0
    query_weights = {}
    
    query_dict = Counter(query)
    
    
    for token in query_dict.keys():
        token_tf = query_dict[token] / query_dict.most_common(1)[0][1]
        query_weights[token] = token_tf * wp_idf_dict.get(token,0)
        query_len += query_weights[token] ** 2
    
    query_len = math.sqrt(query_len)
    
    for token in query:
        token_weight = query_weights.get(token)

        if token_weight:

            for page in wp_tf_idf[token].keys():
                similarity_scores[page] = similarity_scores.get(page,0) + (wp_tf_idf[token][page] * token_weight)

    for page in similarity_scores:
        similarity_scores[page] = similarity_scores[page] / (doc_lens[page] * query_len)
        

    return similarity_scores

# Function to tokenize query text

def tokenize_query(query_text):
    text = query_text.lower()
    text = re.sub('[^a-z]+', ' ', text)
    tokens = text.split()
    clean_stem_tokens = [
            st.stem(token) for token in tokens 
            if (token not in stop_words and st.stem(token) not in stop_words) and len(st.stem(token))>2
        ]
    return clean_stem_tokens


def show_relevant_pages(count,webpages):
    for i in range(count, count+10):

        try:
            url_no = int(webpages[i][0])
            
        except Exception as e: 
            print("\nNo more results found !!")
            break
            

        if urls.get(url_no, None):
            print(i+1,urls.get(url_no))
    
# show_relevant_pages(0,most_relevant_pages)    

wp_idf_dict = calc_idf(inverted_index)

for page in webpages_tokens:
    max_freq[page] = Counter(webpages_tokens[page]).most_common(1)[0][1]
    
wp_tf_idf = calc_tfidf(inverted_index)
wp_lens = doc_len_pages(webpages_tokens)

print('\n         ------*****UIC Web Search Engine*****------\n')
query = str(input("Enter a search query: "))
print('\n')
query_tokens = tokenize_query(query)

query_simil_pages = calc_cos_sim_scores(query_tokens, wp_lens)
most_relevant_pages = sorted(query_simil_pages.items(), key= lambda x: x[1], reverse=True)

yes = {'y','yes'}
first_pass = True
count = 0

while first_pass or choi.lower() in yes:
    first_pass = False
    show_relevant_pages(count, most_relevant_pages)
    choi = str(input("\nDo you want to more web page results? "))
    count += 10