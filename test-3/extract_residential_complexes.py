#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 12 08:54:34 2017

@author: vanessa
"""
from nltk import pos_tag, word_tokenize
from nltk.tokenize import RegexpTokenizer
import pandas as pd
import re
import string
import unicodedata

def pre_process_title(title):
    #convert accented characters to its unaccented version
    title = ''.join(c for c in unicodedata.normalize('NFD', title) if unicodedata.category(c) != 'Mn')
    printable = set(string.printable)
    #removing non-ascii characters, found on some listing
    title = ''.join(filter(lambda x: x in printable, title))
    #remove codes and numbers from the properties listings
    title = re.sub(r"[A-Za-z]*\d+"," ",title)
    title = title.replace("–"," ")
    return title

def classify_location_automatically(data,selected_locations):
    value = data['automatic_category'] 
    if value in selected_locations: 
        return value
    else:
        text = data['Title'].lower()
        for location in selected_locations:
            if location in text:
                return location
        return "UNDEFINED"
            

def classify_location_with_sentence_patterns(title):
    tokenizer = RegexpTokenizer(r'\w+')
    #chunked = ne_chunk(pos_tag(word_tokenize(title)))
    #common words found in the spanish listings
    location = ""
    if any(word in ['en','venta','dormitorio','apartamento'] for word in tokenizer.tokenize(title.lower())):
        title = title.lower()
        longer_pattern = re.search('(?<= en venta en )[a-z ]*',title)
        if longer_pattern:
            location = longer_pattern.group(0)
        else:
            shorter_pattern = re.search('(?<= en )[a-z ]*',title)
            if shorter_pattern:
                location = shorter_pattern.group(0)
        
    else:
        #words have to keep its capitalization for the pos_tag
        #this tokenization that keeps the punctuation mark is needed
        #to break the place.
        chunked = pos_tag(word_tokenize(title))
        #now we dont neet capital letters
        chunked = [(element[0].lower(),element[1]) for element in chunked]
        #get all occurrences
        indices = [i for i, x in enumerate(chunked) if x == ("in","IN")]
        if len(indices) > 0:  
            for index_in in indices:
                location_parts =list()
                for element in chunked[index_in+1:]:
                    if(element[1] == 'NN' or element[1] == 'NNP' or element[1] == 'FW'):
                        location_parts.append(element[0])
                    else:
                        break
                if(len(location_parts)) > 0:
                    location = " ".join(location_parts)
                    break
    if location not in ['marbella', 'puerto banus', 'golden mile', 'milla de oro', 'malaga']:
        return location
    else:
        return " "

if __name__ == "__main__":
    data = pd.read_csv("Titles_gmile_pbanus.csv",delimiter=";")
    #Almost all meta location fields are NULL
    data['Title'] = data['Title'].apply(pre_process_title)
    
    data['automatic_category'] = data['Title'].apply(classify_location_with_sentence_patterns)
            
    result = data[data['automatic_category'].str.len() > 1]['automatic_category'].reset_index()
    result = result.groupby('automatic_category').count()
    result.columns = ["occurrences"]
    #remove least frequent entities found - avoid overfitting
    result = result[result['occurrences'] >= 2]
    #get the longest strings first to try to match them
    selected_locations = result.index.values.tolist()
    selected_locations.sort(key=len, reverse = True)
    
    #get the empty entries and see if they have some of the identified locations
    data['automatic_category'] = data.apply(lambda row: classify_location_automatically(row, selected_locations),axis=1) 
    result = data['automatic_category'].groupby(data['automatic_category']).count()
    print(result.sort_values(ascending=False))
    
    
    #improvements - some kind of external knowledge has to be used
    #to identify for example that "rio verde", "rio verde alto" and "rio verde playa" are the same thing
    
    #TODO: FROM THE UNDEFINED, SEE HOW MANY ARE MARBELLA...
    
    
    
    
    
    
    
    