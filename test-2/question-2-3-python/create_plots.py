#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 16 14:20:08 2017

@author: vanessa
"""

import matplotlib.pyplot as plt
import os

def plots(data):
    if not os.path.exists("feature_analysis"):
        os.makedirs("feature_analysis")
    
    #------------- Some plots
    plt.figure()
    data['new_price'].plot.hist(alpha=0.5,bins=50)
    plt.title("Histogram of the column 'new price'")
    plt.xlabel("New price")
    plt.savefig("feature_analysis/new_price.png")
    data['new_price'].describe()
    #We see some outlier prices greater than 15M = remove those.
    
    plt.figure()
    data['old_price'].plot.hist(alpha=0.5,bins=50,color='DarkBlue')
    plt.title("Histogram of the column 'old price'")
    plt.xlabel("Old Price")
    plt.savefig("feature_analysis/old_price.png")
    data['old_price'].describe()
    #We see some outlier prices as weel greater than 15M = remove those.
    
    plt.figure()
    data['used_area'].plot.hist(alpha=0.5,bins=50, color="DarkGreen")
    plt.title("Histogram of the column 'used area'")
    plt.xlabel("Used area")
    plt.savefig("feature_analysis/used_area.png")
    data['used_area'].describe()
    #Some outliers in the used_area as well. Remove those greater than 1250
    
    plt.figure()
    data['built_area'].plot.hist(alpha=0.5,bins=50,color="k")
    plt.title("Histogram of the column 'built area'")
    plt.xlabel("Built area")
    plt.savefig("feature_analysis/built_area.png")
    data['built_area'].describe()
    #Some outliers in the built_area as well. Remove those greater than 1250
    
    plt.figure()
    data['price_variation_per_square_meter'].plot.hist(alpha=0.5,bins=50,color="m")
    plt.title("Histogram of the variation of the price/sqm")
    plt.xlabel("Variation per square meter")
    plt.savefig("feature_analysis/price_variation_per_square_meter.png")
    data['price_variation_per_square_meter'].describe()
    #delete some outliners, properties with a price variation of less than
    #-5000 per sqm and more than 5000 per sqm
    plt.figure()
    plt.scatter(data['used_area'],data['new_price'])
    plt.title("Used area x New price")
    plt.ylabel("New price")
    plt.xlabel("Used area")
    plt.savefig("feature_analysis/used_areaXprice.png")
    
    plt.figure()
    plt.scatter(data['built_area'],data['new_price'],color="y")
    plt.title("Built area x New price")
    plt.ylabel("New price")
    plt.xlabel("Built area")
    plt.savefig("feature_analysis/built_areaXprice.png")