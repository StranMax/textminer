"""Convert conll-u files to one doc per line style

This cli converts conll-u files to more widely supported formats.
Many text processing tools except input to be text format with one 
document per line.

Output format: DOC: <LEMMA> <LEMMA> <LEMMA>...   

"""

import argparse
import concurrent.futures
import logging
import threading

from io import open
from concurrent.futures import ThreadPoolExecutor
from conllu import parse_incr, parse
from conllu.exceptions import ParseException
from pathlib import Path
from threading import Lock




def cli_args():
    parser = argparse.ArgumentParser(description=__doc__, prog="conllu2doc")
    #input_group = parser.add_mutually_exclusive_group(required=True)
    #input_group.add_argument("filepath", type=str, help="path to input file")
    #input_group.add_argument("dirpath", type=str, 
    #                         help="path to directory with conll-u files")
                             
    parser.add_argument("inpath", type=str, 
                        help="path to input file or directory with conllu files")
                        
    parser.add_argument("outpath", type=str, 
                        help="path to output text file")                    
    
    parser.add_argument("--upos", type=str, nargs="*", 
                        help=("Filter by Universal-Part-Of-Speechs tags. See all UPOS at:"
                              "https://universaldependencies.org/u/pos/index.html")
                       )
                        
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


class ConlluDocs:
    def __init__(self, path):
        self.paths = []
        #self.docs = {}
        self.read_docs(path)
        
    def read_docs(self, path):
        path = Path(path)
        if path.is_file():
            self.docs.append(path)
        elif path.is_dir():
            p = path.glob('**/*.conllu')
            [self.paths.append(x) for x in p if x.is_file()]
        
        logging.debug("Initialized ConlluDocs with paths: %s", self.paths)
   
    def conllu2lemma(self, upos):
        for path in self.paths:
            document = path.name
            lemmas = []
            with ConlluReader(path, encoding='utf-8') as tokenlists:
                try:
                    for tokenlist in tokenlists:
                        logging.debug("tokenlist: %s", tokenlist)
                        if upos is not None:
                            tokenlist = tokenlist.filter(upos=lambda upo: upo in upos)
                        for token in tokenlist:
                            lemmas.append(token.get("lemma"))
                except ParseException as e:
                        logging.warning("Encountered problem with tokenlist (doc: %s, len: %s):\n%s exception: %s", path.name, len(tokenlist), tokenlist, e)
            yield (document, lemmas)


class ConlluReader:
    def __init__(self, path, **kwargs):
        logging.debug("ConlluReader created with path: %s", path)
        self.path = path
        self._kwargs = kwargs
        logging.debug("Initialize ConlluReader with path: %s and kwargs: %s", path, kwargs)
    
    def __enter__(self):
        logging.debug("Entering context manager for: %s", self.path)
        self.file_obj = open(self.path, mode='r', **self._kwargs)
        return parse_incr(self.file_obj)
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.file_obj:
            logging.debug("Exiting context manager for: %s", self.path)
            self.file_obj.close()
    
    def __iter__(self):
        return self
    

class ConlluWriter:
    def __init__(self, path, **kwargs):
        logging.debug("ConlluWriter created with path: %s", path)
        self.path = path
        self._kwargs = kwargs
        logging.debug("Initialize ConlluWriter with path: %s and kwargs: %s", path, kwargs)
    
    def __enter__(self):
        logging.debug("Entering context manager for: %s", self.path)
        self.file_obj = open(self.path, mode='a', **self._kwargs)
        return self.file_obj
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.file_obj:
            logging.debug("Exiting context manager for: %s", self.path)
            self.file_obj.close()


def formatter(doc: dict, style='mallet'):
    assert style in ['mallet', 'gensim'], 'style must be one of ["mallet", "gensim"]'
    if style=='mallet':
        formatted = f"{doc.keys()}\t{doc.values()}"
    else:
        formatted = None
    return formatted
    

def cli():
    args = cli_args()
    
    log_config(args.verbose)
    logging.debug(args)
    
    docs = ConlluDocs(args.inpath)
    with ConlluWriter(args.outpath, encoding='utf-8') as f:
        for idx, doc in enumerate(docs.conllu2lemma(args.upos)):
            doc_name, lemmas = doc
            if len(lemmas) == 0: continue
            f.write(str(idx))
            f.write('\t')
            f.write(doc_name)
            f.write('\t')
            f.write(' '.join(lemmas))
            f.write('\n')
        
    
    
