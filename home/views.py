from django.http import HttpResponse
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from validate import clean_file
from .forms import PDFForm
import pdftotext
from tika import parser
from gtts import gTTS
import pdfplumber
import PyPDF2
from pdfminer.high_level import extract_text



from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO





def home(request):
    if request.POST and request.FILES:
        # print('THE FILE =?', request.FILES.get('pdf_file'))
        # print('THE POST=?', request.POST)
        form = PDFForm(request.POST, request.FILES)
        if form.is_valid():
           mp3 =  handle_pdf(request.FILES['pdf_file'])
           print("MY MP3 FILE => ", mp3.get_urls())
    else:
        form = PDFForm()

    return render(request, 'index.html', {'form': form})



def convert_to_mp3(text):
    the_mp3 = gTTS(text=text, lang='en')
    the_mp3.save("list_to_fr.mp3")

    return the_mp3


def handle_pdf(pdf_file):
    print('############################')
    print(pdf_file)
    print('##########################')

    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    # fp = open(pdf_file, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos = set()

    for page in PDFPage.get_pages(pdf_file, pagenos, maxpages=maxpages, password=password, caching=caching,
                                  check_extractable=True):
        interpreter.process_page(page)

    text = retstr.getvalue()
    print(text)

    # fp.close()
    device.close()
    retstr.close()
    return  convert_to_mp3(text)
