#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 11 20:12:30 2020

@author: ben
"""

import pandas as pd
import glob
from tqdm import tqdm

glob.glob('*.csv')

'*2020-02' + ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09'] + '*'


month = '02'
day = '01'

glob.glob('*2020-' + month + '-' + day + '*')


def word_trends(month, days, word):
    word_array = []
    date = []
    for day in tqdm(days): 
        day_counter = 0
        files = glob.glob('*2020-' + month + '-' + day + '*')
        for file in files:
            day_counter += pd.read_csv(file, lineterminator='\n').full_text.str.lower().str.contains(word).sum()
        word_array.append(day_counter)
        date.append('2020-'+ month + '-' + day)
    return pd.DataFrame({word:word_array, 'date':date})
            
#and...

jan = word_trends('01', ['22', '23', '24', '25', '26', '27', '28', '29', '30', '31'], 'covid')            

feb = word_trends('02', ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19'], 'corona')

result2 = pd.read_csv('jan_mentions_per_day.csv')


import matplotlib.pyplot as plt
plt.plot(feb.date, feb.corona)
files = glob.glob('*')
files.sort()


final = pd.concat([result, result2])
final['date'] = pd.to_datetime(final.date)

import matplotlib.pyplot as plt

plt.bar(final.date, final.covid)


pd.read_csv()

file = glob.glob('*')[0]


df = pd.read_csv(file, lineterminator='\n')

df.full_text.str.lower().str.contains('covid').sum()
