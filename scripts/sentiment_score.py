#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 13 19:35:05 2020

@author: ben
"""
import pandas as pd
import vaderSentiment
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import numpy as np
import re
import glob
from tqdm import tqdm
import swifter


def classify_sentiment(sentence):
    analyzer = SentimentIntensityAnalyzer()
    score = analyzer.polarity_scores(sentence)
    lb = score['compound']
    if lb >= 0.05:
        return 1
    elif lb > -0.05: 
        return 0
    else: 
        return -1
    
def get_keyword_sentiment(df, keyword):
    #Eliminate retweets
    df = df[df.full_text.str.contains('RT') == False]
    #Restrict to english: 
    df = df[df.lang == 'en']
    #Filter on keyword 
    df = df[df.full_text.str.lower().str.contains(keyword)].reset_index(drop=True)
    #Add sentiment column
    df['sentiment'] = df.full_text.swifter.apply(classify_sentiment)
    #Scaled sentiment
    df['scaled_sentiment'] = df.sentiment*(df.retweet_count + 1)
    df['retweet_count'] = df['retweet_count'] + 1
    group = df.groupby('sentiment').retweet_count.sum()
    return group


    
def get_favorite_sentiment(df, keyword):
    #Eliminate retweets
    df = df[(df.lang == 'en') & df.full_text.str.lower().str.contains(keyword)]
    #Restrict to english: 
    df['favorite_count']+=1
    #Add sentiment column
    df['sentiment'] = df.full_text.swifter.apply(classify_sentiment)
    #Scaled sentiment\
    group = df.groupby('sentiment').favorite_count.sum()
    return group


def sentiment_history(month, days, keyword):
    date = []
    pos = []
    neg = []
    neut = []
    for day in tqdm(days):
        print("STARTING DAY" + str(day))
        day_pos = 0
        day_neg = 0
        day_neut = 0
        if day < 10: 
            day = '0'+str(day)
        else: day = str(day)
        files = glob.glob('*2020-'+month+'-'+day+'*')
        for file in tqdm(files): 
            df = pd.read_csv(file, lineterminator = '\n', usecols = ['retweet_count', 'full_text', 'lang'])
            group = get_keyword_sentiment(df, keyword)
            if 1 in group.index:
                day_pos += group[1]
            if 0 in group.index:
                day_neut += group[0]
            if -1 in group.index:
                day_neg += group[-1]
        date.append('2020-'+month+'-'+day)
        pos.append(day_pos)
        neut.append(day_neut)
        neg.append(day_neg)
    return pd.DataFrame({'date':date, 'positive': pos, 'neutral': neut, 'neg': neg})

files = glob.glob('*jan*/*')
files.contains('*')
files[0]
def sentiment_favorites(months, days, keyword): 
    month_dict = {'01':'jan', '02':'feb', '03':'mar', '04':'apr'}
    date = []
    pos = []
    neg = []
    neut = []
    for month in months: 
        for day in tqdm(days):
            day_pos = 0 
            day_neg = 0 
            day_neut = 0
            if day < 10: 
                day = '0'+ str(day)
            else: 
                day = str(day)
            files = glob.glob('*'+month_dict[month]+'*/*2020-'+month+'-'+day+'*')
            if len(files) == 0: 
                continue
            for file in files:
                df = pd.read_csv(file, lineterminator = '\n', usecols = ['favorite_count', 'full_text', 'lang'])
                group = get_favorite_sentiment(df, keyword)
                if 1 in group.index:
                    day_pos += group[1]
                if 0 in group.index:
                    day_neut += group[0]
                if -1 in group.index:
                    day_neg += group[-1]
            date.append('2020-'+month+'-'+day)
            pos.append(day_pos)
            neut.append(day_neut)
            neg.append(day_neg)
    return pd.concat([pd.DataFrame({'date': date, 'number':pos, 'type':['positive']*len(date)}),
                      pd.DataFrame({'date': date, 'number':neut, 'type':['neutral']*len(date)}),
                      pd.DataFrame({'date': date, 'number':neg, 'type':['negative']*len(date)})])


whitcheck = sentiment_favorites(['01', '02', '03'], range(1, 32), 'whitmer')
whitcheck.to_csv('whitcheck.csv', index=False)
def remove_pattern(input_txt, pattern):
    r = re.findall(pattern, input_txt)
    for i in r:
        input_txt = re.sub(i, '', input_txt)        
    return input_txt

def clean_tweets(lst):
    # remove twitter handles (@xxx)
    lst = np.vectorize(remove_pattern)(lst, "@[\w]*")
    # remove URL links (httpxxx)
    lst = np.vectorize(remove_pattern)(lst, "https?://[A-Za-z0-9./]*")
    # remove special characters, numbers, punctuations (except for #)
    lst = np.core.defchararray.replace(lst, "[^a-zA-Z#]", " ")
    return lst


