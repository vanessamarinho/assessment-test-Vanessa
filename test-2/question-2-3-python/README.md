# Test 2  - Questions 2 and 3

Questions 2 and 3 were solved together.

### Python version and packages:

* Python 3.6.1
* numpy (version 1.13.3)
* pandas (version 0.20.1)
* matplotlib (version 2.0.2)

## Properties with a sea view

For questions 2 and 3, I first had to select the properties with a sea view. This had to be inferred from the descriptions presented in file *Details.csv* and there were multiple ways to indicate that, such as *views to the sea* and *sea view*.

To solve this, I created an approach that combines **bag of words** with **distant supervision**.
Distant supervision is a technique in which rules (or heuristics) are used to automatically label data. Each property was then represented by its bag of words (i.e. the set of words in the description and their frequencies) and then classified automatically according to a few rules. Such rules are based in two sets of keywords (called seeds in the code). These keyword sets include words frequently found in descriptions related with a sea view and a mountain view. The selected sets are:

* mountain_keywords: **mountain** and **country**
* sea_keywords: **sea**, **ocean**, **beach**, **lake** and **bay**

The main idea is that descriptions that contain sea_keywords are likely to have a "sea view", and so on. It's important to mention that the word **water** was not included in the sea_keywords, even though it can be found in some sea view descriptions. This is because this word is ambiguous and can be used to list other features, such as *central water supply* and *water tank*. Approaches like *n*-grams of words could be used in order to disambiguate those usagesof the word *water*.

The created rules are presented below:

* When the bag of words contains **at least one** sea_keywords and **none** mountain_keywords, the property would be classified as **Sea Area**;
* When the bag of words contains **none** sea_keywords and **at least one** mountain_keywords, the property would be classified as **Mountain Area**;
* When the bag of words contains words from both sets, the property would be classified as *Both*;
* The **Undefined** class covers the properties that do not present any of the selected keywords.

After doing this, the distribution of properties and classes were:

| Category        | Occurrences  |
| ------------- |:-------------:| 
| Both      | 318 | 
| Mountain Area      | 471      | 
| Sea Area      | 722      | 
| Undefined | 899      |  

One description from the *Both* class is presented below:
"Fireplace, Security system, Guest apartment, Jacuzzi, Air conditioning, Basement, Sauna, Built-in kitchen, Sea/lake view, Terrace, Elevator, Mountain view, Swimming pool,  Garden"

One description from the *Undefined* class is presented below:
"Security system, Fireplace, Terrace, Guest apartment, Jacuzzi, Air conditioning, Swimming pool, Basement, Sauna,  Guest toilet, Garden, Built-in kitchen"

**NOTE:** The experiments in question 2 and 3 were then made for properties classified as *Sea Area* and *Both*

## Rationale

My approach for question 2 is based on the two modelling decisions:

1. Even though the question asks to predict only the prices for properties with a sea view and built area between 200 and 300, I included all the properties with a sea view in my analysis (using the previous method to classify). My idea was that by including more data (properties with area between 200 and 300 are just a few), more accurate values for price per square meter (also referred to as price/sqm) would be obtained. In the end, the predicted prices for properties between 200 and 300 are given as 250(average of the sizes) times the predicted prices/sqm in that particular months.
2. The **prediction task** was performed using a **time series analysis**. However, if I had modelled my time series using the average values of the prices/sqm, the obtained series wouldn't be *stationary* (with constant mean and variance), which is a property required by some prediction methods. Because of this, I modelled the time series as the variation of the average price/sqm, i.e. each point in the time series represents how much the average price/sqm increased (or decreased) compared to the previous period. This technique in which values are subtracted is known as the *first difference* of a time series. Then, from the predicted variation of the average prices/sqm, it's possible to transform the data back to the prices/sqm and obtain those predicted values. Moreover, the variation values are easier to be obtained from the file *Price_changes.csv*. In every price change, we have the old and new prices and we know the size of the property, so we have the variation of the price/sqm of that property in a particular month. The variation of average price/sqm in each month is given by the average of those variations (from the price changes) over all properties. 

## Data Cleaning and Transformation

### Missing data

* **Price_changes.csv**: This file had some price changes in which the old_value was equal to 0.  These price changes were disregarded because they do not represent a real price increase. Price changes with any of the values as "nan" were removed.
* **Built_used_area.csv**: The entries with both built_area and used_area equal to "nan" were removed. For the ones in which only one of the values was "nan", this value was replaced to 0.
After that, the entries with both built_area and used_area equal to 0 were removed. This file contained some duplicates, i.e. for some listing_ids, it had more than one entry. In such cases,    
the duplicates were combined in a single listing_id and the built and used area values are replaced by the average of the values in the duplicates.

### New features

The 
Three features were created:

* **months_passed**: It accounts for the number of months since the first observation. The first month in the dataset (January 2016) was considered Month 1. The last month with observed data was Month 20, which is August 2017.
* **price_variation**: It is the difference between the new_price and the old_price.


### Outliers



![Built area histogram](feature_analysis/built_area.png?raw=true "Built area histogram")