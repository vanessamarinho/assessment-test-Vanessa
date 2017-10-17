# Test 3  - Vanessa Marinho

### Python version and packages:

* Python 3.6.1
* pandas (version 0.20.1)
* NLTK (version 3.2.3)

## Main ideas and assumptions

Almost all Meta location values are not filled, therefore this column was disregarded.

Some descriptions of the properties are in English and Spanish. Therefore, *my first idea* about this test was to identify the language of the description using the lists of stopwords from NLTK. This wasn't helpful because some titles written in English, such as *"2 bedroom apartment for sale, Milla **De** Oro, Marbella, Malaga Costa **del** Sol, Andalucia"*, present many Spanish stopwords, such as *de* and *del*. In addition, there were also English texts with the word "en" instead of "in", which might be a common language dependent error, such as *"Wonderful apartment en Guadalpin Marbella, Golden Miles"* and *"Villa for sale en Marbella"*.

My *second attempt* was to use named entity recognition (NER) systems in the English texts. The goal of these systems is to identify named entities, which are words that name people, organizations and location. However, these systems are case sensitive. In most of them, when a noun is found with capital letters, it's likely that this word will be classified as a Proper Noun, and would be classified as a named entity. Because of that, some words from the descriptions such as *Sale*, *Middle*, *Apartment* were classified as proper nouns. Lower-casing all words wouldn't help finding proper nouns (and therefore the named entities that represent the residential complexes) because all nouns and proper nouns would be mostly classified as nouns, which is mainly what a POS tagger does. Because of these reasons I did not use NER systems, only a POS tagger that I'll explain later. 

In order to split the sentences between the two languages, I then hard coded a few common words found in the Spanish listings, such as *en*, *venta*, *dormitorio*, and *apartamento*. Descriptions with at least one of those Spanish words would be treated as Spanish texts, otherwise the texts are considered as English.

1. The approach to extract candidates for residential complexes from the **Spanish texts** was: 

* I hard coded two regular expressions to extract the possible residential complexes. The first one looks for words found right after the expression **en venta en**. If this expression is found, all following words until a punctuation mark are extracted as a candidate for a residential complex. If this longer expression is not found, I then looked for sequence of words found right after the word **en** (which is a Spanish preposition used for location).

2. The approach to extract candidates for residential complexes from the **English texts** was not hard coded, instead it used a POS tagger. A part-of-speech (POS) tagger is a tool that tags words with their POS. The tags returned by the tagger follow this tagset convention, https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html.

* The text is tagged and we look at all occurrences of the preposition IN. If the preposition IN is followed by a word or a sequence of words tagged as Nouns (NN), Proper Nouns (NNP), and foreign words (FW), these following words are extracted. It's important to mention that this sequence is extracted until we find a word or character (such as punctuation marks) tagged with different POS tags.

After extracting the candidates according to one of the previous presented approaches, I verify if this candidate is not in the list of geographical names [*Marbella*, *Puerto Banus*, *Golden Mile*, *Milla de Oro*, *Malaga*]. If the candidate is not in the list, that description is initially tagged with that residential complex and this candidate is part of the list of possible candidates. Before verifying if the candidate word is in the list of geographical names, a pre-processing code is executed in order to eliminate repeated locations, such as "marbella golden mile marbella golden mile" or "malaga malaga".

## Reclassification of the properties

From the list of possible candidates obtained in the previous step, the ones with frequencies greater than 1 (an attempt to remove some misclassified ones) were selected (list called *selected_locations*) and used to check the dataset one more time. 

In this second look at the dataset, the descriptions classified with residential locations in the *selected_locations* were kept as they are. The text of the descriptions not classified yet or with classifications not on the list (i.e. the ones with frequency less than one) is searched in order to find at least one residential complex from the list *selected_locations*. If one match is found, this description is classified with that residential complex. If no match is found, this text is classified as "UNDEFINED".

This reclassification step is performed in order to generalize the rules to more data, because some descriptions do not include the residential complex after textual indicators such as "en" or "in". Some could simply do "property for sale, reserva de marbella".

## Results

The frequencies of some extracted residential complexes are presented below.

| automatic_category           | Counts |
| -------------------------- |:----------:| 
|UNDEFINED                           | 3942|
|marbella golden mile                 |1370|
|marbella club                         | 73|
|la milla de oro                       | 39|
|lomas del rey                         | 39|
|marina mariola                        | 37|
|reserva de marbella                   | 36|
|marbella alta                         | 34|
|coto real                             | 34|
|centro                                | 33|
|casablanca                            | 32|
|marbella real                         | 31|
|imara                                 | 31|
|alhambra del mar                      | 31|
|... | ...|
|el real   |                              2|
|la caridad |                             2|
|la coneja   |                            2|
|la rinconada |                           2|
|las alamandas |                          2|
|lorcrimar      |                         2|
|marbelah pueblo |                        2|
|marbella centerapartment |               2|
|milla de oro de marbella  |              2|
|marina marbella            |             2|
|la carolina                 |            2|

## Notes

There were a few things that I wanted to try in this test but I didn't have time. One of them was to use a Spanish part-of-speech tagger instead of the hard coded rules. So that the Spanish approach would be similar to the English one, in which Nouns (NN), Proper Nouns (NNP), and foreign words (FW) after a preposition are likely to be residential complexes. As far as I'm aware, NLTK does not provide a Spanish POS tagger but it does provide some Spanish tagged text in which a unigram and bigram tagger can be trained. The other thing would be to include the few filled Meta location values in the analysis.

For this task, some kind of external knowledge could be used in order to achieve better results. For example, extra information would be needed to differentiate "rio verde", "rio verde alto" and "rio verde playa" or group them as the same residential complex.
