# -*- coding: utf-8 -*-
"""
Created on Wed Apr 27 12:06:18 2016

@author: henry
"""


##scratching fomc statement
from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.util import ngrams
Date=[]
##monthdict={'January':1,'February':2,'March':3,'April':4,'May':5,'June':6,'July':7,'August':8,'September':9,'October':10,'November':11,'December':12}

fed='https://www.federalreserve.gov'
mainlink='https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm#24561'
html=urlopen(mainlink)
bsobj=BeautifulSoup(html)
link=[]
article=[]


statementlink=bsobj.findAll('a',text='Statement')
for i in statementlink:
    link.append(i.attrs['href'])

link=['/newsevents/press/monetary/20160127a.htm','/newsevents/press/monetary/20160316a.htm','/newsevents/press/monetary/20160427a.htm']+link

for i in link:
    Date.append(re.findall('[0-9]{8}',i)[0])
    subhtml=urlopen(fed+i)
    subobj=BeautifulSoup(subhtml)
    text=subobj.findAll('p')
    content=[]
    text=text[:-1]
    for t in text:
        content.append(t.get_text())
    article.append(content)
    print(i)
    
for yr in range(2000,2011):
    mainlink='https://www.federalreserve.gov/monetarypolicy/fomchistorical'+str(yr)+'.htm'
    html=urlopen(mainlink)
    bsobj=BeautifulSoup(html)
    link=[]
    statementlink=bsobj.findAll('a',text='Statement')
    for i in statementlink:
        link.append(i.attrs['href'])
    for i in link:
        Date.append(re.findall('[0-9]{8}',i)[0])
        subhtml=urlopen(fed+i)
        subobj=BeautifulSoup(subhtml)
        text=subobj.findAll('p')
        content=[]
        ##take out the last paragraph        
        text=text[:-1]
        for t in text:
            content.append(t.get_text())
        article.append(content)
        print(i)
        
for i in range(len(article)):
    for j in range(len(article[i])):
        article[i][j]=article[i][j].strip()

for i in range(len(article)):        
    article[i]=" ".join(article[i])
    words=article[i].split()
    for j in range(len(words)):
        if '\x92' in words[j]:
            idx=words[j].index('\x92')
            words[j]=words[j][:idx]+words[j][idx+4:]
        elif '\xa0' in words[j]:
            idx=words[j].index('\xa0')
            words[j]=words[j][:idx]+words[j][idx+4:]
    article[i]=" ".join(words)
        
for i in range(len(Date)):
    year,month,day=Date[i][:4],Date[i][4:6],Date[i][6:8]
    if month.startswith('0'):
        month=month[-1]
    if day.startswith('0'):
        day=day[-1]
    Date[i]=year+'/'+month+'/'+day

mode='ngram'
##processing articles
arttrim=[]
if mode=='normal':
    tokenizer = RegexpTokenizer(r'\w+')
    pos=['JJ','JJR','JJS','VBD','VBG','VBN','RB','RBR','RBS','VB']
    ##pos=['JJ','JJR','JJS','RB','RBR','RBS','VB']
    for a in article:
        ##get rid of the last part about voting
        if 'Voting' in a:
            a_idx=a.index('Voting')
            a=a[:a_idx]
        temp=tokenizer.tokenize(a)
        if temp[0]=='Release':
            temp=temp[5:]
        temp1=nltk.pos_tag(temp)
        temp2=[i[0] for i in temp1 if i[1] in pos]
        temp2=[i for i in temp2 if i.lower() not in stopwords.words('english')]
        arttrim.append(temp2)
elif mode=='ngram':
    for a in article:
        ##get rid of the last part about voting
        if 'Voting' in a:
            a_idx=a.index('Voting')
            a=a[:a_idx]
        ##get rid of punctuations
        tokenizer = RegexpTokenizer(r'\w+') 
        temp=tokenizer.tokenize(a)
        #get rid of unnecessary first words
        if temp[0]=='Release':
            temp=temp[5:]
        temp=[i.lower() for i in temp if i.lower() not in stopwords.words('english') and i.isdigit()==False]
        temp1=ngrams(temp,3)
        temp3=[' '.join(i) for i in temp1]
        arttrim.append(temp3)
       
