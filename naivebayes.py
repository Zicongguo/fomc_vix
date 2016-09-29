# -*- coding: utf-8 -*-
"""
Created on Sun May  1 00:35:51 2016

@author: henry
"""

import nltk
import random
def get_words_in_fomc(fomc):
    all_words=[]
    for (words,label) in fomc:
        all_words.extend(words)
    return all_words

def get_word_features(wordlist):
    wordlist=nltk.FreqDist(wordlist)
    word_features=wordlist.keys()
    return word_features

def extract_features(document):
    document_words=set(document)
    features={}
    for word in word_features:
        features['contains(%s)'% word]=(word in document_words)
    return features

accuracy=[]
accuracy1=[]
size=6
indx=int(len(tagged_art)*size*0.1)
wordlist=get_words_in_fomc(tagged_art[:indx])
word_features=get_word_features(wordlist)
training_set=nltk.classify.apply_features(extract_features,tagged_art[:indx])
test_set=nltk.classify.apply_features(extract_features,tagged_art[indx:])
##test_set1=nltk.classify.apply_features(extract_features,tagged_art1[(indx-81):])
classifier=nltk.NaiveBayesClassifier.train(training_set)
result=nltk.classify.accuracy(classifier,test_set)
##result1=nltk.classify.accuracy(classifier,test_set1)
print('VIX Accuracy is ' +str(result))
accuracy.append(result)    
    
    
    
