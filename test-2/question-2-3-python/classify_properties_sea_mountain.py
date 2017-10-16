#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 13 10:53:07 2017

@author: vanessa
"""
import pandas as pd
from collections import Counter
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer

categories = ["Mountain Area", "Sea Area"]
number_of_categories = len(categories)
#attempt to classify each listing between the classes
#I got some frequent words that could be found in each category
#GET THE FREQUENCY OF THE WORDS
#WATER:: it's common to find it in the sea category, but 
#this word is misleading - water view, waterfront, central water supply, water tank
#tank. To capture this, we would need to extract 2-grams of words
seeds_per_category = [["mountain","country"],["sea","ocean","beach","lake","bay"]]
#Simple approach that worked fine for this example
#classified as distant supervision approach -
#classify data according to some rules
#another way was to increment it and use techniques to find
#semantic similarity among words - such as wordnet or wordembeddings

#remove punctuation marks, replace / by space
#if it has 0 from one set and some from the other
#classify as the other
#if it doesnt look for similar words -- I didnt add all the words because that 
#wouldnt generalize, may not capture all properties

def classify_one_property(text):
    tokenizer = RegexpTokenizer(r'\w+')
    words = [word.lower() for word in tokenizer.tokenize(text) if word not in stopwords.words('english')]
    occurrences = Counter(words)
    occurrences_per_category = dict.fromkeys(categories,0)
    for category,seeds in zip(categories,seeds_per_category):
        for word in seeds:
            occurrences_per_category[category] += occurrences[word]
    #Classify
    if(occurrences_per_category["Mountain Area"] > 0 and occurrences_per_category["Sea Area"] == 0):
        return "Mountain Area"
    elif(occurrences_per_category["Mountain Area"] == 0 and occurrences_per_category["Sea Area"] > 0):
        return "Sea Area"
    elif(occurrences_per_category["Mountain Area"] > 0 and occurrences_per_category["Sea Area"] > 0):
        return "Both"   
    else:
        return "Undefined"

def classify_all_properties():
    data = pd.read_csv("Details.csv",delimiter=";")
    
    #apply function to all fields
    data['Category'] = data['Details'].apply(classify_one_property)
    data.to_csv("Details_with_categories.csv",sep=";",index = False)
    result = data['Category'].reset_index()
    result = result.groupby('Category').count()
    result.columns = ["occurrences"]
    print(result)


    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    