# .GOVology

![.GOVology Logo](static/.govology-logo.png)

Studying Data from the US Government's .gov Domain Registry

Utilizing [the data available](https://get.gov/about/data/) for the .GOV registry as well as [TTS' Site Scanning Program](https://digital.gov/guides/site-scanning/) I've started taking a look at some of the forms and functions that seem to be represented in the data.

Note: this is not my operational repository which has some other ad-hoc analysis that is waiting to be finalized before publishing but I wanted to share the baseline automation for others who might find it interesting.

### Methodology
Right now there's a fairly simple set of automation that (1) downloads the .GOV domain data via GitHub (per the Program's recommendation) and (2) TTS' Site Scanning Data.
Currently `generate_data.py` is run manually to take the CISA GET.gov data and convert it into a JSON dataset for the search tool, outlined below.

Note: Site Scanning Data is used more for _ad hoc_ analysis at this time. The .GOV registry data has been useful to see additions, deletions, and updates in near(er) realtime.

### Interactive Search - gov0logy.us
A [search tool](https://gov0logy.us) was developed to help find and filter domain names based on the latest export from the .gov registry. While I often use their [web-based spreadsheet](https://flatgithub.com/cisagov/dotgov-data/blob/main/?filename=current-federal.csv) it seemed like a more interactive and exploratory tool might be useful.

So far the tool supports the following syntax - based on automatic classifications - as defined below:
  - `agency:"*"` - this is a case-insensitive text search for the `Agency` field in the dataset. Note (because of spaces) the agency name should probably be quoted via `"Agency Name"`
  - `org:"*"` - this is a case-insensitive text search for the `Organization name` field in the dataset. Note (because of spaces) the organization  should probably be quoted via `"Org Name"`
  - `len:[<>!](\d+)` - this is the length of the domain name, excluding the three (3) characters for `.gov`
      - This operator will support `<`, `>`, and `!` (not equal), with a number being assumed to mean `=`
      - For example `len:4` are all domains of length 4, `len:<5` are all domaons of length 4 _or less_, `len:!2` are all domains where length is not 2
  - `is_agency: [true|false]` - this is based on whether or not the domain is listed as a term for an agency, per pythons Natural Language Toolkit (NLTK)
      - Note, if `is_agency` is `false` for a domain that doesn't mean it's *not* representative of an agency (since by definition most if not all .gov domains could be considered an agency).
      - a `false` value means that the python NTLK library does not _define_ this domain as belonging to an agency
      - e.g. this might mean Python NLTK needs updating, or perhaps could be considered a sign that the agency needs to do more commmunications, or the domain is a bad match, etc.
      - Code for this test is found in [other_file.md](periodic-table/generate_data.py) with the specific check being `if "agency" in w.definition():`
  - `is_noun: [true|false]` - this is based on whether or not the NLTK Wordnes corpus `nltk.corpus import wordnet as wn` identifies the domain as a 'noun'
      - Code for this test is found in [other_file.md](periodic-table/generate_data.py) with the specific check being `return any(synset.lexname().startswith('noun') for synset in wn.synsets(name))`
  - `is_verb: [true|false]` - this is based on whether or not the NLTK Wordnes corpus `nltk.corpus import wordnet as wn` identifies the domain as a 'verb'
      - Code for this test is found in [other_file.md](periodic-table/generate_data.py) with the specific check being `return any(synset.lexname().startswith('verb') for synset in wn.synsets(name))`
  - `is_acronym: [true|false]` - this is basically a 'meta check' - if the domain isn't (1) recognized as a 'agency', (2) isn't known as a word, (3) isn't a 'noun' or a 'verb' [similar to check #2], or (4) isn't identified as a word (e.g. stem) based on the [Aho-Corasick string matching algorithm](https://www.geeksforgeeks.org/aho-corasick-algorithm-pattern-searching/) then we presume it's an acronym
  - `is_words: {} | [ {_word_: _location_ } ]` - this executes an implementation of the the [Aho-Corasick string matching algorithm](https://www.geeksforgeeks.org/aho-corasick-algorithm-pattern-searching/) to determine if the domain consists of (one of more) words
    - If it is, it will build a list of dictionaries where the key is the 'word' (or root / stem), and the value is the location in the string, e.g. `uspsinformeddelivery` (.gov is removed) contains `is_words` of `{'inform': 4, 'form': 6, 'forme': 6, 'informed': 4, 'formed': 6, 'live': 14, 'deliver': 12, 'liver': 14, 'delivery': 12, 'livery': 14, 'very': 16}`
    - Use this filter as a boolean, e.g. `is:words`
    - Again, code for this check is in [other_file.md](periodic-table/generate_data.py) but is slightly more complicated then a general NLTK check

If you have thoughts on how to further catalogue websites, please reach out!

### References:
    * **List of National Monuments**: https://geojango.com/pages/list-of-national-monuments
    * **TTS Site Scanning Analysis**: https://github.com/CivicActions/site-evaluation-tools/blob/main/digital.gov-scan-upload.js.md
        - [Direct Link to Spreadsheet](https://docs.google.com/spreadsheets/d/1CsXAzCzghYYwXzGCcrJqrsWpr5f7MbID2Qw6vQvi3sQ/edit?gid=497600811#gid=497600811)
