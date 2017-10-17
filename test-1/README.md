# Test 1  - Vanessa Marinho

* The first part of this test consisted of several CSS3 selectors, which are included in the file *styles.css*
* The regex created in order to match the requested patterns are presented below.

### Regex 1
It should not include URLS like: "https://mydomain.com/path-to-current-page" and "http://mydomain.com/link-to-ad", which are also in the file
```
"https?:\/\/[A-Za-z0-9-]+\.[A-Za-z0-9]+\/[A-Za-z0-9-]+listing"
```

### Regex 2
```
(?<=data-coorgps=")[+-]?(\d{1,2}\.\d*|\d{1,2})(?=,)
```

### Regex 3
```
data-coorgps=.+,\K[+-]?(\d{1,3}\.\d*|\d{1,3})(?=")

```

### Regex 4.1
All unique IDs are of the form "LLNNN" where L is a capital letter and N is a number. Total of 211 unique IDs.
```
"[A-Z]{2}[0-9]{3}"(?=:)
```

### Regex 4.2
To extract all the 130 IDs with "land":"ESP":
```
"[A-Z]{2}[0-9]{3}"(?=:{[^}]*"land":"ESP".+})
```

As Mila suggested me, the regular expressions were all tested here, https://regex101.com/, with the flavor PCRE selected and "/" for the delimiter.