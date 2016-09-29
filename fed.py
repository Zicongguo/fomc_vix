# -*- coding: utf-8 -*-
"""
Created on Wed Apr 27 12:06:18 2016

@author: henry
"""


##scratching fomc statement
from bs4 import BeautifulSoup
from urllib2 import urlopen
import re
import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.util import ngrams

fed_url = 'https://www.federalreserve.gov'
fomc_meetings_url = 'https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm#24561'
dates, articles = [], []
# links = ['/newsevents/press/monetary/20160127a.htm','/newsevents/press/monetary/20160316a.htm','/newsevents/press/monetary/20160427a.htm']
# why did you miss June, July and September
links = ['/newsevents/press/monetary/20160127a.htm','/newsevents/press/monetary/20160316a.htm','/newsevents/press/monetary/20160427a.htm', '/newsevents/press/monetary/20160615a.htm', '/newsevents/press/monetary/20160727a.htm', '/newsevents/press/monetary/20160921a.htm']
fomc_meetings_socket = urlopen(fomc_meetings_url)
Bsobj = BeautifulSoup(fomc_meetings_socket, 'html.parser')
statements = Bsobj.findAll('a', text = 'Statement')

for statement in statements:
    links.append(statement.attrs['href'])

for year in range(2000, 2011):
    fomc_yearly_url = fed_url + '/monetarypolicy/fomchistorical' + str(year) + '.htm'
    fomc_yearly_socket = urlopen(fomc_yearly_url)
    Bsobj_Yearly = BeautifulSoup(fomc_yearly_socket, 'html.parser')
    statements_historical = Bsobj_Yearly.findAll('a', text = 'Statement')
    for statement_historical in statements_historical:
        links.append(statement_historical.attrs['href'])

for link in links:
    # date of the article content
    date = re.findall('[0-9]{8}', link)[0]
    date = date.encode('ascii')
    if date[4] == '0':
        date = date[:4] + '/' + date[5:6] + '/' + date[6:]
    else:
        date = date[:4] + '/' + date[4:6] + '/' + date[6:]
    dates.append(date)
    print date
    statement_socket = urlopen(fed_url + link)
    statement = BeautifulSoup(statement_socket, 'html.parser')
    paragraphs = statement.findAll('p')
    content = []
    #print link
    for i in range(len(paragraphs)-1):
        #print paragraphs[i]
        #print "\n"
        # split into paragraphs and put them into a same array
        content.append(paragraphs[i].get_text())
    #print "\n\n\n"
    articles.append(content)

for row in range(len(articles)):
    print articles[row]
    print "\n"
    articles[row] = map(lambda x: x.strip(), articles[row])
    words = " ".join(articles[row]).split()
    # Are you sure your data has the right character encoding? 
    # 0x92 is a smart quote of Windows-1252. 
    # It simply doesn't exist in unicode, therefore it can't be decoded.
    # words = map(lambda x: "".join(x.decode('utf-8').split('\x92')), words)
    # words = map(lambda x: "".join(x.decode('utf-8').split('\xa0')), words)
    articles[row] = " ".join(words)
    print articles[row]
    print "\n\n\n"



mode = 'ngram'
arttrim = []

tokenizer = RegexpTokenizer(r'\w+')
pos = ['JJ','JJR','JJS','VBD','VBG','VBN','RB','RBR','RBS','VB']
##pos = ['JJ','JJR','JJS','RB','RBR','RBS','VB']
for article in articles:
    # get rid of the last part about voting
    if 'Voting' in article:
        idx = article.index('Voting')
        article = article[:idx]
    article = tokenizer.tokenize(article)
    if article[0] == 'Release':
        article = article[5:]
        print article
    if mode == 'ngram':
        article = [a.lower() for a in article if a.lower() not in stopwords.words('english') and a.isdigit() == False]
        article = ngrams(article, 3)
        article = [' '.join(a) for a in article]
    elif mode == 'normal':
        article = nltk.pos_tag(article)
        article = [a[0] for a in article if a[1] in pos]
        article = [a for a in article if a.lower() not in stopwords.words('english')]
    arttrim.append(article)
       
