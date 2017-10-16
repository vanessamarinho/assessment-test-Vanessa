#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 11 15:18:00 2017

@author: vanessa
"""

from itertools import accumulate
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from statsmodels.tsa.arima_model import ARIMA
from pathlib import Path
#import from local files
import classify_properties_sea_mountain
import create_plots

def get_number_of_months(data):
    data = pd.to_datetime(data)
    return (data.year - 2016)*12 + data.month

def get_avg_variation_per_sqm(price_variation, built, used):
    return price_variation/max(built,used)

def get_final_values_after_month(month, data, previous_values):
    new_values = previous_values.set_index('listing_id')
    data = data[data['months_passed'] == month]
    #if there are more than one price change per property in the same month,
    #we will consider only the last one
    last_prices = data.groupby('listing_id')['change_date'].agg([max]).rename(columns={'max':'change_date'}).reset_index()
    #get the last_price of each property
    month_increases = pd.merge(data, last_prices, on=['listing_id','change_date'])[['listing_id','new_price']].set_index('listing_id')
    new_values.update(month_increases)
    new_values = new_values.reset_index()
    return new_values

#### -------- Question 2
#------------------Read all data
price_changes = pd.read_csv("Price_changes.csv", delimiter = ";")
area = pd.read_csv("Built_used_area.csv", delimiter = ";")
#check if the listings were categorized or not
details_with_categories = Path("Details_with_categories.csv")
if details_with_categories.is_file() == False:
    classify_properties_sea_mountain.classify_all_properties()
categories = pd.read_csv("Details_with_categories.csv", delimiter = ";")

#-----------------Cleaning
#some old prices in the price_changes have values equal to 0.
#delete these lines
price_changes = price_changes[price_changes['old_price'] != 0]
price_changes = price_changes.dropna(how = 'all')
#remove all listings with built area = NAN and used area = NAN
area = area.dropna(how = 'all', subset=['built_area','used_area'])
#fill the remaining NAN with 0
area = area.fillna(0)
#removing the lines where built and used are equal to 0
area = area[(area['built_area'] + area['used_area'] > 0)]
#The file Built_used_area.csv has some listing_id with more than one entry
#This code combines all the duplicates in a single listing and the values
# for the fields will be the average
area = area.groupby("listing_id").mean().reset_index()

#calculate the variation per sqm in all sea view properties
#Get all listings with sea view
#I used the variation of the price per sqm instead of the actual price per
#sm because it would be troublesome to obtain this information from the dataset 
#since we dont have the price of every listing at every month
#this info would need to be inferred from the price changes
#Then I decided to work with the variation and convert it to the price later
sea_views = categories[(categories['Category'] == "Sea Area") | (categories['Category'] == "Both")]
prices_sea_views = pd.merge(price_changes, sea_views, on='listing_id') 
prices_sea_views_areas = pd.merge(area, prices_sea_views, on='listing_id') 

prices_sea_views_areas['months_passed'] = prices_sea_views_areas['change_date'].apply(get_number_of_months)
prices_sea_views_areas['price_variation'] = (prices_sea_views_areas['new_price'] - prices_sea_views_areas['old_price'])
prices_sea_views_areas['price_variation_per_square_meter'] = prices_sea_views_areas.apply(lambda row: get_avg_variation_per_sqm(row['price_variation'], row['built_area'], row['used_area']), axis=1)

#Get plots of the dataframe
#create_plots.plots(prices_sea_views_areas)

#-----------------Removing outliers - 468 before removing outliers, 449 after
prices_sea_views_areas = prices_sea_views_areas[(prices_sea_views_areas['new_price'] < 15000000) & (prices_sea_views_areas['old_price'] < 15000000) & (prices_sea_views_areas['used_area'] < 1250)  & (prices_sea_views_areas['built_area'] < 1250)]
prices_sea_views_areas = prices_sea_views_areas[(prices_sea_views_areas['price_variation_per_square_meter'] > -5000) & (prices_sea_views_areas['price_variation_per_square_meter'] < 5000)]

variation_per_sqm = prices_sea_views_areas.groupby('months_passed')['price_variation_per_square_meter'].agg([np.sum]).rename(columns={'sum':'monthly_variation_per_sqm'}) 
#the variation has to be averaged over all listings, not the number of price_changes in that month
variation_per_sqm['monthly_variation_per_sqm'] = variation_per_sqm['monthly_variation_per_sqm']/len(prices_sea_views_areas['listing_id'].unique())

#Write about the Moving average - which is good to get maybe the next element
#----- Predict
#As we want the prices in January, February, March, April and May 2018
#First let's predict the price/sqm variation in that months and then
#from the initial average price/sqm we can obtain the price per sqm in 
#that periods
#To do that, we need to predict the variation for:
#September - October - November - December - January - ... - May
months_to_predict = 9
months = [(pd.Period("09/2017")+i) for i in range(20)]
variation_series = pd.Series(variation_per_sqm['monthly_variation_per_sqm'].tolist(),index=[(pd.Period("01/2016")+i) for i in range(20)])
history = [x for x in variation_series]
predictions = list()
for t in range(months_to_predict):
    #(X,1,X) = has to be one, not stationary error
    #(X,,) = reduce the first one makes it more linear, less variation
    #tested several values
	model = ARIMA(history, order=(6,1,0))
	model_fit = model.fit(disp=0)
	output = model_fit.forecast()
	predicted = output[0]
	predictions.append(predicted[0])
	history.append(predicted)

plt.figure()
predicted_series = pd.Series(predictions,index=[(pd.Period("09/2017")+i) for i in range(9)])
variation_series.plot(linestyle='--', marker='o')
predicted_series.plot(linestyle='--', marker='o',color="red")
plt.title("Monthly average variation of the price/sqm ")
plt.ylabel("Average Variation")
plt.savefig("time_series_variation_values.png")

#get the date of the first listing of each property
first_prices = prices_sea_views_areas.groupby('listing_id')['change_date'].agg([min]).rename(columns={'min':'change_date'}).reset_index()
#get the old_price of each property
first_prices_area_info = pd.merge(prices_sea_views_areas, first_prices, on=['listing_id','change_date'])[['listing_id','built_area','used_area','old_price']] 
first_prices_area_info["considered_area"] = first_prices_area_info[["used_area", "built_area"]].max(axis=1)
first_prices_area_info['initial_price_per_sqm'] = first_prices_area_info['old_price']/first_prices_area_info['considered_area']
initial_price_per_sqm = np.mean(first_prices_area_info['initial_price_per_sqm'])

#first position is the initial price per sqm and the next are variations
#so I can accumulate and get the value
initial_price_and_variations = [initial_price_per_sqm] + variation_per_sqm['monthly_variation_per_sqm'].tolist() + predictions
price_per_sqm_series = list(accumulate(initial_price_and_variations))

#The average (rounded to the closest integer) price of a property from 200 to 300 meters
#will be calculated as 250 * predicted price per square meter
print("Predicted average price of properties with a sea view between 200 - 300 built area")
for i,price in enumerate(price_per_sqm_series[-5:]):
    forecast = 250 * price
    print("%s : %d" % (str(pd.Period("01/2018")+i),forecast))


plt.figure()
variation_series = pd.Series(price_per_sqm_series[1:21],index=[(pd.Period("01/2016")+i) for i in range(20)])
predicted_series = pd.Series(price_per_sqm_series[21:],index=[(pd.Period("09/2017")+i) for i in range(9)])
variation_series.plot(linestyle='--', marker='o')
predicted_series.plot(linestyle='--', marker='o',color="red")
plt.title("Monthly average price/sqm ")
plt.ylabel("Average price/sqm")
plt.savefig("time_series_values_monthly.png")

#Works fairly well, with a decrease trend, steady periods around october and increase 
#in April


#### -------- Question 3
import os
if not os.path.exists("undervalued_properties"):
    os.makedirs("undervalued_properties")
    
area = first_prices_area_info['considered_area']
#prices before month 1
updated_prices = first_prices_area_info[['listing_id','old_price']]
updated_prices.columns= [['listing_id','new_price']]
colors = ["DarkGreen","DarkBlue"]

# ------ NOTE -----------
#The undervalued properties for all months (20 months) are stored inside the folder "undervalued_properties"
#To avoid a warning about showing more than 20 plots, I'll just loop through the first 5 months
#To see all months, change the line ''for month in range(1,6):'' for ''for month in range(1,21)''.
for month in range(1,6):
    updated_prices = get_final_values_after_month(month,prices_sea_views_areas,updated_prices)
    plt.figure()
    plt.xlim(0, 1300)
    x=np.arange(1300)
    #plot average line
    plt.plot(x, price_per_sqm_series[month]*x, '--', color='k')
    plt.ylabel("Price")
    plt.xlabel("Max. between built and used area")
    plt.title("Price x Area in %s" % str(pd.Period("12/2015")+month))
    plt.scatter(area,updated_prices['new_price'], c = updated_prices['new_price']/first_prices_area_info['considered_area'] < price_per_sqm_series[month], cmap="Dark2")
    plt.savefig("undervalued_properties/undervalues_%s" %str(pd.Period("12/2015")+month))
