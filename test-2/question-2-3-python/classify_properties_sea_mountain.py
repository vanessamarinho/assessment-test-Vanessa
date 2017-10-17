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
#Frequent words that could be found in each category
seeds_per_category = [["mountain","mountains","country"],["sea","ocean","beach","beaches","lake","lakes","bay"]]

def classify_one_property(text):
    tokenizer = RegexpTokenizer(r'\w+')
    words = [word.lower() for word in tokenizer.tokenize(text) if word not in stopwords.words('english')]
    occurrences = Counter(words)
    occurrences_per_category = dict.fromkeys(categories,0)
    for category,seeds in zip(categories,seeds_per_category):
        for word in seeds:
            occurrences_per_category[category] += occurrences[word]
    #Classify according to the occurrence of seed words
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
    
    data['Category'] = data['Details'].apply(classify_one_property)
    data.to_csv("Details_with_categories.csv",sep=";",index = False)
    result = data['Category'].reset_index()
    result = result.groupby('Category').count()
    result.columns = ["occurrences"]
    print(result)


    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    