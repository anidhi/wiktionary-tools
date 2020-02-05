#!/usr/bin/python3

from bs4 import BeautifulSoup
from pathlib import Path
import sys,argparse


def getLanguageId(language_file, language):
    language_id = ""
    g = [line.rstrip('\n') for line in open(language_file)]
    for i in range(len(g)):

        current = g[i].split()
        length = len(current)
        langid = current[length-1]

        current = g[i].rsplit('\t', 1)[0]

        if current == language:
            language_id = langid
    return language_id


parser = argparse.ArgumentParser()
parser.add_argument('language', help="What is the language ? ", default="Spanish")
args = parser.parse_args()
language = args.language

wordPOSLink = open((language + "_WordPOSLink.txt"), 'w')
wordNounLink = open((language + "_Noun.txt"), 'w')
wordAdjectiveLink = open((language + "_Adjective.txt"), 'w')
wordVerbLink = open((language + "_Verb.txt"), 'w')

langid = getLanguageId("LanguageISOCodes.txt", language)

pathlist = Path("candidate_pages/" + language).glob('**/*.html')
for path in pathlist:
    path_in_str = str(path)

    with open(path_in_str, "r") as f:
        contents = f.read()
        soup = BeautifulSoup(contents, 'lxml')

        for tag in soup.find_all("strong", lang=langid):
            a = tag.previous_element
            try:
                text = a.get_text()
            except:
                print(a)
            b = a.find_previous()
            pos = b.get_text()

            # To just print the HTML in place of text just replace the third field 'text' with the variable a
            # in the print statements.
            print("{0}\t{1}\t{2}".format(tag.text, pos, text), file=wordPOSLink)
            
            if pos == "Noun":
                print("{0}\t{1}\t{2}".format(tag.text, pos, text), file=wordNounLink)
            if pos == "Adjective":
                print("{0}\t{1}\t{2}".format(tag.text, pos, text), file=wordAdjectiveLink)
            if pos === "Verb":
                print("{0}\t{1}\t{2}".format(tag.text, pos, text), file=wordVerbLink)
wordPOSLink.close()
wordNounLink.close()
wordAdjectiveLink.close()
wordVerbLink.close()
