# -*- coding: utf-8 -*-
"""
Created on Fri Aug 23 01:31:18 2019

@author: Hello
"""

import requests 
from bs4 import BeautifulSoup as bs
import re


import matplotlib.pyplot as plt
from wordcloud import WordCloud

#creating an empty review list
redmi_reviews = []

for i in range (1,31):
    ip=[]
    url ="https://www.amazon.in/Redmi-Pro-Blue-64GB-Storage/product-reviews/B07DJHR5DY/ref=cm_cr_arp_d_paging_btm_next_2?ie=UTF8&reviewerType=all_reviews&pageNumber="+str(i)
    response = requests.get(url)
    soup = bs(response.content,"html.parser")
    reviews = soup.findAll("span",attrs = {"class","a-size-base review-text review-text-content"})
    for i in range(len(reviews)):
        ip.append(reviews[i].text)
    redmi_reviews = redmi_reviews+ip
    
red_rev_string = " ".join(redmi_reviews)

#red_rev_string = re.sub("[^A-Za-z" "]+"," ",red_rev_string).lower()
#red_rev_string =re.sub("[0-9" "]+"," ",red_rev_string)

#tok
#red_rev_words1 = red_rev_string.split(" ")

import nltk
#red_rev = str(redmi_reviews)
from nltk.tokenize import sent_tokenize    
tokenize_sent = sent_tokenize(red_rev_string)
#tokenize_sent1 = str(tokenize_sent)
#from nltk.tokenize import word_tokenize
#token_word = word_tokenize()

from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords

a = stopwords.words('english')
wordnet = WordNetLemmatizer()

filtered_split=[]
for i in range(len(tokenize_sent)):
    review = re.sub("[^A-Za-z" "]+"," ",tokenize_sent[i])
    review = re.sub("[0-9" "]+"," ",tokenize_sent[i])
    review =review.lower()
    review = review.split()
    review = [wordnet.lemmatize(word) for word in review if not word in set(stopwords.words('english'))]
    review = ' '.join(review)
    filtered_split.append(review)
    
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
tf = TfidfVectorizer()
text_tf= tf.fit_transform(filtered_split)
feature_names =  tf.get_feature_names()
dense = text_tf.todense()
denselist = dense.tolist()
df = pd.DataFrame(denselist, columns = feature_names)

cloud = ",".join(df)

wordcloud= WordCloud(
                      background_color='black',
                      width=1800,
                      height=1400
                     ).generate(cloud)

plt.imshow(wordcloud)

##For positive world cloud 
with open("C:\\Users\\Hello\\Desktop\\Data science\\data science\\assignments\\Text mining\\Datasets\\positive-words.txt","r") as pos:
  poswords = pos.read().split("\n")

poswords = poswords[36:]

red_pos = ' '.join([w for w in df if w in poswords])

wordcloud_pos = WordCloud(
                           background_color = 'black',
                           width =1800,
                           height =1400
                           ).generate(red_pos)
plt.imshow(wordcloud_pos)

##For negative word cloud
with open("C:\\Users\\Hello\\Desktop\\Data science\\data science\\assignments\\Text mining\\Datasets\\negative-words.txt","r") as nos:
    negwords = nos.read().split("\n")
    
negwords =negwords[37:]

red_neg =' '.join([w for w in df if w in negwords])

wordcloud_neg = WordCloud(
        background_color = 'black',
        width = 1800,
        height = 1400
        ).generate(red_neg)
plt.imshow(wordcloud_neg)
