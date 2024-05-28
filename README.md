# textminer

Command line tools for text mining

In development stage with following tasks:

1. Task is to create tool for converting raw conll-u files to one 
line per document in MALLET style `id	document	LEMMA LEMMA LEMMA ...`  
with stopwords removed

## Installation

```
pip install git+https://github.com/StranMax/textmining.git@master
```

Requisites:

- python>=3.12  
- conllu

## Usage

```
conllu2doc.exe C:\Users\maxs\Documents\data\kansallisarkiston_oaipmh_haku_maaseutu\conllu C:\Users\maxs\Documents\data\kansallisarkiston_oaipmh_haku_maaseutu\text_corpus_rmstopwords_lemma_ver4.txt -v --upos "NOUN" "VERB" "ADJ"
```

## TODO list:

* Threaded read and write (thread safe write with lock)

* Fix ParseException: Failed parsing field 'head': 'NUM' is not a valid value for parse_int_value. Failed parsing field 'head': 'NumType=Card' is not a valid value for parse_int_value. (PROBLEM IN READING COLUMNS CORRECTLY?)