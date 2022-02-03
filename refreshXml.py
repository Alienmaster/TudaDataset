# -*- coding: utf-8 -*-

# Copyright 2022 Hamburger Informatik Technologie-Center e.V. (HITeC) (author: Robert Geislinger)
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
import xml.etree.ElementTree as ET

cleaned = {}
raw = {}

def import_cleaned_sentences(cFile, rFile):

    with open (cFile, "r") as cF:
        for line in cF:
            cln = line.split(" ", 1)[0]
            cText = line.split(" ", 1)[1]
            cleaned[cln] = cText.split("\n")[0]

    with open (rFile, "r") as rF:
        for line in rF:
            rln = line.split(" ", 1)[0]
            rText = line.split(" ", 1)[1]
            raw[rln] = rText.split("\n")[0]


    for folder in ['train/','test/','dev/']:
        for f in os.listdir(folder):
            if f.endswith('xml'):
                print(f)
                mytree = ET.parse(folder + f)
                myroot = mytree.getroot()
                sentence_id = ""
                for sid in myroot.iter('sentence_id'):
                    sentence_id = sid.text
                for s_old in myroot.findall('sentence'):
                    myroot.remove(s_old)
                for sc_old in myroot.findall('cleaned_sentence'):
                    myroot.remove(sc_old)
                if sentence_id:
                    myroot.insert(6, (ET.fromstring("<cleaned_sentence>" + cleaned[sentence_id] + "</cleaned_sentence>")))
                    myroot.insert(6, (ET.fromstring("<sentence>" + raw[sentence_id] + "</sentence>")))

                if args.dummy:
                    mytree.write(folder + f + "D", encoding='utf-8', xml_declaration=True)
                else:
                    mytree.write(folder + f, encoding='utf-8', xml_declaration=True)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Reads the sentence_id in the xml files ' 
                            'and (over)writes the sentence (raw and cleaned) into each xml')
    parser.add_argument('-c', '--cleanInput', dest='cFile', 
                            help='Process the clean Sentences (defaults to: SentencesAndIDs.cleaned.txt)', type=str, default = 'SentencesAndIDs.cleaned.txt')
    parser.add_argument('-r', '--rawInput', dest='rFile', 
                            help='Process this input file (defaults to: SentencesAndIDs.raw.txt)', type=str, default = 'SentencesAndIDs.raw.txt')
    parser.add_argument('-d', '--dummy', dest='dummy', 
                            help='Writes instead of .xml files xmlD files (for testing purposes)', type=bool, default = False)
        
    args = parser.parse_args()
    import_cleaned_sentences(args.cFile, args.rFile)
