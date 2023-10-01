# This is a sample Python script.
import os.path

# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


from PyPDF2 import PdfReader, PdfWriter
import re
from colorama import init, Fore, Style
import sys

init()

def get_pdf_max_pages(pdf):
    with open(pdf, 'rb') as read_stream:
        pdf_reader = PdfReader(read_stream)
        totalPages = len(pdf_reader.pages)
    return totalPages

def pdf_extract(pdf, pages):
    """
    pdf: str | Path
    segments: [(start, end), {'start': int, 'end': int}]
    """
    pdf_writer = PdfWriter()  # we want to reset this when starting a new pdf

    with open(pdf, 'rb') as read_stream:
        pdf_reader = PdfReader(read_stream)
        for page_indices in pages:
            b1=page_indices[0] - 1
            b2=page_indices[1]
            print(Style.RESET_ALL+"  extracting pages in range "+ Fore.LIGHTYELLOW_EX+"[{},{}]".format(b1+1, b2)+Style.RESET_ALL)
            for idx in range(b1, b2):
                pdf_writer.add_page(pdf_reader.pages[idx])

    output_filename = pdf.replace(".pdf", "_new.pdf")
    with open(output_filename, "wb") as out:
        pdf_writer.write(out)
    print(Fore.LIGHTGREEN_EX + "SUCCESS:"+ Style.RESET_ALL+" output PDF file saved in "+output_filename)

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

def split_rangeString(_srange):
    # 2;5;2-8
    print("input ranges = " + _srange)
    retult=[]
    for _s in _srange.strip().replace(';', ',').split(','):
        _s=_s.strip()
        if _s.find('-') > -1:
            b1_string = _s.split('-')[0]
            try:
                b1=int(b1_string)
            except:
                b1 = 1
            b2_string = _s.split('-')[1]
            try:
                b2 = int(b2_string)
            except:
                b2 = MAX_PAGES
        else:
            b1 = int(_s)
            b2 = int(_s)
        if not 0 < b1 <= MAX_PAGES:
            raise Exception("page number ({}) must be between 1 and max_pages ({}) ".format(b1,MAX_PAGES))
        if not 0 < b2 <= MAX_PAGES:
            raise Exception("page number ({}) must be between 1 and max_pages ({})".format(b2, MAX_PAGES))
        if b1 > b2:
            raise Exception("range [{},{}] b1 must be < b2".format(b1, b2))

        retult.append((b1,b2))
        #print ("[{},{}]".format(b1,b2))
    return retult

def check_rangeSntax(s_range):
    if re.search("[^ 0-9;,-]", s_range):
        return False
    return True


#pdf_dir="E:/Chrome Downloads/"
#pdf_filename_root="Demande inscription Zeid BELHAJ BETTAIEB.pdf"
#pdf_filename=pdf_dir+pdf_filename_root
#pdf_extract(pdf_filename, [(1, 1)])

_exemple="1;5; -8; 4 -"

pdf_filename = ""
extract_expression = ""
i = 1
while i<len(sys.argv):
    #print("i={}; arg[i]={}".format(i,sys.argv[i]))
    if sys.argv[i] == '-i' and i+1<len(sys.argv):
        pdf_filename = sys.argv[i+1]
        i += 1

    if sys.argv[i] == '-e' and i+1<len(sys.argv):
        extract_expression = sys.argv[i+1]
        i += 1

    i += 1

#print("pdf_filename = " + pdf_filename)
#print("extract_expression = "+extract_expression)


if pdf_filename == "":
    pdf_filename = input(Fore.LIGHTWHITE_EX + "PDF file : "+Fore.GREEN)

if not os.path.isfile(pdf_filename):
    print(Fore.LIGHTRED_EX+"Error:"+Style.RESET_ALL+" file does not exist")
    exit(2)

if extract_expression == "":
    extract_expression=input(Fore.LIGHTWHITE_EX + 'Extract expression '+Style.RESET_ALL+'(example "{}") : '.format(_exemple)+Fore.GREEN)

if not check_rangeSntax(extract_expression):
    print(Fore.LIGHTRED_EX+"Syntax KO"+Style.RESET_ALL+" not allowed chars found in range expression")
    exit(3)

MAX_PAGES = get_pdf_max_pages(pdf_filename)
print(Style.RESET_ALL)
print("MAX PAGES = {}".format(MAX_PAGES))

try:
    pdf_extract(pdf_filename, split_rangeString(extract_expression))
except Exception as error:
    print(Fore.LIGHTRED_EX+"Error "+Style.RESET_ALL+str(error))
    exit(3)
