"""Convert conll-u files to one doc per line style

This cli converts conll-u files to more widely supported formats.
Many text processing tools except input to be text format with one 
document per line.

Output format:

"""

import argparse
import logging

from io import open
from conllu import parse_incr, parse
from pathlib import Path


def cli_args():
    parser = argparse.ArgumentParser(description=__doc__, prog="conllu2doc")
    
    parser.add_argument("path", type=str, help="input file")
    
    parser.add_argument("--upos", type=str, nargs="*", 
                        help="Filter by upostags")
                        
    parser.add_argument(
     "-v",
     "--verbose",
     action="count",
     default=0,
     help="Verbosity (-v, -vv, etc)")

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
    
#def conllu_reader():
    
#def remove_stopwords(rm_names, rm_numerals):


class ConlluReader:
    def __init__(self, path, **kwargs):
        self.path = path
        self._kwargs = kwargs
        logging.debug("Initialize ConlluReader with %s and %s", path, kwargs)
    
    def __enter__(self):
        logging.debug("Entering with statement")
        self.file_obj = open(self.path, mode='r', **self._kwargs)
        return self.file_obj
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.file_obj:
            logging.debug("Exiting with statement")
            self.file_obj.close()
        
    def __iter__(self):
        for tokenlist in parse_incr(self):
            yield tokenlist
        
    #def __next__(self):
    #    tokenlist = self.next()
    #    if tokenlist is not None:
    #        return tokenlist
    #    else:
    #        raise StopIteration
        

def cli():
    args = cli_args()
    
    log_config(args.verbose)
    logging.debug(args)
    
    #data = open(args.path, "r", encoding="utf-8")
    #
    #for tokenlist in parse_incr(data):
    #    if args.upos is not None:
    #        tokenlist = tokenlist.filter(upos=lambda upo: upo in args.upos)
    #    for sentence in tokenlist:
    #        print("<" + sentence["lemma"], end="> ")
    with ConlluReader(args.path, encoding='utf-8') as data:
        for tokenlist in parse_incr(data):
        #for tokenlist in data:
            logging.debug("tokenlist: %s", tokenlist)
            if args.upos is not None:
                tokenlist = tokenlist.filter(upos=lambda upo: upo in args.upos)
            for sentence in tokenlist:
                print("<" + sentence["lemma"], end="> ")
