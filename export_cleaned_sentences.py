# -*- coding: utf-8 -*-

# Copyright 2015 Language Technology, Technische Universitaet Darmstadt (author: Benjamin Milde)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse
import os
import codecs
import re
from bs4 import BeautifulSoup

def is_problematic(sentence,cleaned_sentence):
    return ((u'€' in sentence) or (u'Euro' in sentence) or (u'EUR' in sentence) #Euros
                or len([ch for ch in sentence if ch.isdigit()]) > 0 #Many digits
                or len([ch for ch in sentence if ch == '.']) > 1 #Many points
                or cleaned_sentence[0].islower() #Starts with lower case
                or ' null ' in cleaned_sentence #Java 'null' from maryfy
                #unresolved roman literals in cleaned sentence
                or (' I ' in cleaned_sentence) or (' II ' in cleaned_sentence) or (' III ' in cleaned_sentence)
                or (' V ' in cleaned_sentence) or (' VI ' in cleaned_sentence) or (' VII ' in cleaned_sentence)
                or (' VIII ' in cleaned_sentence) or (' IX ' in cleaned_sentence) or (' X ' in cleaned_sentence))

def export_cleaned_sentences(problematic_cases_only=False):
    sentences = {}
    cleaned_sentences = {}

    for folder in ['train/','test/','dev/']:
        for f in os.listdir(folder):
            if f.endswith('xml'):
                with codecs.open(folder + f,'r','utf-8') as xmlfile:
                    #remove urls
                    text = xmlfile.read()
                    #print text
                    #if '<url>' in text:
                    #    text = re.sub(r'<url>.*</url>', '', text)
                    #print text
                    soup = BeautifulSoup(text)
                    sentence = (soup.recording.sentence.string).strip()
                    cleaned_sentence = (soup.recording.cleaned_sentence.string).strip()
                    sentence_id = int((soup.recording.sentence_id.string).strip())

                    if sentence_id in cleaned_sentences:
                        assert(cleaned_sentences[sentence_id]) == cleaned_sentence
                    else:
                        if not problematic_cases_only or is_problematic(sentence,cleaned_sentence):
                            cleaned_sentences[sentence_id] = cleaned_sentence
                            sentences[sentence_id] = sentence
                            print sentence_id,cleaned_sentence

    with codecs.open('cleaned_sentences' + ('_sel' if problematic_cases_only else '') + '.txt','w','utf-8') as outfile:
        for key in sorted(cleaned_sentences.keys()):
            outfile.write(str(key)+' '+cleaned_sentences[key]+'\n')

    with codecs.open('sentences' + ('_sel' if problematic_cases_only else '') +'.txt','w','utf-8') as outfile:
        for key in sorted(sentences.keys()):
            outfile.write(str(key)+' '+sentences[key]+'\n')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Exports the cleaned sentences from all XML files in the corpus to a single XML file')
    parser.add_argument('-p', '--problematic-cases', dest='problematic_cases', help='Restrict the export to sentences with dates, numbers, difficult punctuation for better manual inspection of difficult cases of automatic sentence normalization', action='store_true', default=False)
    args = parser.parse_args()
    export_cleaned_sentences(args.problematic_cases)
