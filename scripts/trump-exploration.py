#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 12 19:02:09 2020

@author: ben
"""

import pandas as pd
import vaderSentiment
file = glob.glob('*.csv')[1]

#Read in.
df = pd.read_csv(file, lineterminator='\n')

#Just english.
df = df[df.lang == 'en']

#Convert to lower. 
df.full_text = df.full_text.str.lower()

#Remove retweets.
df = df[df.full_text.str.contains('rt') == False]



#Trump.

terms = ['realdonaldtrump', 'trump', '@potus']
df4[df4['col'].str.contains('|'.join(terms))] 
df = df[df.full_text.str.contains('|'.join(terms))]

df = df[df.full_text.str.contains('jinping')]


text = df.full_text

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
analyser = SentimentIntensityAnalyzer()

def score(sentence):
    score = analyser.polarity_scores(sentence)
    print("{:-<40} {}".format(sentence, str(score)))
    
    

text = text.reset_index(drop = True)
text = text.full_text
score(text[5])

score("Trump's wet dream. Oh wait, this already happened to BLACK americans")

type(analyser.polarity_scores("Hey bitch"))
def get_score(polarity_dict): 
    comp = polarity_dict['compound']
    if comp >= 0.05: 
        return(1) 
    elif comp >= 0: 
        return(0) 
    else: 
        return(-1)
        
        
results = text.apply(lambda x: get_score(analyser.polarity_scores(x)))
results.value_counts()

evaluation = pd.DataFrame({'text':text, 'sentiment':results})
