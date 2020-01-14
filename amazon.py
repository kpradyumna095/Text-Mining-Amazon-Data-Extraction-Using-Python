# -*- coding: utf-8 -*-
"""
Created on Thu Aug 22 11:25:30 2019

@author: Hello
"""
import requests 
from bs4 import BeautifulSoup as bs
import re


import matplotlib.pyplot as plt
from wordcloud import WordCloud

#creating an empty review list
redmi_reviews = []

for i in range (1,21):
    ip=[]
    url ="https://www.amazon.in/Redmi-Pro-Blue-64GB-Storage/product-reviews/B07DJHR5DY/ref=cm_cr_arp_d_paging_btm_next_2?ie=UTF8&reviewerType=all_reviews&pageNumber="+str(i)
    response = requests.get(url)
    soup = bs(response.content,"html.parser")
    reviews = soup.findAll("span",attrs = {"class","a-size-base review-text review-text-content"})
    for i in range(len(reviews)):
        ip.append(reviews[i].text)
    redmi_reviews = redmi_reviews+ip
    
##Writing reviews in a text file
with open("redmi.txt","w",encoding = 'utf-8') as output:
    output.write(str(redmi_reviews))
    
import os
os.getcwd()

## Joining all the reviews into single paragraph
red_rev_string = " ".join(redmi_reviews)

##Removing unwanted symbols in case present
red_rev_string = re.sub("[^A-Za-z" "]+"," ",red_rev_string).lower()
red_rev_string =re.sub("[0-9" "]+"," ",red_rev_string)

##Splitting each word with space -- Tokanization
red_rev_words = red_rev_string.split(" ")

import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
stop_words = stopwords.words('english')

red_rev_words = [w for w in red_rev_words if not w in stop_words]


## Joining all the reviews into single paragraph
red_rev_string =" ".join(red_rev_words)

# WordCloud can be performed on the string inputs. That is the reason we have combined 
# entire reviews into single paragraph
# Simple word cloud

wordcloud_ip = WordCloud(
                      background_color='black',
                      width=1800,
                      height=1400
                     ).generate(red_rev_string)

plt.imshow(wordcloud_ip)

# positive words # Choose the path for +ve words stored in system
with open("C:\\Users\\Hello\\Desktop\\Data science\\data science\\assignments\\Text mining\\Datasets\\positive-words.txt","r") as pos:
  poswords = pos.read().split("\n")

poswords = poswords[36:]


# negative words  Choose path for -ve words stored in system
with open("C:\\Users\\Hello\\Desktop\\Data science\\data science\\assignments\\Text mining\\Datasets\\negative-words.txt","r") as neg:
  negwords = neg.read().split("\n")
  
negwords =negwords[37:]

##Negative word cloud word cloud
##taking those words from the words which are present in the negative words

red_neg_= ' '.join([w for w in red_rev_words if w in negwords])

##Negative word cloud
wordcloud_neg= WordCloud(
                      background_color='black',
                      width=1800,
                      height=1400
                     ).generate(red_neg_)

plt.imshow(wordcloud_neg)

##Considering only the words which are present in the positive words

red_pos = " ".join([w for w in red_rev_words if w in poswords])

##Building Positive word cloud
wordcloud_pos = WordCloud(
                      background_color='black',
                      width=1800,
                      height=1400
                     ).generate(red_pos)

plt.imshow(wordcloud_pos)


    

##Unique words
red_unique = list(set(" ".join(redmi_reviews).split(" ")))

