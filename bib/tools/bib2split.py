# bib2split
#
# Quick & dirty python script to split bibtex into individual files.
# Author: emanuel.regnath@tum.de

from pathlib import Path

# output folder for individual files
FOLDER = Path("./bib/ESI-Publications-Separated/")


# ===========================================================
# Input / Output
# ===========================================================

def readBibFile( fileName ):
    # read file
    fileBaseName, ext = os.path.splitext(fileName)
    if (ext != ".bib"):
        print ("Unknown file format: ", ext)
        sys.exit(1)
    text = readInputFile(fileName)
    return text


def writeOutput( fileName, text ): 
    output = open(fileName, 'w+')
    output.write(text)
    output.close()


def readInputFile( fileName ):
    # Open file as file object and read to string
    sourceFile = open(fileName,'r')

    # Read file object to string
    sourceText = sourceFile.read()

    # Close file object
    sourceFile.close()

    # return
    return sourceText


# ===========================================================
# Parsing
# ===========================================================

lsEntries = 'article|book|inbook|inproceedings|incollection|manual|misc|techreport|standard|patent|online'
lsKeys = ['author', 'title', 'booktitle', 'journal', 'year', 'month', 'day', 'location', 'institution', 'organization', 'number', 'type', 'note', 'pages', 'publisher', 'volume', 'url', 'doi', 'isbn']



reEntryLine = r'@('+lsEntries+')\s*\{(.+?),\s*\n'
reEntry = r'(@(?:'+lsEntries+')\s*\{.+?,\s*\n(?:\n|.)*?\n\s*\})\s*\n'




def getBibKey(keyname, text):
    match = re.search(r'(?<=\n)\s*'+keyname+r'\s*=\s*[\{\"](.+?)[\}\"]\s*(?:,\s*\n|\n\s*\})', text, re.IGNORECASE)
    if match != None:
        return match.group(1).strip()
    else:
        return ""


def deTexify(text):
    text = re.sub(r'\\\"\{?a\}?', 'ä', text)
    text = re.sub(r'\\\"\{?o\}?', 'ö', text)
    text = re.sub(r'\\\"\{?u\}?', 'ü', text)
    text = re.sub(r'\{(.*?)\}', r'\1', text)
    text = re.sub(r'--', r'–', text)
    return text


def split2entries(text):
    matches = re.findall(reEntry, text, re.IGNORECASE)
    return matches


def parseEntry(text):
    entry = {}
    matches = re.search(reEntryLine, text, re.IGNORECASE)
    entry['pubtype'] = matches.group(1).lower()
    entry['entrykey'] = matches.group(2).lower()
    entry['entrykey'] = entry['entrykey'].replace(":", "_")
    
    for bibkey in lsKeys:
        entry[bibkey] = deTexify(getBibKey(bibkey, text))

    return entry




# ===========================================================
# Convert to individual bib/txt files
# ===========================================================

def split2bibtex( folder, text ):
    textlist = split2entries(text)
    for text in textlist:
        entry = parseEntry(text)
        filename=entry['entrykey']
        filename += ".bib"
        writeOutput(Path(folder, filename), text)




# Main Program
#############################################
import fileinput
import sys
import os
import re


# check arguments
args = sys.argv[1:]

if len(args) != 1: print("Bibfile Missing.")
infile = args[0]

text = readBibFile(infile)
split2bibtex(FOLDER, text) 



