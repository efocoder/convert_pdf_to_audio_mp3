from django.shortcuts import render, redirect
from .forms import PDFForm
from gtts import gTTS
from datetime import datetime
import os

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO

import cloudinary
import cloudinary.uploader


def home(request):
    audio_url = {}
    if request.POST and request.FILES:
        form = PDFForm(request.POST, request.FILES)
        if form.is_valid():
          link =  handle_pdf(request.FILES['pdf_file'])
          print("MY MP3 FILE => ", link)
          audio_url = link
    else:
        form = PDFForm()

    context = {
        'form': form,
        'audio_url': audio_url.get('url'),
        'public': audio_url.get('public_id')
    }
    return render(request, 'index.html', context)



def handle_pdf(pdf_file):

    print('############################')
    print(pdf_file)
    print('##########################')

    resource_manager = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(resource_manager, retstr, codec=codec, laparams=laparams)
    # fp = open(pdf_file, 'rb')
    interpreter = PDFPageInterpreter(resource_manager, device)
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
    # give name to mp3
    return  convert_to_mp3(text)



def convert_to_mp3(text):
    the_mp3 = gTTS(text=text, lang='en')
    now = datetime.now()
    today = now.strftime("%d_%m_%Y_%H:%M:%S")
    filename = "files/"+today+".mp3"
    the_mp3.save(filename)


    cloudinary.config(
                cloud_name = 'deurbvxwp',  
                api_key = '368636563326952',  
                api_secret = 'sXNEaXFV1iQAk-Jr8WFUgdzBLII'  
                )
    cloud =  cloudinary.uploader.upload(filename, resource_type='raw')     
    print(cloud) 


     
    if cloud:
        audio_link = {
                        'public_id': cloud.get('public_id'),
                        'url': cloud.get('secure_url')
                    }
        os.remove(filename)

    return audio_link


def download(request):
    link = request.GET['link']
    print("THIS IS THE LINK +++>", link)
        
    return redirect('home')