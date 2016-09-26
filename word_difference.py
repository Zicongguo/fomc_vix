# -*- coding: utf-8 -*-
"""
Created on Mon Sep  5 10:57:41 2016

@author: henry
"""
import operator
import nltk

positive=list(filter(lambda i:i[1]=="up",tagged_art))
negative=list(filter(lambda i:i[1]=="down",tagged_art))
wordlistpos=get_words_in_fomc(positive)
wordlistneg=get_words_in_fomc(negative)
posfd=dict(nltk.FreqDist(wordlistpos))
negfd=dict(nltk.FreqDist(wordlistneg))
poskey=list(posfd.keys())
negkey=list(negfd.keys())
poskeyunik=[i for i in poskey if i not in negkey]
negkeyunik=[i for i in negkey if i not in poskey]
posfd=sorted(posfd.items(),key=operator.itemgetter(1),reverse=True)
negfd=sorted(negfd.items(),key=operator.itemgetter(1),reverse=True)
