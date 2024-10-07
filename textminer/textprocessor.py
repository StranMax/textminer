"""
Python functions for processing text

Takes input as a string and converts to sentences,
tokens or lemmas


This program requires following packages to be installed:
  - trankit >= 1.0.0
  - torch
  
Includes cli-tool for segmenting file/directory of files to sentences
"""

__author__ = "Max Strandén"
__version__ = "0.1.0"
__license__ = "MIT"

import argparse
import logging
from pathlib import Path

import pandas as pd
from PyPDF2 import PdfReader
import torch
from trankit import Pipeline
    
    
def pdf2text(file: Path) -> str:
    """Extract text from pdf file
    
    Read in pdf file and retun text as a string
    """
    reader = PdfReader(file)
    pages = [page.extract_text() for page in reader.pages]
    text = ''.join(pages)
    if text != '':
        return text
    else:
        logging.warning(f'Empty text. Maybe OCR document instead. Returning None.')
        return None
    
def segment_sentences(pipeline, text: str) -> list[str]:
    """Segmentation of sentences
    
    Takes in a single string (document) and returns a list of strings, one list element per sentence
    """
    if text is not None:  # pdf to text transformation fails for scanned documents and returns None
        sentences = pipeline.ssplit(text)
        return [sentence.get('text') for sentence in sentences.get('sentences')]
    else:
        logging.warning(f'Empty string. Returning None.')
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
    
    
def cli_args():
    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument("input", 
                        metavar="<file> OR <directory>",
                        help=("Input data. Supported formats: txt, pdf. If a directory given, all files inside will be processed."), 
                        type=str)
                        
    parser.add_argument("sentencefile", 
                        metavar="<text file>",
                        help=("Output text file with all sentences seperated by newlines"), 
                        type=str)
                        
    parser.add_argument("-c", "--cache_dir", 
                        metavar="<path to dir>",
                        help=("location to download models"), 
                        type=str, default='./cache/trankit')
                        
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
    
    
def main():
    
    args = cli_args()
    INPUT = Path(args.input)
    SENTENCEFILE = Path(args.sentencefile)
    CACHE_DIR = Path(args.cache_dir)
    VERBOSE = args.verbose
    
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
        
        
    if not torch.cuda.is_available():
        logging.warning('CUDA is not available')
        
    p = Pipeline('finnish', gpu=True, cache_dir=CACHE_DIR)
        
    if INPUT.is_file():
        logging.info(f'{INPUT.name} is file')
        
        logging.info(f'Extracting text from pdf...')
        text = pdf2text(INPUT)
        if text is None:
            logging.warning(f'No text found in {INPUT.name}. Exiting...')
            return None
        logging.info(f'Segmenting sentences from text...')
        sent = segment_sentences(p, text)
        sentences = pd.DataFrame({'doc': INPUT.name, 'nro': range(len(sent)), 'sentence': sent})
        
        logging.info(f'Writing csv of size: {sentences.shape[0]}.')
        sentences.to_csv(SENTENCEFILE, sep=';', encoding='utf-8')
        logging.info(f'Finished.')
    elif INPUT.is_dir():
        logging.info(f'{INPUT.name} is directory')
        pdfs = [pdf for pdf in INPUT.glob('**/*.pdf') if pdf.is_file()]
        logging.info(f'Found in total {len(pdfs)} files.')
        
        for pdf in pdfs:
            logging.info(f'Processing file {pdf.name}...')
            text = pdf2text(pdf)
            if text is None:
                logging.warning(f'Found no text in {pdf.name}. Skipping...')
                continue
            sent = segment_sentences(p, text)
            if sent is not None:
                sentences = pd.DataFrame({'doc': pdf.name, 'nro': range(len(sent)), 'sentence': sent})
                if 'sentences_all' in locals():
                    sentences_all = pd.concat([sentences_all, sentences], ignore_index=True)
                else:
                    sentences_all = pd.DataFrame({'doc': pdf.name, 'nro': range(len(sent)), 'sentence': sent})
        logging.info(f'Writing csv of size: {sentences_all.shape[0]}.')        
        sentences_all.to_csv(SENTENCEFILE, sep=';', encoding='utf-8')
        logging.info(f'Finished')