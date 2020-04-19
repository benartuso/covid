#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  8 16:54:23 2020

@author: ben
"""

from tqdm import tqdm 

import pandas as pd
import swifter
import glob

files = glob.glob('*.jsonl')

csv = glob.glob('*.csv')[0]

file = files[0]

file
csv

file.split('.jsonl')[0] + '_reduced.csv' in glob.glob('*.csv') 

def reduce_json(files): 
    csvs = glob.glob('*.csv')
    for file in tqdm(files): 
        if file.split('.jsonl')[0] + '_reduced.csv' in csvs: 
            print("Skipping")
            continue
        df = pd.read_json(file, lines=True)
        df = df[['created_at', 'full_text', 'user', 'place', 'retweet_count', 'favorite_count', 'lang']]
        df['description'] = df.user.swifter.apply(lambda x: x['description'])
        df['location'] = df.user.swifter.apply(lambda x: x['location'])
        df['verified'] = df.user.swifter.apply(lambda x: x['verified'])
        df['followers_count'] = df.user.swifter.apply(lambda x: x['followers_count'])
        df = df.drop(columns = 'user')
        df.to_csv(file.split('.json')[0]+'_reduced.csv', index=False)

import glob
files = glob.glob('*.jsonl')
files.sort()

reduce_json(files)

df = pd.read_json(files[0], lines=True)

head = df.head(50)

place = df[df.place.isna() == False]

files = glob.glob('*.jsonl')

reduce_json(files)



files = glob.glob('*.jsonl')


reduce_json(files)
