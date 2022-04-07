# bib2
#
# Quick & dirty python script to parse bibtex into different formats.


MYNAME='FooFooFoo'
#MYNAME='Emanuel Regnath'
#MYNAME='Sebastian Steinhorst'

BIB_FOLDER='./publications/bib/'


BIB_URL='https://emanuel.regnath.info/bib/'
PDF_URL='https://emanuel.regnath.info/publications/'





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


def parseBibFile( fileName ):
    text = readBibFile( fileName )  
    entries = splitAndParse(text)
    return entries


def writeOutput( fileName, text ): 
    output = open(fileName, 'w+')
    output.write(text)
    output.close()



def print_usage():
    print("""
Usage: python bib2.py FORMAT BIBFILE [LOCATION]
    - FORMAT= raw|bib|html|toml|rtf
    - LOCATION="./" (default)
""")
    


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

lsEntries = 'article|book|inbook|inproceedings|incollection|manual|misc|techreport|standard|patent'
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
    
    for bibkey in lsKeys:
        entry[bibkey] = deTexify(getBibKey(bibkey, text))

    return entry

def parseAllEntries( textlist ):
    entries = []
    for match in textlist:
        bibtext = match
        #print(bibtext)
        entry_dict = parseEntry(bibtext)
        entries.append(entry_dict)
    return entries


def splitAndParse( text ):
    textlist = split2entries(text)
    entries = parseAllEntries( textlist )
    return entries






# ===========================================================
# Convert to HTML
# ===========================================================
HTML='''
  <ul class="pub-list fa-ul lh-11">
    {entries}
  </ul>
'''

ENTRY_HTML='''
    <li>
      <i class="fa fa-li fa-file-text-o"></i>
      <div class="pub-list-item">
        <span>{title}</span>
        <div class="pub-authors"><small>{author}</small></div>
        <div class="pub-publisher"><small>{publisher}</small></div>
        {buttons}
      </div>
    </li>
'''

ENTRY_HTML_SIMPLE='''
    <li><span><b>{title}</b></span></br>
        {author}</br>
        {publisher}</br>
        {buttons}
    </li>
'''



#BUTTON_HTML='<div class="pub-buttons">{buttons}</div>'
BUTTON_HTML='{buttons}'


def entry2html(entry):
    html = ENTRY_HTML_SIMPLE

    authorstring = entry['author'].replace(' and ', ', ').replace(MYNAME, '<strong>'+MYNAME+'</strong>')

    if entry['pubtype'] in ["inproceedings"]:
        publisherstring = entry['booktitle']+', '+entry['location']+', '+entry['year']
    elif entry['pubtype'] in ["article"]:
        publisherstring = entry['journal']+', '+entry['year']
    elif entry['pubtype'] in ["book"]:
        publisherstring = entry['publisher']+', '+entry['year']
    elif entry['pubtype'] in ["misc", "techreport"]:
        publisherstring = ""
        if entry['booktitle'] != "": 
            publisherstring = entry['booktitle']
        elif entry['note'] != "": 
            publisherstring = entry['note']
        if entry['type'] != "": publisherstring += ", "+entry['type']
        if entry['year'] != "": publisherstring += ", "+entry['year']
    else:
        publisherstring=""

    publisherstring = publisherstring.replace(', , ', ', ')


    filename = entry['entrykey']

    # title string
    if entry['doi'] != "":
        #print(entry)
        titlestring = '<a href="https://dx.doi.org/{doi}">{title}</a>'.format(doi=entry['doi'], title=entry['title'])
    elif entry['isbn'] != "":
        titlestring = ' <a href="https://dx.doi.org/{isbn}">{title}</a>'.format(isbn=entry['isbn'], title=entry['title'])
    elif entry['url'] != "" and entry['url'][-4:] != ".pdf":
        titlestring = ' <a href="{url}">{title}</a>'.format(url=entry['url'], title=entry['title'])
    else:
        #print(entry['url'])
        titlestring = '<span>{title}</span>'.format(title=entry['title'])

    # buttonstring
    if entry['url'] != "" and entry['url'][-4:] == ".pdf":
        buttonstring = '<a href="{url}">[PDF]</a> <a href="{bibfolder}{filename}.txt">[BibTeX]</a>'.format(url=entry['url'], bibfolder=BIB_URL, filename=filename)
    else:
        buttonstring = '<a href="{bibfolder}{filename}.txt">[BibTeX]</a>'.format(bibfolder=BIB_URL, filename=filename)
    buttonhtml = BUTTON_HTML.format(buttons=buttonstring)



    html = html.format(title=titlestring, author=authorstring, publisher=publisherstring, buttons=buttonhtml)
    return html


def entries2html(entries):
    html = HTML
    entryhtml = ""
    for entry in entries:
        #print(entry)
        entryhtml += entry2html(entry)
    html = html.format(entries=entryhtml)
    return html



def inject2Html( fileName, html):
    text = readInputFile(fileName)
    text = text.replace('\{\{% bibliography \}\}', html)
    writeOutput( fileName, text )




# ===========================================================
# Convert to RTF 
# ===========================================================
RTF_TEMPLATE='''
\\par\\b {title}\\b0
\\par {author}
\\par {publisher}
\\line
'''

def entry2rtf(entry):
    authorstring = entry['author'].replace(' and ', ', ').replace(MYNAME, '\\b '+MYNAME+'\\b0 ')
    titlestring = entry['title']

    if entry['pubtype'] in ["inproceedings"]:
        publisherstring = entry['booktitle']+', '+entry['location']+', '+entry['year']
    elif entry['pubtype'] in ["article"]:
        publisherstring = entry['journal']+', '+entry['year']
    elif entry['pubtype'] in ["book"]:
        publisherstring = entry['publisher']+', '+entry['year']
    else:
        publisherstring=""


    rtf = RTF_TEMPLATE.format(title=titlestring, author=authorstring, publisher=publisherstring)   # url_pdf=url_pdf, url_doi=entry['doi']
    return rtf



# ===========================================================
# Convert to TOML (for Hugo)
# ===========================================================
TOML_TEMPLATE='''
+++
title = "{title}"
authors = [{author}]
publication = "{publisher}"
date = "{date}"
publication_types = ["{pubtype}"]

url_pdf = "{url_pdf}"
url_bibtex = "/res/bib/{bibkey}.txt"
url_doi = "{url_doi}"
+++
'''

def entry2toml(entry):
    authorstring = entry['author'].replace(' and ', ', ').replace(MYNAME, '**'+MYNAME+'**')
    titlestring = entry['title']

    if entry['pubtype'] in ["inproceedings"]:
        publisherstring = entry['booktitle']
        pubtypestr = '1'
    elif entry['pubtype'] in ["article"]:
        publisherstring = entry['journal']
        pubtypestr = '2'
    else:
        publisherstring=""
        pubtypestr = '1'

    datestr = entry['year']+"-"+entry['month']+"-"+entry['day']

    url_pdf = ""
    if entry['url'] != "" and entry['url'][-4:] == ".pdf":
        url_pdf = entry['url']


    toml = TOML_TEMPLATE.format(title=titlestring, author=authorstring, publisher=publisherstring, date=datestr, pubtype=pubtypestr, url_pdf=url_pdf, bibkey=entry['entrykey'], url_doi=entry['doi'])
    return toml



# ===========================================================
# Convert to raw text
# ===========================================================

RAW_TEMPLATE='{author}: “{title}”, {publisher}{location}{year}{doi}.'

def entry2raw(entry):
    titlestr = entry['title']

    authorstr="ERROR"
    if entry['author'] != "":
        authorstr=entry['author'].replace(' and ', ', ')
    elif entry['institution'] != "":
        authorstr=entry['institution']

    pubstr="ERROR"
    if entry['booktitle'] != "":
        pubstr = "In: "+entry['booktitle']
    elif entry['journal'] != "":
        pubstr = entry['journal']

    locstr=entry['location']
    if locstr != "": locstr = ", "+locstr

    yearstr=entry['year']
    if yearstr != "": yearstr = ", "+yearstr

    doistr=""
    if entry['doi'] != "": 
        doistr = ", "+"DOI: https://doi.org/{}".format(entry['doi'])

    raw = RAW_TEMPLATE.format(title=titlestr, author=authorstr, publisher=pubstr, location=locstr, year=yearstr, doi=doistr)
    return raw    






# ===========================================================
# Convert to individual bib/txt files
# ===========================================================

def split2bibtex( folder, text ):
    textlist = split2entries(text)
    for text in textlist:
        entry = parseEntry(text)
        filename=entry['entrykey']
        writeOutput(folder+filename+".txt", text)









# Main Program
#############################################
import fileinput
import sys
import os
import re



# check arguments
args = sys.argv[1:]
if not len(args) in [2, 3]:
    print_usage()
    sys.exit(0)

print("Starting Conversion")



# run script
folder = "./"
if len(args) == 3:
    folder = args[2]
    if folder[-1] != "/": folder += "/"

infile = args[1]
outformat = args[0]



if outformat == "html":
    entries = parseBibFile(infile)
    html = entries2html( entries )
    #print(html)
    writeOutput(folder+"publications.html", html)

elif outformat == "bib":
    text = readBibFile(infile)
    split2bibtex(folder, text) 


elif outformat == "raw":
    entries = parseBibFile(infile)
    raw = ""
    for idx, entry in enumerate(entries):
        raw += "[{}] ".format(idx+1) + entry2raw(entry) + "\n\n"
    print(raw)
    writeOutput(folder+"publications.txt", raw)


elif outformat == "rtf":
    entries = parseBibFile(infile)
    rtf = '{\\rtf1\n'
    for entry in entries:
        rtf += entry2rtf(entry)
    rtf += '}'
    writeOutput(folder+"publications.rtf", rtf)



elif outformat == "toml":
    entries = parseBibFile(infile)
    for entry in entries:
        toml = entry2toml(entry)
        print(toml)
        writeOutput(folder+entry['entrykey']+".md", toml)

else:
    print_usage()



