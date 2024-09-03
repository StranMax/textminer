# textminer

Command line tools for text mining

1. Tool for converting raw conll-u files to one 
line per document in MALLET style `id	document	LEMMA LEMMA LEMMA ...`  
with stopwords removed

2. Natural language processing with [trankit](https://github.com/nlp-uoregon/trankit).  
- Sentence segmentation  
- Tokenization  
- Posdep tagging  
- Lemmatization  

3. Sentence embedding and clustering  
- Sentence embedding  
- Dimensionality reduction  
- Clustering  
- Labeling  

## Installation

> NOTE! GPU-support requires compatible GPU with 
correct version of CUDA-driver, CUDA-toolkit and 
pytorch package. More details on pytorch [here](https://pytorch.org/get-started/locally/).
> With CUDA toolkit 11.8 on Windows 11 system execute following command:  
```
pip install torch==2.0.1 torchvision==0.15.2 torchaudio==2.0.2 --index-url https://download.pytorch.org/whl/cu118
```

Then you can proceed by installing this package normally:  
```
pip install git+https://github.com/StranMax/textmining.git@master
```

or optionally for trankit:  
```
pip install "textmining[preprocessing] @ git+https://github.com/StranMax/textmining.git@master"
```

or for transformers:  
```
pip install "textmining[clustering] @ git+https://github.com/StranMax/textmining.git@master"
```

Requisites:

- python>=3.10  
- conllu

## Usage

```
conllu2doc.exe C:\Users\maxs\Documents\data\kansallisarkiston_oaipmh_haku_maaseutu\conllu C:\Users\maxs\Documents\data\kansallisarkiston_oaipmh_haku_maaseutu\text_corpus_rmstopwords_lemma_ver4.txt -v --upos "NOUN" "VERB" "ADJ"
```

## TODO list:

* Threaded read and write (thread safe write with lock)

* Fix ParseException: Failed parsing field 'head': 'NUM' is not a valid value for parse_int_value. Failed parsing field 'head': 'NumType=Card' is not a valid value for parse_int_value. (PROBLEM IN READING COLUMNS CORRECTLY?)