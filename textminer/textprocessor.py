"""
Python functions for processing text

Takes input as a string and converts to sentences,
tokens or lemmas


This program requires following packages to be installed:
  - trankit >= 1.0.0
  - torch
"""

__author__ = "Max Strandén"
__version__ = "0.1.0"
__license__ = "MIT"

from pathlib import Path

import torch
from trankit import Pipeline
    
    
def segment_sentences(pipeline, text: str) -> list[str]:
    """Segmentation of sentences
    
    Takes in a single string (document) and returns a list of strings, one list element per sentence
    """
    if len(text) >= 2:  # pdf to text transformation fails for scanned documents and returns empty string (len(text) == 1)
        sentences = pipeline.ssplit(text)
        return [sentence.get('text') for sentence in sentences.get('sentences')]
    else:
        return None
        
        
def tokenize(pipeline, sentences: list[str]) -> list[list[str]]:
    """Tokenize presegmented sentences
    
    Takes in a list (document) of strings (sentences) and returns list (document) of lists (sentences)
    of strings (tokens)
    """
    token_list = [pipeline.tokenize(sentence, is_sent=True) for sentence in sentences]
    tokens = [[token.get('text') for token in token_sent.get('tokens')] for token_sent in token_list]
    return tokens
    
    
def filter_posdep(pipeline, pre_tokenized: list[list[str]], upos: list[str]) -> list[list[str]]:
    """Filter tokens by UPOS-tags
    
    Takes in a list (document) of strings (sentences) and list of upos to match
    Returns list (document) of lists (sentences) of strings (tokens) 
    """
    posdep = [pipeline.posdep(sentence, is_sent=True) for sentence in pre_tokenized]
    tokens = [[token.get('text') for token in sentence.get('tokens') if token.get('upos') in upos] for sentence in posdep]
    return tokens
    

def lemmatize(pipeline, pre_tokenized: list[list[str]]):
    """Lemmatize pre tokenized sentences
    
    Takes in a list (document) of lists (sentences) of strings (tokens) and 
    returns a list (document) of lists (sentences) of strings (lemmas)
    """
    lemmatized = [pipeline.lemmatize(sentence, is_sent=True) for sentence in pre_tokenized]        
    lemmas = [[token.get('lemma') for token in sentence.get('tokens')] for sentence in lemmatized]
    return lemmas