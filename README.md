[ProjectReport_GG_IR.docx](https://github.com/gagangiri05/Search_Engine_on-UIC-Domain/files/7791247/ProjectReport_GG_IR.docx)
# Search_Engine_on-UIC-Domain
A Search Engine that returns top 10 webpages for the given user query


Web Search Engine on UIC Domain
CS 494 Term Project
                                                                                                    Fall 2021
 





ABSTRACT
 
     Gagan Giri
Computer Science Department The University of Illinois at Chicago
Chicago, Illinois 
                ggiri3@uic.edu
 
This document is a report for the final course project for CS494: Information Retrieval course at the University of Illinois at Chicago during the Fall 2021 term. The goal of the project is to design and implement a web search engine for the UIC domain. A web crawler, preprocessing and indexing of online pages, and an IR system using the vector-space model to retrieve webpages relevant to a user query are all included in the search engine.

1	Software Description
All of the functions are modularized for efficient program development, and the software is written in Python(3.8). The search engine retrieves, crawls, and preprocesses 6000 webpages from the UIC domain, which takes 3-4 hours. This is not a process that can be repeated. To run the code without first browsing the UIC domain, the 'Pickle_Files' folder containing all the pickle files that stores the python object as byte streams collected from executing web crawling.py and preproc.py script files that are required to run the code. The search engine can be started by running the search query.py script from the terminal.
1.1	Web Crawler
The script web crawler.py is used to run the web crawler. The UIC-CS department page (https://www.cs.uic.edu/) is the starting point for Web exploration, and crawling is limited to the UIC domain (https://www.uic.edu/). The crawler uses a Breadth-First Search (BFS) method, with the UIC-CS page serving as the root node, and a First in First Out queue for storing URL links to be traversed next. The URL of each web page visited is added to a list of crawled pages, the HTML content is downloaded and parsed using the Beautiful Soup library, and all the page's links are extracted. Only links that correspond to the UIC domain, do not have an irrelevant file extension, and are not already in the queue are appended to the FIFO queue.

                                                                       The crawler's performance is improved by implementing the FIFO queue with a deque rather than a list, because a deque can remove elements from the head in real time. A list, on the other hand, can only remove members from the tail in constant time. Links are popped from the top of the queue in the BFS technique, hence deque was chosen for better efficiency. 

Some file extensions were designated as irrelevant and discarded for web traversal because they did not refer to valid web pages that could be parsed and preprocessed, and downloading these unnecessary extensions would take longer and complicate the process. The file extensions ignored are: '.pdf', '.doc', '.docx', '.ppt', '.pptx', '.xls', '.xlsx', '.css', '.js', '.aspx',’.png', '.jpg', '.jpeg', '.gif', '.svg', '.ico', '.mp4', '.avi', '.tar', '.gz', '.tgz', '.zip' .
The links were processed before being added to the BFS technique's FIFO queue. A query parameter is a set of parameters that are appended to the end of a URL. These are URL extensions that let you define customized content or actions based on the data you're passing. A '?' is appended to the end of a URL to append query parameters, followed by a query parameter. The query parameters denoted by '?' and intra-page anchors denoted by '#' were eliminated, resulting in each URL added to the queue being a distinct web page.
The BFS traverse of links is ended when the FIFO queue becomes empty or the crawling limit is reached. To make the search engine more comprehensive, the crawling limit was set at 6000. Crawling 6000 pages took about 3 hours.
Each web page is saved in the 'FetchedPages' folder. The links to the pages that have been processed and downloaded are saved in a dictionary. The name of the file that stores the link's downloaded content is the key for each link. By pickling the dictionary, it is saved as a file.
 
The file error log.txt contains a list of all the links that the crawler was unable to parse or download, as well as the cause for the failure.
1.2	Preprocessing
The preprocessing of the downloaded web pages is executed by the script preproc.py. A Beautiful Soup object is created for each page that is downloaded. All text on the webpage is taken first, followed by all text that is never accessible in a browser. The text inside the HTML tags <script>, <meta>, and <style> is excluded to achieve this. Following that, the retrieved text is subjected to typical preprocessing methods in order to tokenize it, including the removal of any punctuation, digits, and stop words. Each token is stemmed using Poster Stemmer from the nltk toolkit. Any remaining stop words and tokens with a length of 1 or 2 characters were eliminated after stemming. Each downloaded webpage's tokens are saved in a dictionary.
The inverted index provides for quick and strong searches on enormous amounts of data. After all the text preparation is finished, tokens are created, and an inverted index is calculated. This inverted index is a dictionary of dictionaries. The key is each token in the corpus of web pages' vocabulary, and the value is a dictionary of webpages where the token appears. The key in the internal dictionary is the filename of the downloaded web page, and the matching value is the count of the token on that page.
It takes around 20 minutes to finish the preprocessing of each downloaded web page and the computing of the inverted index. The inverted index and the dictionary of tokens, like the crawler's dictionary of all crawled pages, are stored as pickle files.
1.3	Vector Space Model
The search_engine.py script is executed to process user input query and return the most relevant webpages from the UIC domain.
All of the pickle files for the crawled links, tokens of webpages, and the inverted index are unpickled and extracted first. 
The inverted index is used to generate the Inverse Document Frequency for each webpage-token pair, which is then saved as a separate dictionary. Each webpage's most common token's frequency is calculated
 
which will be used to calculate the term frequency of each token for it’s related webpage. Finally for each token in the corpus, the TF-IDF value is generated and kept as a dictionary of dictionaries like the inverted index. Document length of each web page is calculated to form document vectors for each webpage.
The user enters a query as the input, which is preprocessed and tokenized in the same way as webpage tokens are. The cosine similarity between each downloaded webpage and the query is then computed. The URLs are then sorted by cosine similarity scores in decreasing order and shown to the user as a result.

2	Challenges
•	Initially it took a lot of time in hours to crawl few pages using an early version of the crawler. Because many of the connections were to video, zip files, script files, or document/PDF files rather than genuine webpages. So had to list all these unnecessary file types and decided not to fetch or process them. The following file extensions are ignored: '.pdf', '.doc', '.docx', '.ppt', '.pptx', '.xls', '.xlsx', '.css', '.js', '.aspx', '.png', '.jpg', '.jpeg', '.gif', '. This was done to reduce the time taken in web crawling as the above file extensions were taking a lot of time to download.
•	It was difficult to manage the web crawling and preprocessing results without knowing about the pickle module at first. After using this module, I was able to understand how to write objects to disk as a byte stream.
•	The Beautiful Soup object returned all types of words from the webpage while parsing and extracting the text from each downloaded webpage. These were not English words, and they were producing trash tokens, which may have hampered the vector space model's performance. After going through an internet article, I realized the text inside tags <Script>, <Meta>, and <Style> HTML elements should be ignored as the text included within the aforementioned tags is irrelevant to the user's inquiry.
•	To improve the project's controllability, I started with an integrated python script and subsequently changed to modular programming.

 

3	Weighting Scheme and Similarity Measure
3.1	Weighting Scheme
The TF-IDF of words on websites was employed as a weighting scheme in this project. The TF-IDF (term frequency-inverse document frequency) statistically measures the relevance of a word to a document in a collection of documents. This is accomplished by multiplying two metrics: the number of times a word appears in a document and the word's inverse document frequency over a collection of documents. For fewer common terms in the document corpus, TF-IDF returns higher values. When both IDF and TF values are high, the TF-IDF value is high, indicating that the term is rare in the overall document yet frequent in a document. The semantic meaning of the words is ignored by TF-IDF. It can quickly calculate the similarity of two documents.
3.2	Similarity Measure
The Cosine similarity was the similarity metric used to rank relevant webpages. The length of both the document and the query is taken into account while computing cosine similarity. Cosine similarity is the cosine of the angle between two n-dimensional vectors in an n-dimensional space. Even though there is data duplication, it is useful for determining the similarity between two vectors. Cosine similarity is favorable because two similar documents might have a reduced angle between them even if they are separated by the Euclidean distance. The smaller the angle, greater the resemblance.
3.3	Alternative Similarity measures
Inner Product, Simple Matching, Dice Coefficient, Overlap Coefficient, and Jaccard Coefficient are other similarity metrics that can be used instead of cosine similarity. For each document, Jaccard similarity considers only a single set of words, whereas cosine similarity considers the overall length of the vectors. When examining text similarity, Jaccard similarity is useful for circumstances when duplication is not an issue, whereas cosine similarity is good for cases where duplication is an issue.
4	Evaluation of Queries
The Search Engine was evaluated using five user queries and the top 10 webpages retrieved as result for each query.

 
1.	Query: Research
                              
          
All webpages retrieved were related to the query. 
Precision = 1.0
2.	Query: Data Mining and Text mining


 
Eight retrieved web page has the query terms in them.
Precision = 0.8
3.	Query: Course Catalog


 
All webpages retrieved were related to different course catalogs.
Precision = 1.0
4.	Query: Jobs

All webpages retrieved were related to the query. 
Precision = 1.0

 
5.	Query: Faculty


 

All webpages retrieved were related to the query.
 Precision = 1.0

5	Results
•	  Based on the evaluation of the queries in section 4.The precision value is good. For each query at least the top three ranked returned webpages are actually the top result for all queries.
•	  In a vector space model IR system, Query 4 highlights the benefit of the TF-IDF weighting strategy. Words that appear more frequently in a document, regardless of their frequency in all documents, have a significant effect in establishing the topic of that document. For example, the term 'job' does not appear in every paper, but it does appear often in employment-related documents.
•	 When you search for anything outside of the domain, you'll get less relevant results.
•	 We can observe that for the data mining and text mining query most of the webpages returned have the occurrences of the stemmed query token but the context of query could be to search for the course. It is evident from the result of this query that the query results returned might not always be relevant to the context intended by the query. 

6	Related Work
I went through several internet resources to learn how to do link traversal and web crawling, as well as how to implement Breadth-First Search in Python, parse webpage content, and calculate cosine similarity effectively.





To implement the functions, I referred the documentation for pickle, bs4, and nltk in Python. I read articles on the internet about similarity measures used in informational metrics and how to rank results that are relevant to the user query.

7	Future Work
•	Selecting and adding terms to the user’s query to minimize query document mismatch to improve retrieval performance.
•	Improve web crawling of dynamic pages.
•	A graphical user interface (GUI) program can be used as the search engine's front end.
•	Giving the title portion of a web page more weight than other sections, which might increase efficiency.
•	The crawled pages must be updated on a regular basis in order for the search results to be updated.
•	Improving the recall and precision by introducing LSA (Latent Semantic Analysis) paradigm to the IR system.


