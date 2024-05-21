
import argparse
import os
from pathlib import Path
import subprocess

import pytest

#from textminer import conllu2doc
from textminer.conllu2doc import cli

@pytest.fixture(scope='module')
def first_sentence_conllu():
    return ("# newdoc\n"
            "# newpar\n"
            "# sent_id = 1\n"
            "# text = JULKINEN LIIKENNE JA ALUEIDEN KEHITYS – ESISELVITYS Joukkoliikenteen merkitys maaseudun kehittämisessä Liikenne- ja viestintäministeriö\n"
            "1	JULKINEN	JULKinEn	PROPN	_	Case=Nom|Number=Sing	2	amod	_	_\n"
            "2	LIIKENNE	liikenne	NOUN	_	Case=Nom|Number=Sing	0	root	_	_\n"
            "3	JA	ja	CCONJ	_	_	4	cc	_	_\n"
            "4	ALUEIDEN	alue	NOUN	_	Case=Gen|Number=Plur	5	nmod:poss	_	_\n"
            "5	KEHITYS	kehitys	NOUN	_	Case=Nom|Number=Sing	2	conj	_	_\n"
            "6	–	–	PUNCT	_	Case=Nom|Number=Sing	7	punct	_	_\n"
            "7	ESISELVITYS	esi#selvitys	NOUN	_	Case=Nom|Number=Sing	2	nmod	_	SpacesAfter=\\n\n"
            "8	Joukkoliikenteen	joukko#liikenne	NOUN	_	Case=Gen|Number=Sing	9	nmod:poss	_	_\n"
            "9	merkitys	merkitys	NOUN	_	Case=Nom|Number=Sing	7	nmod	_	_\n"
            "10	maaseudun	maa#seutu	NOUN	_	Case=Gen|Number=Sing	11	nmod:gobj	_	_\n"
            "11	kehittämisessä	kehittäminen	NOUN	_	Case=Ine|Derivation=Minen|Number=Sing	9	nmod	_	SpacesAfter=\\n\n"
            "12	Liikenne-	liikenne	NOUN	_	Case=Nom|Number=Sing	9	nmod:poss	_	_\n"
            "13	ja	ja	CCONJ	_	_	14	cc	_	_\n"
            "14	viestintäministeriö	viestintä#ministeriö	NOUN	_	Case=Nom|Number=Sing	12	conj	_	SpacesAfter=\\n\\n\n")

@pytest.fixture(scope='module')
def conllu_data():
    file = Path("tests/integration/fixtures/test_conllu_file.conllu")
    with open(file, encoding = 'utf-8') as f:
        data = f.readlines()
        
    return data
    
def test_conllu_reader(first_sentence_conllu, conllu_data):
    assert ''.join(first_sentence_conllu) == ''.join(conllu_data[0:18])
    

#def test_conllu2doc():
    #output = subprocess.check_output('conllu2doc.exe "tests/integration/fixtures/test_conllu_file.conllu" --upos "NOUN"', encoding='utf-8')  # encoding error!?
    
    #assert output == 'liikenne, alue, kehitys, esi#selvitys, joukko#liikenne, merkitys, maa#seutu, kehittäminen, liikenne, viestintä#ministeriö, esi#puhe, esi#selvitys, tarkoitus, alue, kehittäminen, tavoite, suhde, yhteis#kunta, liikenne, maa#seutu, sosiaali#toimi, koulu#toimi, kunta, rahoitus, joukko#liikenne,'
    
#@pytest.mark.parametrize('path', '"tests/integration/fixtures/test_conllu_file.conllu')
#@pytest.mark.parametrize('--upos', ['NOUN'])
#@pytest.mark.parametrize('--verbose', 0)
#def test_conllu2doc_nouns(monkeypatch, path, name_input):
#    with monkeypatch.context() as m:
#        m.setattr(sys, 'argv', [ sys.argv[0], '--animal', animal_input, '--name', name_input])
#        assert foo() == (animal_input)