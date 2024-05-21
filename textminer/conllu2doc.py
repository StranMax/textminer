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
            loglevel = logging.MESSAGE
        case 3:
            loglevel = logging.DEBUG
            
    logging.basicConfig(
        format='[%(asctime)s] - [%(levelname)s] - %(message)s', 
        level=loglevel, 
        datefmt='%d-%b-%y %H:%M:%S'
    )
    
def cli():
    args = cli_args()
    log_config(args.verbose)
    logging.debug(args)
    
    upos = [{"upos": upos} for upos in args.upos]
    logging.debug(upos)
    data = open(args.path, "r", encoding="utf-8")
    for tokenlist in parse_incr(data):
        for upo in upos:
            tokenlist = tokenlist.filter(**upo)
            for sentence in tokenlist:
                print(sentence["lemma"], end=", ")

