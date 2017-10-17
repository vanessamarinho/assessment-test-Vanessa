# Test 2  - Questions 2 and 3

Questions 2 and 3 were solved together.

### Python version and packages:

* Python 3.6.1
* numpy (version 1.13.3)
* pandas (version 0.20.1)
* matplotlib (version 2.0.2)

### To run the code for questions 2 and 3 do:

```
python predict_visualize_outliers.py
```

## Properties with a sea view

For questions 2 and 3, I first had to select the properties with a sea view. This had to be inferred from the descriptions presented in file *Details.csv* and there were multiple ways to indicate that, such as *views to the sea* and *sea view*.

To solve this, I created an approach that combines **bag of words** with **distant supervision**.
Distant supervision is a technique in which rules (or heuristics) are used to automatically label data. Each property was then represented by its bag of words (i.e. the set of words in the description and their frequencies) and then classified automatically according to a few rules. Such rules are based in two sets of keywords (called seeds in the code). These keyword sets include words frequently found in descriptions related with a sea view and a mountain view. The selected sets are:

* mountain_keywords: **mountain**, **mountains** and **country**
* sea_keywords: **sea**, **ocean**, **beach**, **beaches**, **lake**, **lakes** and **bay**

The main idea is that descriptions that contain sea_keywords are likely to have a "sea view", and so on. It's important to mention that the word **water** was not included in the sea_keywords, even though it can be found in some sea view descriptions. This is because this word is ambiguous and can be used to list other features, such as *central water supply* and *water tank*. Approaches like *n*-grams of words could be used in order to disambiguate those usages of the word *water*.

The created rules are presented below:

* When the bag of words contains **at least one** sea_keywords and **none** mountain_keywords, the property would be classified as **Sea Area**;
* When the bag of words contains **none** sea_keywords and **at least one** mountain_keywords, the property would be classified as **Mountain Area**;
* When the bag of words contains words from both sets, the property would be classified as *Both*;
* The **Undefined** class covers the properties that do not present any of the selected keywords.

After doing this, the distribution of properties and classes were:

| Category        | Occurrences  |
| ------------- |:-------------:| 
| Both      | 322 | 
| Mountain Area      | 481      | 
| Sea Area      | 719      | 
| Undefined | 888      |  

One description from the *Both* class is presented below:
```
Fireplace, Security system, Guest apartment, Jacuzzi, Air conditioning, Basement, Sauna, Built-in kitchen, Sea/lake view, Terrace, Elevator, Mountain view, Swimming pool,  Garden
```

One description from the *Undefined* class is presented below:
```
Security system, Fireplace, Terrace, Guest apartment, Jacuzzi, Air conditioning, Swimming pool, Basement, Sauna,  Guest toilet, Garden, Built-in kitchen
```

**NOTE:** The experiments in question 2 and 3 were then made for properties classified as *Sea Area* and *Both*

## Rationale

My approach for question 2 is based on the two modelling decisions:

1. Even though the question asks to predict only the prices for properties with a sea view and built area between 200 and 300, I included all the properties with a sea view in my analysis (using the previous method to classify). My idea was that by including more data (properties with area between 200 and 300 are just a few), more accurate values for price per square meter (also referred to as price/sqm) would be obtained. In the end, the predicted prices for properties between 200 and 300 are given as 250 (average of the sizes) times the predicted prices/sqm in that particular months.
2. The **prediction task** was performed using a **time series analysis**. However, if I had modelled my time series using the average values of the prices/sqm, the obtained series wouldn't be *stationary* (with constant mean and variance), which is a property required by some prediction methods. Because of this, I modelled the time series as the average variation of the price/sqm, i.e. each point in the time series represents how much the average price/sqm increased (or decreased) compared to the previous period. This technique in which a series is obtained by the subtraction of the original values is known as the *first difference* of a time series. Then, from the predicted average variation of the prices/sqm, it's possible to transform the values back to the prices/sqm and obtain those predicted values. Moreover, the variation values are easier to be obtained from the file *Price_changes.csv*, which only includes the prices of the properties when there are variations. Because we have the old and new prices and we know the size of each property, we easily obtain the variation of the price/sqm (i.e. previous price/sqm - new price/sqm) of a property in each price change. Therefore, the average variation of the price/sqm in a month X is given by the sum of all variations (from the price changes) that happened in that month divided by all properties. 

## Data Cleaning and Transformation

### Missing data

* **Price_changes.csv**: This file had some price changes in which the old_value was equal to 0.  These price changes were disregarded because they do not represent a real price increase. Price changes with any of the values as "nan" were removed.
* **Built_used_area.csv**: The entries with both built_area and used_area equal to "nan" were removed. For the ones in which only one of the values was "nan", this value was replaced to 0.
After that, the entries with both built_area and used_area equal to 0 were removed. This file contained some duplicates, i.e. for some listing_ids, it had more than one entry. In such cases,    
the duplicates were combined in a single listing_id and the built and used area values are replaced by the average of the values in the duplicates.

### New features

After removing the missing data, the dataset **price_changes** (from Price_changes.csv) and the dataset **area** (from Built_used_area.csv) were merged (joined by the id of the listing) with those listing_ids with a sea view (from Details_with_categories.csv - a file created after the classification of the properties, I used classes *Sea Area* and *Both*).

From this combined data, some features were created and a few are described below:

* **months_passed**: It accounts for the number of months since the first observation. The first month in the dataset (January 2016) was considered Month 1. The last month with observed data was Month 20, which is August 2017.
* **price_variation**: It is the difference between the new_price and the old_price of the price change.
* **price_variation_per_square_meter**: It is the price_variation divided by the size of the property. **Note:** The size of the property was considered as the maximum value between the built_area and the used_area.


### Removing Outliers
In order to obtain a model that extracts the main patterns and generalizes well to new observations, data that deviates markedly from others is usually removed. I plotted histograms of several features, namely *built_area*, *used_area*, *new_price*, *old_price*, *price_variation_per_square_meter*. By looking at those graphs, unusual observations are usually spotted. I also created scatterplots to visualize the relationship between the property size and the new_price. These graphs are presented below.

![Old price histogram](feature_analysis/old_price.png?raw=true "Old price histogram") ![New price histogram](feature_analysis/new_price.png?raw=true "New price histogram")

From these two histograms, we can see that almost all prices are lower than 15M (million), with only a few properties with values greater than that. Therefore, entries with new_price or old_price greater than 15 million were removed. 

![Built area histogram](feature_analysis/built_area.png?raw=true "Built area histogram") ![Used area histogram](feature_analysis/used_area.png?raw=true "Used area histogram")

We can see that many values are 0 and most of the properties have sizes lower than a thousand. For both sizes, all the listings with sizes greater than 1250 were removed.

![Built area x New price](feature_analysis/built_areaXprice.png?raw=true "Built area x New price") ![Used area x New price](feature_analysis/used_areaXprice.png?raw=true "Used area x New price") ![Price variation per square meter](feature_analysis/price_variation_per_square_meter.png?raw=true "Price variation per square meter")

From the two first graphs, we visually verify that the price of the property correlates with its size, which suggests that it's a good decision to predict new values based on the price per square meter of all properties. Finally, the last histogram shows the price variation per square meter for all listings. We can see that the prices per square meter from most listings varied between -5000 and +5000. Therefore, all the listings that the price per square meter varied by less than -5000 or more than +5000 were considered unusual and were disregarded.  
 
These graphs are included in the folder "feature_analysis" and can be obtained from the main Python code when the line **create_plots.plots(prices_sea_views_areas)** is uncommented.

## Predict - Question 2
Each month was considered a single observation period. Therefore, we only had 20 observations, from January 2016 to August 2017. As the question requires the prices in January, February, March, April and May 2018, we first need to predict the prices for the months in between, September to December, and then predict the rest, a total of 9 predictions.

One technique that can be used to predict time series values is called moving average, in which the average of the last *n* observations are used to predict the value of the *n+1*. However, this technique is good to predict only a few points in the future. Because I had to predict 9 points in the future, I selected a more complex model called **ARIMA**, which stands for Autoregressive Integrated Moving Average Model. I tried several ARIMA parameters and selected those which returned the best visual results. The time series with the average variation prices/sqm is presented below, in which observed points are presented as blue dots and predicted points as red dots.

![Time series with the average variation prices/sqm](time_series_plots/time_series_variation_values.png?raw=true "Time series with the average variation prices/sqm")

As I mentioned earlier, this obtained time series can be considered *stationary*, since the mean doesn't vary much over time. We see that the averages for the predicted points are positive, negative and then positive again. Now that we predicted the average variation prices/sqm, the actual average prices/sqm are given by applying the successive variations to the initial average price/sqm, which was considered as the average of the old prices of the properties in their first price change. The time series with the average prices/sqm is presented below.

![Time series with the average prices/sqm](time_series_plots/time_series_values_monthly.png?raw=true "Time series with the average prices/sqm")

There is a decreasing trend in this time series, in which the prices/sqm are usually reducing. From this time series, we can see that the predicted values fit fairly well the observed data. A few patters such as steady periods around October and slightly increases around April are reproduced in the predicted values. Using these predicted average prices/sqm, the price of a property with built area between 200 and 300 and sea view was given by 250 * the respective predicted prices. The predicted prices (rounded to the closest integer) are presented below:

| Month        | Price  |
| ------------- |:-------------:| 
| 2018-01      | 1724196 | 
| 2018-02      | 1720897      | 
| 2018-03      | 1721494      | 
| 2018-04 | 1722132      |  
| 2018-05 | 1722905      |

## Undervalued outliers - Question 3
For this question, I included back those unusual points that were removed in Question 2, and I used the average prices/sqm calculated on Question 2 to determine undervalued properties. There were only a few properties with prices greater than 30M (listing_ids=290227, 281582 and 296543) that were removed because these points were making the y axis too large, and we are only interested in undervalued properties, not overvalued ones.

A simple method that can be used to detect outliers is to find the points which are distant from the average by values greater than the standard deviation (i.e. values outside of the range [mean - std, mean + std]). This is based on the fact that in a normal distribution, almost 70% of values are within 1 standard deviation of the mean. In order to identify those points, a scatterplot for each month was created. In each scatterplot, all properties, the average value and the standard deviation around the average are included. Listings with an average price/sqm greater than the average are plotted as green points. On the other hand, listings with an average price/sqm lower than the average are plotted in gray. Points outside the shaded area can be considered outliers (green points are overvalued and grey points are undervalued), since they are far from the average line by more than one standard deviation.

The scatterplots obtained for Months 1 and 5 (January 2016 and May 2016) are presented below:

![Price x Area in 2016/01"](outlier_properties_all_points/undervalues_2016-01.png?raw=true "Price x Area in 2016/01") ![Price x Area in 2016/05](outlier_properties_all_points/undervalues_2016-05.png?raw=true "Price x Area in 2016/05")

The graphs for the other months (which are very similar) are included in the folder "outlier_properties_all_points". We can see that the properties bigger than 1,400 square meters are inside the shaded area. Therefore, in order to better visualize the other gray points, I reduced the x-axis from 3,000 to 1,400. The new graphs for Months 1 and 5 (January 2016 and May 2016) are presented below:

![Price x Area in 2016/01"](outlier_properties/undervalues_2016-01.png?raw=true "Price x Area in 2016/01") ![Price x Area in 2016/05](outlier_properties/undervalues_2016-05.png?raw=true "Price x Area in 2016/05")

A few undervalued outliers are easily spotted. The main one is a property with area of 1,200 and price at around 2,1M (not much greater than the predicted prices for the properties with sizes 200 - 300 in Question 2). A few months later, the price of this property increased a bit, to around 3,2M. Other undervalued outliers have areas between 400 and 800 square meters and price values lower than 2,5M. The scatterplots from the other months do not change much from these two.

I looked at the data and I found out the outlier with area of 1,200. A few features of this property are presented below.

|listing_id | built_area | used_area | old_price | new_price | change_date | Details | Category|
|-----------|:----------:|:---------:|:---------:|:---------:|:-----------:|:-------:|:---------------------------------:| 
|296792	| 0.0	| 1200.0	| 2150000	| 3350000| 2016-05-25	| Mountain view,Sea View,Private... | Both|

**NOTE**: To avoid warnings because this question plots many graphs, the code that creates the scatterplots just loops through the first 6 months, change it to range(1,21) to see the plots for all months. The plots are included in the folder "outlier_properties".