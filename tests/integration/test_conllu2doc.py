
from pathlib import Path

import pytest

from textminer.conllu2doc import cli()

@pytest.fixture
def conllu_data():
    file = Path("tests/integration/fixtures/test_conllu_file.conllu")
    with open(file) as f:
        data = f.readlines()
        
    return data
        
def test_firstline_conllu_data(conllu_data):
    assert conllu_data[0] == '# newdoc\n'
    
#def test_conllu2doc():
    
    