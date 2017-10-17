# Test 2  - Question 1

### MySQL Version:

MySQL 5.7

### Data Cleaning

The original csv files "Built_used_area.csv" and "Price_changes.csv" were a bit modified in order to be loaded as tables. The changes were:
* The NULL values found in the built_area or used_area columns were replaced by 0. This new data was uploaded in the file "Built_used_area_sql.csv".
* Nothing changed in the "Price_changes.csv" file, we just renamed it to "Price_changes_sql.csv".

A **database** called *casafari* was created with the following tables:
* The table **"built_used_area"** came from the file "Built_used_area_sql.csv".
* The table **"price_changes"** was created from the data in the file "Price_changes_sql.csv"

### Main points

1. Given a listing_id, there are some duplicates in the table built_used_area, so I grouped them by id and the built and used area were given as the average of the built_area and used_area in all duplicates.

2. The average price per square meter of the property in each price change is given by the new_price divided by the *maximum value* between built area and used area.

3. Finally, because there are some cases where one property had more than 1 price change in the year of 2016, the average price per sqm of that property is given by the average of all the price per sqm of that property in its price changes.

#### Extract the **average price/sqm per property** with an increased price in 2016 that have an area > 200 

```sql
SELECT combined_prices_areas.listing_id, AVG(combined_prices_areas.listing_sqm_price) as avg_sqm_price FROM
	(SELECT prices.listing_id, prices.new_price/GREATEST(areas.built,areas.used) as listing_sqm_price FROM
		(SELECT listing_id, new_price FROM casafari.price_changes WHERE new_price - old_price > 0 and YEAR(STR_TO_DATE(change_date,'%Y-%m-%d')) = 2016) prices
	INNER JOIN
		(SELECT listing_id, AVG(built_area) as built, AVG(used_area) as used FROM casafari.built_used_area WHERE built_area > 200 OR used_area > 200 GROUP BY listing_id) areas
	ON prices.listing_id = areas.listing_id) combined_prices_areas
GROUP BY combined_prices_areas.listing_id
```

Result for a few IDS

|listing_id |avg_sqm_price|
| ------------- |:-------------:| 
|279284	|14018.69160000|
|279299	|8906.25000000|
|279313	|11764.70590000|
|279327	|5394.73680000|
|279344	|6255.62560000|
|279354	|7222.22220000|
|...	|...|

#### Extract the **average price/sqm over all properties** with an increased price in 2016 that have an area > 200
To do that, we have to average the previous results, so that:

```sql
SELECT AVG(combine_all_listings.avg_sqm_price) FROM 
	(SELECT combined_prices_areas.listing_id, AVG(combined_prices_areas.listing_sqm_price) as avg_sqm_price FROM
		(SELECT prices.listing_id, prices.new_price/GREATEST(areas.built,areas.used) as listing_sqm_price FROM
			(SELECT listing_id, new_price FROM casafari.price_changes WHERE new_price - old_price > 0 and YEAR(STR_TO_DATE(change_date,'%Y-%m-%d')) = 2016) prices
		INNER JOIN
			(SELECT listing_id, AVG(built_area) as built, AVG(used_area) as used FROM casafari.built_used_area WHERE built_area > 200 OR used_area > 200 GROUP BY listing_id) areas
		ON prices.listing_id = areas.listing_id) combined_prices_areas
	GROUP BY combined_prices_areas.listing_id) combine_all_listings
```

The new result would be: **6511.09**



