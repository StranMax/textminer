
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
def test_pipeline(test_string):
    p = Pipeline('finnish', gpu=True)
    sentences = textprocessor.segment_sentences(p, test_string)
    tokens = textprocessor.tokenize(p, sentences)
    filtered_tokens = textprocessor.filter_posdep(p, tokens, ['NOUN', 'VERB', 'ADJ'])
    lemmas = textprocessor.lemmatize(p, tokens)
    filtered_lemmas = textprocessor.lemmatize(p, filtered_tokens)
    return {'sentences': sentences, 'tokens': tokens,'lemmas': lemmas, 'filtered_tokens': filtered_tokens, 'filtered_lemmas': filtered_lemmas}
    
def test_segment_sentences_len(test_pipeline):
    sentences = test_pipeline.get('sentences')
    assert len(sentences) == 22, f'Number of elements does not match number of sentences. Expected 22, received {len(sentences)}'
    
def test_segment_sentences_first_elem(test_pipeline):
    sentences = test_pipeline.get('sentences')
    true_string = '"Arviointi koskee valtioneuvoston ilmasto- ja energiapoliittista tulevaisuusselontekoa, joka annettiin eduskunnalle syksyllä 2009.'
    assert sentences[0] == true_string, f'Expected {true_string}, received {sentences[0]}'
    
def test_tokenize_len(test_pipeline):
    tokens = test_pipeline.get('tokens')
    assert len(tokens) == 22, f'Number of elements does not match number of tokenized sentences. Expected 22, received {len(tokens)}'
    
def test_tokenize_first_elem(test_pipeline):
    tokens = test_pipeline.get('tokens')
    true_tokens = ['"', 'Arviointi', 'koskee', 'valtioneuvoston', 'ilmasto-', 'ja', 'energiapoliittista', 'tulevaisuusselontekoa', ',', 'joka', 'annettiin', 'eduskunnalle', 'syksyllä', '2009', '.']
    assert tokens[0] == true_tokens, f'Expected {true_tokens}, received {tokens[0]}'
  
def test_filter_posdep_len(test_pipeline):
    filtered_tokens = test_pipeline.get('filtered_tokens')
    assert len(filtered_tokens) == 22, f'Number of elements does not match number of tokenized sentences. Expected 22, received {len(filtered_tokens)}'
    
def test_filter_posdep_first_elem(test_pipeline):
    filtered_tokens = test_pipeline.get('filtered_tokens')
    true_filtered_tokens = ['Arviointi', 'koskee', 'valtioneuvoston', 'ilmasto-', 'energiapoliittista', 'tulevaisuusselontekoa', 'annettiin', 'eduskunnalle', 'syksyllä']
    assert filtered_tokens[0] == true_filtered_tokens, f'Expected {true_filtered_tokens}, received {filtered_tokens[0]}'
  
def test_lemmatization_len(test_pipeline):
    lemmas = test_pipeline.get('lemmas')
    assert len(lemmas) == 22, f'Number of elements does not match number of lemmatized sentences. Expected 22, received {len(lemmas)}'
    
def test_lemmatization_first_elem(test_pipeline):
    lemmas = test_pipeline.get('lemmas')
    true_lemmas = ['"', 'arviointi', 'koskea', 'valtio#neuvosto', 'ilmasto', 'ja', 'energia#poliitti', 'tulevaisselon#selonteko', ',', 'joka', 'antaa', 'edus#kunta', 'syksy', '2009', '.']
    assert lemmas[0] == true_lemmas, f'Expected {true_lemmas}, received {lemmas[0]}'
    
def test_filtered_lemmatization_len(test_pipeline):
    filtered_lemmas = test_pipeline.get('filtered_lemmas')
    assert len(filtered_lemmas) == 22, f'Number of elements does not match number of lemmatized sentences. Expected 22, received {len(filtered_lemmas)}'
    
def test_filtered_lemmatization_first_elem(test_pipeline):
    filtered_lemmas = test_pipeline.get('filtered_lemmas')
    true_filtered_lemmas = ['arviointi', 'koskea', 'valtio#neuvosto', 'ilmasto', 'energia#poliitti', 'tulevaisselon#selonteko', 'antaa', 'edus#kunta', 'syksy']
    assert filtered_lemmas[0] == true_filtered_lemmas, f'Expected {true_filtered_lemmas}, received {filtered_lemmas[0]}'