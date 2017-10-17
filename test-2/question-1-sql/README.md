# Test 2  - Question 1

## Version:

MySQL 5.7

Given an ID, there are some duplicates in the table built_used_area, so I grouped by id and the built and used area will be given as the average of the built_area and used_area in all duplicates.

The average price per square meter of the property in each price change would be the new_price divided by the maximum size between built area and used area.

Finally, because there are some cases where one property had more than 1 price changes in the year of 2016, the average price per sqm of that property is given by the average of all the price per sqm of that property during its price changes.

SQL code that gives the avg/sqm per listing

```
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

If we want to have the avg sqm over all listings, one more thing:

```
SELECT AVG(combine_all_listings.avg_sqm_price) FROM 
	(SELECT combined_prices_areas.listing_id, AVG(combined_prices_areas.listing_sqm_price) as avg_sqm_price FROM
		(SELECT prices.listing_id, prices.new_price/GREATEST(areas.built,areas.used) as listing_sqm_price FROM
			(SELECT listing_id, new_price FROM casafari.price_changes WHERE new_price - old_price > 0 and YEAR(STR_TO_DATE(change_date,'%Y-%m-%d')) = 2016) prices
		INNER JOIN
			(SELECT listing_id, AVG(built_area) as built, AVG(used_area) as used FROM casafari.built_used_area WHERE built_area > 200 OR used_area > 200 GROUP BY listing_id) areas
		ON prices.listing_id = areas.listing_id) combined_prices_areas
	GROUP BY combined_prices_areas.listing_id) combine_all_listings
```

The result would be: **6511.091194242416**



