# Test 1  - Vanessa Marinho

* The first part of this test consisted of several CSS3 selectors, which are included in the file *styles.css*
* The regular expressions created in order to match the requested patterns are presented below.

### Regex 1
The results should not include URLs like: "https://mydomain.com/path-to-current-page" and "http://mydomain.com/link-to-ad", which are also in the file:
```
"https?:\/\/[A-Za-z0-9-]+\.[A-Za-z0-9]+\/[A-Za-z0-9-]+listing"
```

### Regex 2
Regex to extract latitude values:
```
(?<=data-coorgps=")[+-]?(\d{1,2}\.\d*|\d{1,2})(?=,)
```

### Regex 3
Regex to extract longitude values:
```
data-coorgps=.+,\K[+-]?(\d{1,3}\.\d*|\d{1,3})(?=")

```

### Regex 4.1
All unique IDs are in the form "LLNNN" where L is a capital letter and N is a number. Total of 211 unique IDs were found.
```
"[A-Z]{2}[0-9]{3}"(?=:)
```

### Regex 4.2
To extract all the IDs with "land":"ESP" inside. A total of 130 IDs were found.
```
"[A-Z]{2}[0-9]{3}"(?=:{[^}]*"land":"ESP".+})
```

As it was suggested to me, the regular expressions were tested here, https://regex101.com/, with the flavor PCRE selected and "/" for the delimiter.