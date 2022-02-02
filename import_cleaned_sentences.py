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

def import_cleaned_sentences(import_file):
    cleaned_sentences = {}
    
    with codecs.open(import_file,'r','utf-8') as infile:
        for line in infile:
            split = line.split(u' ')
            sentence_id = int(split[0])
            cleaned_sentence = line[len(str(sentence_id))+1:]
            cleaned_sentences[sentence_id] = cleaned_sentence.strip()

    changed = 0
    for folder in ['train/','test/','dev/']:
        for f in os.listdir(folder):
            if f.endswith('xml'):
                needs_write = False
                with codecs.open(folder + f,'r','utf-8') as xmlfile:
                    #remove urls
                    text = xmlfile.read()
                    soup = BeautifulSoup(text)
                    sentence = (soup.recording.sentence.string).strip()
                    cleaned_sentence = (soup.recording.cleaned_sentence.string).strip()
                    sentence_id = int((soup.recording.sentence_id.string).strip())

                    if sentence_id in cleaned_sentences and cleaned_sentences[sentence_id] != cleaned_sentence: 
                        changed += 1
                        substitute_sentence = cleaned_sentences[sentence_id]
                        print 'Changing', cleaned_sentence, 'to', substitute_sentence
                        text = re.sub(ur'<cleaned_sentence>.*</cleaned_sentence>', u'<cleaned_sentence>'
                                + substitute_sentence  + u'</cleaned_sentence>', text)
                        needs_write = True
                    
                if needs_write:
                    with codecs.open(folder + f,'w','utf-8') as outfile:
                        outfile.write(text)

    print 'Changed', changed, 'files'

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Imports the cleaned sentences ' 
                            '(single txt file) into all XML files in the corpus')
    parser.add_argument('-i', '--input-file', dest='inputfile', 
                            help='Process this input file (defaults to: cleaned_sentences_manual.txt)', type=str, default = 'cleaned_sentences_manual.txt')
        
    args = parser.parse_args()
    import_cleaned_sentences(args.inputfile)
