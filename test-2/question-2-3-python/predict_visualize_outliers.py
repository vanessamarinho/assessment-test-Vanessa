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
    #if there are more than one price change per property in the same month, we consider only the last one
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
price_changes = price_changes[price_changes['old_price'] != 0]
price_changes = price_changes.dropna(how = 'all')
area = area.dropna(how = 'all', subset=['built_area','used_area'])
area = area.fillna(0)
area = area[(area['built_area'] + area['used_area'] > 0)]
area = area.groupby("listing_id").mean().reset_index()

#Get all listings with sea view
sea_views = categories[(categories['Category'] == "Sea Area") | (categories['Category'] == "Both")]
#Combine the datasets
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

#-----------------Predict
#To predict prices in January, February, March, April and May 2018
#we need to predict the variation for September to December first
months_to_predict = 9
months = [(pd.Period("09/2017")+i) for i in range(20)]
variation_series = pd.Series(variation_per_sqm['monthly_variation_per_sqm'].tolist(),index=[(pd.Period("01/2016")+i) for i in range(20)])
history = [x for x in variation_series]
predictions = list()
for t in range(months_to_predict):
    #(X,1,Y) = it has to be one, not stationary error
    #(X,,) = reducing the first one makes it more linear, less variation
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
#get the old_price of each property - considered to be the initial price
first_prices_area_info = pd.merge(prices_sea_views_areas, first_prices, on=['listing_id','change_date'])[['listing_id','built_area','used_area','old_price']] 
first_prices_area_info["considered_area"] = first_prices_area_info[["used_area", "built_area"]].max(axis=1)
first_prices_area_info['initial_price_per_sqm'] = first_prices_area_info['old_price']/first_prices_area_info['considered_area']
initial_price_per_sqm = np.mean(first_prices_area_info['initial_price_per_sqm'])

#Array in which the first element is the initial average price/sqm and the next are variations
initial_price_and_variations = [initial_price_per_sqm] + variation_per_sqm['monthly_variation_per_sqm'].tolist() + predictions
#Accumulate to get the values of the price/sqm
price_per_sqm_series = list(accumulate(initial_price_and_variations))

#Calculate predicted values
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

#-----------------Question 3
print("-------------- Question3 --------------")
import os
if not os.path.exists("outlier_properties"):
    os.makedirs("outlier_properties")
#we dont remove unusual data here
prices_sea_views_areas_question3 = pd.merge(area, prices_sea_views, on='listing_id') 
prices_sea_views_areas_question3 = prices_sea_views_areas_question3[(prices_sea_views_areas_question3['old_price'] < 30000000) & (prices_sea_views_areas_question3['new_price'] < 30000000)]
prices_sea_views_areas_question3['months_passed'] = prices_sea_views_areas_question3['change_date'].apply(get_number_of_months)
first_prices = prices_sea_views_areas_question3.groupby('listing_id')['change_date'].agg([min]).rename(columns={'min':'change_date'}).reset_index()
#get the old_price of each property
first_prices_area_info_question3 = pd.merge(prices_sea_views_areas_question3, first_prices, on=['listing_id','change_date'])[['listing_id','built_area','used_area','old_price']] 
first_prices_area_info_question3["considered_area"] = first_prices_area_info_question3[["used_area", "built_area"]].max(axis=1)
    
area = first_prices_area_info_question3['considered_area']
#prices before month 1
updated_prices = first_prices_area_info_question3[['listing_id','old_price']]
updated_prices.columns= [['listing_id','new_price']]
colors = ["DarkGreen","DarkBlue"]

#The undervalued values for all months (20 months) are presented inside the folder "outlier_properties"
#To avoid warnings because this code plots many graphs, the loop below will just go
#through the first 6 months, change it to range(1,21) to see the plots for all
#for month in range(1,21):
for month in range(1,6):
    updated_prices = get_final_values_after_month(month,prices_sea_views_areas,updated_prices)
    listings_price_per_sqm = updated_prices['new_price']/first_prices_area_info_question3['considered_area']
    monthly_avg_deviation = np.std(listings_price_per_sqm)
    plt.figure()
    #to visualize all points, change the value of the two lines to be greater than 3,000 
    plt.xlim(0, 1400)
    x=np.arange(1400)
    #plot average line
    plt.plot(x, price_per_sqm_series[month]*x, '--', color='k')
    plt.fill_between(x, x*(price_per_sqm_series[month]-1*monthly_avg_deviation), x*(price_per_sqm_series[month] +1*monthly_avg_deviation), color='lightgrey',alpha = 0.9)
    plt.ylabel("Price")
    plt.xlabel("Max. between built and used area")
    plt.title("Price x Area in %s" % str(pd.Period("12/2015")+month))
    plt.scatter(area,updated_prices['new_price'], c = listings_price_per_sqm < price_per_sqm_series[month], cmap="Dark2")
    plt.savefig("outlier_properties/undervalues_%s" %str(pd.Period("12/2015")+month))
