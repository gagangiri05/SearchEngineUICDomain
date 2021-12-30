#Gagan Giri
#UIN: 674925814

import os
import re
import pickle
from bs4 import BeautifulSoup
from bs4.element import Comment
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
# Extracting english stop words
stop_words = stopwords.words('english')

# Initializing Porter Stemmer object
st = PorterStemmer()

# Initializing regex to remove words with one or two characters length
shortword = re.compile(r'\W*\b\w{1,2}\b')

# Folder to store pickel files
pickle_folder = "./PickleFiles/"
os.makedirs(pickle_folder, exist_ok=True)
pages_folder = "./FetchedPages/"
filenames = os.listdir(pages_folder)

# List to store filenames of all stored crawled webpages
files_list = []

for name in filenames:
    files_list.append(name)


def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'meta', '[document]']:
        return False
    elif isinstance(element, Comment):                     # check if element is html comment
        return False
    elif re.match(r"[\s\r\n]+",str(element)):              #  to eliminate remaining extra white spaces and new lines
        return False
    else:
        return True
# Function to extract only the visible text from the html code of each webpage

def get_text_from_code(page):
    soup = BeautifulSoup(page, "lxml")
    text_in_page = soup.find_all(text=True)                # return all text in page
    visible_text = filter(tag_visible, text_in_page)       # return only visible text
    return " ".join(term.strip() for term in visible_text)
# Dictionary to create inverted index
inverted_index = {}

# Dictionary to store tokens in each web page
wp_tokens = {}

for file in files_list:
    web_page = open(pages_folder + file, "r", encoding="utf-8")
    code = web_page.read()
    text = get_text_from_code(code)                     # get all text actually visible on web page
    text = text.lower()
    text = re.sub('[^a-z]+', ' ', text)                 # remove all punctuations and digits
    tokens = text.split()
    
#     # Removing stop words from the tokens
    cleaned_tokens = [word for word in tokens if word not in stop_words]

#     # Stemming the tokens
    stemmed_tokens = [st.stem(word) for word in cleaned_tokens]

#     # Checking for stopwords 
    clean_stem_tokens = [word for word in stemmed_tokens if word not in stop_words]

#     # Converting list of tokens to string
    clean_stem_tokens = ' '.join(map(str,  clean_stem_tokens))

#     # Removing tokens with one or two characters length
    clean_stem_tokens = shortword.sub('', clean_stem_tokens)
    print(clean_stem_tokens, "\n")
    
    # Removing stop words and stemming each token while only accepting stemmed tokens with length greater than 2 
    clean_stem_tokens = [
        st.stem(token) for token in tokens 
        if (token not in stop_words and st.stem(token) not in stop_words) and len(st.stem(token))>2
    ]

    
    wp_tokens[file] = clean_stem_tokens                        # add tokens in web page to dict 
    
    for token in clean_stem_tokens:
        
        freq = inverted_index.setdefault(token,{}).get(file,0)      # get frequency of token and set to 0 if token not in dict
        print(freq)
        inverted_index.setdefault(token,{})[file] = freq + 1        # add 1 to frequency of token in current webpage
        

with open(pickle_folder + '6000_inverted_index.pickle', 'wb') as f:
    pickle.dump(inverted_index,f)
    
with open(pickle_folder + '6000_webpages_tokens.pickle', 'wb') as f:
    pickle.dump(wp_tokens,f)