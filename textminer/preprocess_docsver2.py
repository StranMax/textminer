"""
Python script for preprocessing pdf documents

Follows Trankit workflow

1. PDF to text conversion  
2. Sentence segmentation  
3. Tokenization  
4. Posdep parsing  
5. Lemmatization  



This program requires following packages:
  - list_of_packages_to_be_added
"""

__author__ = "Max Strandén"
__version__ = "0.1.0"
__license__ = "MIT"

import argparse
import logging
from pathlib import Path
import pickle
import re
import time

from PyPDF2 import PdfReader
import torch
from trankit import Pipeline


def cli_args():
    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument("inpath", type=str, 
                        help="path to input document or directory with text (pdf) documents")
                        
    parser.add_argument("outpath", type=str, 
                        help="path to output parent directory")
                        
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
    

def read_file():
    pass

def save_file():
    pass
    
def pdf_to_text(filepath: Path) -> str:
    """Extract text from pdf file
    
    Takes in filepath to pdf document and returns extracted text in one string
    """
    
    reader = PdfReader(filepath)
    pages = [page.extract_text() for page in reader.pages]
    return ' '.join(pages)
    
def segment_sentences(pipeline, txt: str) -> list[str]:
    """Segmentation of sentences
    
    Takes in a string and returns a list of strings, every list element is one sentence
    """
    
    if len(txt) >= 2:
        sentences = pipeline.ssplit(txt)
        return [sentence.get('text') for sentence in sentences.get('sentences')]
    else:
        return None
    
    
def tokenize(pipeline, sentences: list[str]) -> list[list[str]]:
    """Tokenize presegmented sentences
    
    Takes in sentences as a list of strings and returns tokenized 
    sentences as a list of list of strings
    """
    
    token_list = [pipeline.tokenize(sentence, is_sent=True) for sentence in sentences]
    return [[token.get('text') for token in  token_sent.get('tokens')] for token_sent in token_list]
   
   
def parse_posdep(pipeline, tokens: list[list[str]]) -> list[list[dict[str,int, str,str, str,str, str,str, str,str, str,int, str,str]]]:
    """UPOS-tagging and dependency tree parsing of pretokenized input 
    
    Takes in pretokenized document as a list of list of strings/tokens and
    returns list/document of lists/sentences of dictionaries/terms
    """
    
    posdep = [pipeline.posdep(i, is_sent=True) for i in tokens]
    return [sentence.get('tokens') for sentence in posdep]
    
    
def lemmatize():
    pass


def main():
    """ Main entry point of the app """
    args = cli_args()
    # Command line arguments
    INPATH=Path(args.inpath)
    OUTPATH=Path(args.outpath)
    VERBOSE=args.verbose
    
    match VERBOSE:
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
    
    
    pipeline = Pipeline('finnish', gpu=True)
    assert torch.cuda.is_available(), 'CUDA device not found!'
    
    if INPATH.is_dir():
        files = [i for i in INPATH.glob('*') if i.is_file()]
      
      
    for file in files[7:8]:
        logging.debug(f'Starting loop with {file}')
        document = pdf_to_text(filepath=file)
        logging.debug(f'Extracted text from pdf: {type(document)} Characters in doc: {len(document)} Example: {document[0:100]}')
        sentences = segment_sentences(pipeline, document)
        logging.debug(f'Segmented sentences from string: {type(sentences)} Number of sentences in doc: {len(sentences)} Example: {sentences[0:10]}')
        tokens = tokenize(pipeline, sentences)
        logging.debug(f'Tokenized list of sentences: {type(tokens)} {len(tokens)} {tokens[0:5]}')
        posdep = parse_posdep(pipeline, tokens)
        logging.debug(f'UPOS-tagged and parsed dependency tree of tokens: {type(posdep)} {len(posdep)} {posdep[0:5]}')
        
        