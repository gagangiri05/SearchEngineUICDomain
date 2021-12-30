#Gagan Giri
#UIN: 674925814

import requests
import os
import re
import pickle
from bs4 import BeautifulSoup
from collections import deque

domain = "uic.edu"
start_url = "https://cs.uic.edu"                

p_folder = "./FetchedPages/"

#The file extensions to ignore while crawling pages
ign_ext = [
    '.pdf', '.doc', '.docx', '.ppt', '.pptx', '.xls', '.xlsx', '.css', '.js',
    '.aspx', '.png', '.jpg', '.jpeg', '.gif', '.svg', '.ico', '.mp4',
    '.avi', '.tar', '.gz', '.tgz', '.zip'
]
#The maximum number of webpages to crawl
crawl_limit = 6000

error_file = "./error_log.txt"
f = open(error_file, "w+")

f.close()

# Queue to perform BFS web traversal
url_que = deque()
url_que.append(start_url)

# List to keep track of traversed URLs
urls_crawled = []
urls_crawled.append(start_url)

# Dict to track pages fetched and stored in folder
p_crawled_dict = {}
page_no = 0

while url_que:
    
    try:
        url = url_que.popleft()            
        rqst = requests.get(url)            # Get html code of web page

        if (rqst.status_code == 200):
            
            soup = BeautifulSoup(rqst.text, 'lxml')
            tags_extracted = soup.find_all('a')                 # Extract all 'a' tags from the page
            def parse_link(link):
    
                link = link.lower()
                link = link.split('#')[0]
                link = link.split('?', maxsplit=1)[0]
                link = link.rstrip('/')
                link = link.strip()

                return link
            if len(tags_extracted) != 0:                        #Reject pages which don't link to another page
                p_crawled_dict[page_no] = url    

                output_file = p_folder + str(page_no)

                os.makedirs(os.path.dirname(output_file), exist_ok=True)     # Create file to store html code

                with open(output_file, "w", encoding="utf-8") as file:
                    file.write(rqst.text)
                file.close()

                for tag in tags_extracted:

                    link = tag.get('href')                  

                    if link is not None and link.startswith("http") and not any(ext in link.lower() for ext in ign_ext):
                        
                        link = parse_link(link)

                        if link not in urls_crawled and domain in link:
                            url_que.append(link)                 # Valid URL to append to the queue
                            urls_crawled.append(link)

                if (len(p_crawled_dict) > crawl_limit):
                    break                                       # Stop crawling when reached limit

                page_no += 1
            

    except Exception as e:
        with open(error_file, "a+") as log:                  # Add error message to error log
            log.write(f"Could not connect to {url}")
            log.write(f"\nError occured: {e}\n\n")
        log.close()

        print("Could not connect to ", url)
        print("Error occured: ", e, " \n")
        continue

pickle_folder = "./PickleFiles/"
os.makedirs(pickle_folder, exist_ok=True)

# Pickling the dict of crawled pages
with open(pickle_folder + '6000_pages_crawled.pickle', 'wb') as f:
    pickle.dump(p_crawled_dict,f)
print('The number of webpages crawled\n')
print(len(p_crawled_dict))