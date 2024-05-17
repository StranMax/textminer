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

logging.basicConfig(
    format='[%(asctime)s] - [%(levelname)s] - %(message)s', 
    level=logging.DEBUG, 
    datefmt='%d-%b-%y %H:%M:%S'
    )

def cli_args():
    parser = argparse.ArgumentParser(description=__doc__, prog="conllu2doc")
    
    parser.add_argument("path", type=str, help="input file")
    
    parser.add_argument("--upos", type=str, nargs="*", 
                        help="Filter by upostags")

    return parser.parse_args()
    
    
def cli():
    args = cli_args()
    logging.debug(args)
    upos = [{"upos": upos} for upos in args.upos]
    logging.debug(upos)
    data = open(args.path, "r", encoding="utf-8")
    for tokenlist in parse_incr(data):
        for upo in upos:
            tokenlist = tokenlist.filter(**upo)
            for sentence in tokenlist:
                print(sentence["lemma"], end=", ")
