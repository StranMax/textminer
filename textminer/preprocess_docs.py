"""
Python script for preprocessing text documents

Follows Trankit workflow

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
                        help="path to output directory")
                        
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
    
    
class Docs:
    def __init__(self, path):
        self.paths = []
        self.read_docs(path)
        self.p = Pipeline('finnish', gpu=True)

        
    def read_docs(self, path):
        path = Path(path)
        if path.is_file():
            self.docs.append(path)
        elif path.is_dir():
            pdfs = path.glob('**/*.pdf')
            [self.paths.append(pdf) for pdf in pdfs if pdf.is_file()]
        
        logging.debug("Initialized Docs with paths: %s", self.paths)
        
    
    def pdf2text(self, parent: Path):
        dir = parent / Path('text_documents')
        if dir.exists():
            logging.warning(f'Directory {dir} exists! Using it anyway...')
        dir.mkdir(parents=True, exist_ok=True)
        
        for idx, file in enumerate(self.paths, start=1):
            outfile = Path(dir) / (Path(file).stem + '.txt')
            if not Path(file).exists() or outfile.exists():
                logging.info(f'[{idx:03d}] Skip pdf to text conversion: {file.name}')
                continue

            logging.info(f'[{idx:03d}] PDF to text conversion: {file.name}')
            reader = PdfReader(file)
            pages = [page.extract_text() for page in reader.pages]
        
            with open(outfile, 'w', encoding='utf-8') as f:
                f.writelines(pages)
                
            
    def segment_sentences(self, parent: Path):
        txt_files = [i for i in (parent/Path('text_documents')).glob('*.txt')]
        dir = parent / Path('sentences')
        if dir.exists():
            logging.warning(f'Directory {dir} exists! Using it anyway...')
        dir.mkdir(parents=True, exist_ok=True)
        
        if not torch.cuda.is_available():
            logging.warning('CUDA is not available')
        
        for idx, file in enumerate(txt_files, start=1):
            outfile = dir / (file.stem + '.pkl')
            if not file.exists() or outfile.exists():
                logging.info(f'[{idx:03d}] Skip sentence segmentation: {file.name}')
                continue
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    pages = f.readlines()
                    txt = '\n\n'.join(pages)
                    if len(txt) < 2:
                        logging.warning(f'[{idx:03d}] Empty text file: {file.name}')
                        continue
                
                logging.info(f'[{idx:03d}] Sentence segmentation: {file.name}')
                sentences = self.p.ssplit(txt)
                
                with open(outfile, "wb") as out:
                    pickle.dump(sentences, out)
        
            except Exception as e:
                logging.error(f'[{idx:03d}] Error with file: {file.name} -> {e}')
                continue
        
def main():
    """ Main entry point of the app """
    args = cli_args()
    # Command line arguments
    INPATH=args.inpath
    OUTPATH=args.outpath
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
    
    docs = Docs(INPATH)
    
    logging.debug(docs)
    
    docs.pdf2text(OUTPATH)
    docs.segment_sentences(OUTPATH)