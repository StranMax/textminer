
from pathlib import Path

from textminer import textprocessor

import pytest
from trankit import Pipeline

@pytest.fixture(scope='module')
def test_string():
    file = Path("tests/integration/fixtures/test_abstract.txt")
    with open(file, 'r', encoding = 'utf-8') as f:
        text = f.read()
    assert len(text) == 3209, f'Expected string of 3209 characters, received {len(text)} characters'    
    return text

@pytest.fixture(scope='module')
def test_pipeline():
    p = Pipeline('finnish', gpu=True)
    return p
    
def test_segment_sentences(test_pipeline, test_string):
    sentences = textprocessor.segment_sentences(test_pipeline, test_string)
    assert len(sentences) == 22, f'Number of elements does not match number of sentences. Expected 22, received {len(sentences)}'
    
def test_tokenization(test_pipeline, test_string):
    sentences = textprocessor.segment_sentences(test_pipeline, test_string)
    tokens = textprocessor.tokenize(test_pipeline, sentences)
    assert len(sentences) == 22, f'Number of elements does not match number of tokenized sentences. Expected 22, received {len(tokens)}'
    
def test_lemmatization(test_pipeline, test_string):
    sentences = textprocessor.segment_sentences(test_pipeline, test_string)
    tokens = textprocessor.tokenize(test_pipeline, sentences)
    lemmas = textprocessor.lemmatize(test_pipeline, tokens)
    assert len(lemmas) == 22, f'Number of elements does not match number of lemmatized sentences. Expected 22, received {len(lemmas)}'