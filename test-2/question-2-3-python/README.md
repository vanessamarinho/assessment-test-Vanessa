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

* When the bag of words contains **at least one** sea_keywords and *none* mountain_keywords, the property would be classified as **Sea Area**;
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

### Removing outliers

![Built area histogram](feature_analysis/built_area.png?raw=true "Built area histogram")