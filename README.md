# textminer

Text mining tools
 

## Installation

Requisites:  
- python>=3.10


> NOTE! GPU-support requires compatible GPU with 
correct version of CUDA-driver, CUDA-toolkit and 
pytorch package. More details on pytorch [here](https://pytorch.org/get-started/locally/).
> With CUDA toolkit 11.8 on Windows 11 system execute following command:  
```
pip install torch==2.0.1 torchvision==0.15.2 torchaudio==2.0.2 --index-url https://download.pytorch.org/whl/cu118
```

Then you can proceed by installing this package in one of three ways:  

1. Tool for converting raw conll-u files to one 
line per document in MALLET style `id	document	LEMMA LEMMA LEMMA ...`  
with stopwords removed (OBSOLETE! NOT MAINTAINED)  
```
pip install git+https://github.com/StranMax/textminer.git@master
```

2. Natural language processing with [trankit](https://github.com/nlp-uoregon/trankit).  
- Sentence segmentation  
- Tokenization  
- Filtering by posdep tags  
- Lemmatization  
```
pip install "textminer[textprocessor] @ git+https://github.com/StranMax/textminer.git@master"
```

3. Sentence embedding and clustering with transformers 
- Sentence embedding  
- Dimensionality reduction  
- Clustering  
- Labeling  
```
pip install "textminer[textanalyser] @ git+https://github.com/StranMax/textminer.git@master"
```

Requisites:

- python>=3.10  
- conllu

## Usage

> Convert conll-u file to <LEMMA> <LEMMA>... style possibly filtered by UPOS:  

```
conllu2doc.exe C:\Users\maxs\Documents\data\kansallisarkiston_oaipmh_haku_maaseutu\conllu C:\Users\maxs\Documents\data\kansallisarkiston_oaipmh_haku_maaseutu\text_corpus_rmstopwords_lemma_ver4.txt -v --upos "NOUN" "VERB" "ADJ"
```

Segment files to sentences and save to csv file:  

For single file:  

```
files2sentences C:\Users\maxst\Desktop\MAAVALTA\docs_maaseutu_07102024\1_14_2003.pdf C:\Users\maxst\Desktop\MAAVALTA\sentence_test\three_files.csv -c C:\Users\maxst\Desktop\MAAVALTA\cache\trankit -vv
```

For directory of pdf files:

```
files2sentences C:\Users\maxst\Desktop\MAAVALTA\test_docs C:\Users\maxst\Desktop\MAAVALTA\sentence_test\three_files.csv -c C:\Users\maxst\Desktop\MAAVALTA\cache\trankit -vv
```

NLP tasks using trankit (OLD STUFF):  
```
preprocess_docs -vvv C:\Users\maxst\Desktop\MAAVALTA\documents C:\Users\maxst\Desktop\MAAVALTA\
```

## TODO list:

> NOTE! This list is outdated. To be updated.

* Threaded read and write (thread safe write with lock)

* Fix ParseException: Failed parsing field 'head': 'NUM' is not a valid value for parse_int_value. Failed parsing field 'head': 'NumType=Card' is not a valid value for parse_int_value. (PROBLEM IN READING COLUMNS CORRECTLY?)