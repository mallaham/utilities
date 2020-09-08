#!/usr/bin/env python
# coding: utf-8

from tqdm import tqdm 
import pandas as pd
import re
import sys
import logging
import warnings

warnings.filterwarnings("ignore")
logging.getLogger().setLevel(logging.INFO)

hashtags = []

def get_hashtag_words(hashtag):
    if len(hashtag)==1 and type(hashtag)==list:
        hashtag = hashtag[0]
        hashtags.append(hashtag.replace("#",''))
    else:
        for tag in hashtag:
            hashtags.append(tag.replace("#",''))


# pd.set_option('display.max_colwidth', -1)


if __name__ == '__main__':
    
    filename = sys.argv[1]
    
    logging.info("Loading data...")
    data = pd.read_csv(filename)
    
    logging.info("parsing hashtags...")
    data['hashtags']=data['tweet'].apply(lambda x: re.findall(r'#[\w]+',x))
    
    logging.info("removing tweets with no hashtags")
    data = data[data.astype(str)['hashtags']!='[]']
    
    for row in tqdm(data['hashtags']):
        get_hashtag_words(row)

    if hashtags:
        pd.DataFrame(hashtags,columns=['hash'])['hash'].value_counts().reset_index().to_csv("hashtags_frequency.csv")

    exit(0)