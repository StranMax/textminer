"""
Python script for transforming text to lemmatized string

Takes input of string, possibly filters by UPOS and
outputs to <LEMMA> <LEMMA> <LEMMA> <...> style string.


This program requires following packages to be installed:
  - trankit >= 1.0.0
"""

__author__ = "Max Strandén"
__version__ = "0.1.0"
__license__ = "MIT"

import argparse
import logging
from pathlib import Path
import re
import time

import torch
from trankit import Pipeline


def cli_args():
    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument("text", type=str, 
                        help="inout text to be lemmatized")
                        
    parser.add_argument("--upos", type=str, nargs="*", 
                        help=("Filter by Universal-Part-Of-Speechs tags. See all UPOS at:"
                              "https://universaldependencies.org/u/pos/index.html")
                       )
                        
    # Optional verbosity counter (eg. -v, -vv, -vvv, etc.)
    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="Verbosity of metadata printing (-v, -vv, etc)")

    # Specify output of "--version"
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s (version {version})".format(version=__version__))

    return parser.parse_args()
    
    
def log_config(verbose):
    match verbose:
        case 0:
            loglevel = logging.ERROR
        case 1:
            loglevel = logging.WARNING
        case 2:
            loglevel = logging.INFO
        case 3:
            loglevel = logging.DEBUG
            
    logging.basicConfig(
        format='[%(asctime)s] - [%(levelname)s] - %(message)s', 
        level=loglevel, 
        datefmt='%d-%b-%y %H:%M:%S'
    )
    
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
    return [[token.get('text') for token in  token_sent.get('tokens')] for token_sent in token_list]
    

def lemmatize(pipeline, pre_tokenized: list[list[str]]):
    """Lemmatize pre tokenized sentences
    
    Takes in a list (document) of lists (sentences) of strings (tokens) and 
    returns a list (document) of lists (sentences) of strings (lemmas)
    """
    lemmatized = [pipeline.lemmatize(sentence, is_sent=True) for sentence in pre_tokenized]        
    lemmas = [[token.get('lemma') for token in sentence.get('tokens')] for sentence in lemmatized]
    return lemmas