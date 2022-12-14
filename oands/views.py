# import cloudinary.uploader
# from django.shortcuts import render
#
# # import pytesseract to convert text in image to string
# import pytesseract
# # import summarize to summarize the ocred text
# #from summarizer import summarizer
#
# from .forms import ImageUpload
# import os
#
# # import Image from PIL to read image
# from PIL import Image
# from django.conf import settings
from urllib import request

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from pytesseract import pytesseract
from rest_framework.decorators import api_view

import json
import urllib.request
from io import BytesIO
from PIL import Image
# from django.http import HttpRequest as rq

import time
# file='https://firebasestorage.googleapis.com/v0/b/ocr-test2-9b5be.appspot.com/images%2Fexxx.png?alt=media'
# file2 = 'https://firebasestorage.googleapis.com/v0/b/ocr-test2-9b5be.appspot.com/o/images%2Fexxx.png?alt=media&token=018185c4-b4d7-4ae6-8bb4-1bc127d55da0'
# storage = firebase.storage()
import sys


# Create your views here.

# connect with firebase

@api_view(['GET', 'POST'])
def index(request):
    if request.method == 'POST':
        return index2(request)


def index2(request):
    text = ""
    message = ""
    eng_to_kor = ""
    request_msg = ""
    img_msg = ""
    error = ""
    text2 = ""
    # if request.method == 'POST':
    # form = ImageUpload(request.POST, request.FILES)
    # if form.is_valid():
    try:
        request_msg = request.data['image']
        img = img_open(request_msg)
        img_msg = str(img)
        text = pytesseract.image_to_string(img, lang='kor+eng')
        text = text.encode("ascii", "ignore")
        text = text.decode()
        text2 = Summerization(text)
    except Exception as e:
        message = "check your filename and ensure it doesn't have any space or check if it has any text"
        error = str(e)

        # form.save()
        # image = image.name
        # path = settings.MEDIA_ROOT
        # pathz = path + "/images/" + image
        # image=request.POST.get('picture')
        # image=request.FILES['image']
        # print(requests.data['image'])
        # request_msg=request.data

        # img=img_open(request.data['image'])
        # text = pytesseract.image_to_string(img, lang='kor+eng')
        # text = text.encode("ascii", "ignore")
        # text = text.decode()

        #     # translate eng to kor through Papago API
        #     client_id = "7cyuDLUY3kSNzmFs_i88" # 개발자센터에서 발급받은 Client ID 값
        #     client_secret = "NMYcZYMSNp" # 개발자센터에서 발급받은 Client Secret 값
        #     encText = urllib.parse.quote(text)
        #     data = "source=en&target=ko&text=" + encText
        #     url = "https://openapi.naver.com/v1/papago/n2mt"
        #     request = urllib.request.Request(url)
        #     request.add_header("X-Naver-Client-Id",client_id)
        #     request.add_header("X-Naver-Client-Secret",client_secret)
        #     response = urllib.request.urlopen(request, data=data.encode("utf-8"))
        #     rescode = response.getcode()
        #
        #     if(rescode==200):
        #         response_body = response.read()
        #         result=response_body.decode('utf-8')
        #         d=json.loads(result)
        #         eng_to_kor = d['message']['result']['translatedText']
        #         # print(response_body)
        #         # print(eng_to_kor)
        #     else:
        #         eng_to_kor = "error code: "+rescode
        #
        #     # Summary (0.1% of the original content).
        #     # summarized_text = summarizer.summarize('',text, count=2)
        #     # os.remove(pathz)
        # except:
        #     message = "check your filename and ensure it doesn't have any space or check if it has any text"

    context = {
        'text': text,
        'text2' : text2,
        'message': message,
        'img_msg': img_msg,
        # 'eng_to_kor': eng_to_kor,
        'request_msg': request_msg,
        'error': error
    }
    # get(context)
    # return render(request, 'formpage.html', context)
    return JsonResponse(context)


# def get(context):
#     return JsonResponse(context)

def img_open(imgUrl):
    # request.urlopen()
    res = request.urlopen(imgUrl).read()
    # Image open
    img = Image.open(BytesIO(res))
    return img


from konlpy.tag import Okt
from typing import List
from lexrankr import LexRank


# import json

class OktTokenizer:
    okt: Okt = Okt()

    def __call__(self, text: str) -> List[str]:
        tokens: List[str] = self.okt.pos(text, norm=True, stem=True, join=True)
        return tokens


def Summerization(text):
    # 1. init using Okt tokenizer
    mytokenizer: OktTokenizer = OktTokenizer()
    lexrank: LexRank = LexRank(mytokenizer)
    # text = ""

    # 2. summarize (like, pre-computation)
    lexrank.summarize(text)

    summerization = []

    # 3. probe (like, query-time)
    summaries: List[str] = lexrank.probe()
    for summary in summaries:
        summerization.append(summary)

    return summerization
