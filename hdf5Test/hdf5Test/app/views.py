"""
Definition of views.
"""

from django.shortcuts import render
from django.http import HttpRequest
from django.http import HttpResponse
from django.http import JsonResponse
from django.template import RequestContext
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt

import cv2
import datetime as dt
import h5py
import matplotlib.pyplot as plt
import matplotlib.pylab as plb
import numpy as np
import json
import http.client, urllib.request, urllib.parse, urllib.error, base64
import time
import os
from glob import glob
import fnmatch
import requests 
from bs4 import BeautifulSoup
import psycopg2 as pg2 #DB연동
from django.core.files.storage import FileSystemStorage #파일 저장
from openpyxl import load_workbook #excel 읽기
from django.conf import settings
from .module import DomainDicMain

DB_CONN_INFO = "host=192.168.0.244 dbname=crawler user=taihoinst password=taiho123 port=5432";

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)

    try:
        imgForm = "data:image/png;base64,"
        # f = h5py.File('static/h5/data2.h5', 'r')

        # dset = f['X0']
        # data = np.array(dset[:,:,:])
        # cv2.imwrite(file, data)

        # Convert captured image to JPG
        # retval, buffer = cv2.imencode('.png', data)

        # png_as_text = base64.b64encode(buffer)

        # jpg_original = base64.b64decode(png_as_text)

        # imgForm += png_as_text.decode("utf-8") 

        return render(
            request,
            'app/index.html',
            {
                'title':'Home Page',
                'year':datetime.now().year,
                'imgVal':imgForm
            }
        )
    except Exception as e:
        print("[Errno {0}] ".format(e))
        return render(
            request,
            'app/index.html',
            {
                'title':'Home Page',
                'year':datetime.now().year,
                'imgVal':'none'
            }
        )
@csrf_exempt
def getImageFnc(request):
    fileName = request.POST.get('fileName', None)
    fileIndex = int(request.POST.get('fileIndex', None)) +1
    imgForm = "data:image/png;base64, "

    try:
        
        start = dt.datetime.now()

        f = h5py.File('static/h5/data2.h5', 'r')
        
        time.sleep(0.1)

        progTime = dt.datetime.now()
        print("\n1--------------------: ", (progTime - start).seconds, " seconds")

        keys = f.keys()
    
        dset = ''
        fIndex = -1
        fName = ''

        arrLen = len(keys)
        for i, fName in enumerate(keys):
            if fileIndex >= arrLen-1 or fileIndex==0:
                dset = f[fName]
                fIndex = i
                fName = fName
                break
            elif i != 0 and fileIndex <= i:
                dset = f[fName]
                fIndex = i
                fName = fName
                break
        
        
        end = dt.datetime.now()
        print("\n2--------------------: ", (end - start).seconds, " seconds")

        data = np.array(dset[:,:,:])
        # cv2.imwrite(file, data)

        # Convert captured image to JPG
        retval, buffer = cv2.imencode('.png', data)

        png_as_text = base64.b64encode(buffer)

        # jpg_original = base64.b64decode(png_as_text)
    
        imgForm += png_as_text.decode("utf-8") 
        # tmp = str(png_as_text, encoding)

        data = {
            'success': True,
            'imgForm': imgForm,
            'fIndex': fIndex,
            'fName': fName
        }
        return JsonResponse(data)
    except Exception as e:
        print("[Errno {0}] ".format(e))
        data = {
            'success': False,
            'imgForm': '',
            'fIndex': '-1',
            'fName': ''
        }
        return JsonResponse(data)


def dirFileReadFnc(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)

    try:
        imgForm = "data:image/png;base64,"
        # f = h5py.File('static/h5/data2.h5', 'r')

        # dset = f['X0']
        # data = np.array(dset[:,:,:])
        # cv2.imwrite(file, data)

        # Convert captured image to JPG
        # retval, buffer = cv2.imencode('.png', data)

        # png_as_text = base64.b64encode(buffer)

        # jpg_original = base64.b64decode(png_as_text)

        # imgForm += png_as_text.decode("utf-8") 

        return render(
            request,
            'app/normalDir.html',
            {
                'title':'Home Page',
                'year':datetime.now().year,
                'imgVal':imgForm
            }
        )
    except Exception as e:
        print("[Errno {0}] ".format(e))
        return render(
            request,
            'app/normalDir.html',
            {
                'title':'Home Page',
                'year':datetime.now().year,
                'imgVal':'none'
            }
        )


@csrf_exempt
def getImageByDirFnc(request):
    inputName = request.POST.get('fileName', None)
    fileIndex = int(request.POST.get('fileIndex', None))

    try:
        
        start = dt.datetime.now()

        #PATH = os.path.abspath(os.path.join('..', 'input'))
        #C:\Users\taiho\Desktop\images\img_align_celeba
        SOURCE_IMAGES = "C://Users/taiho/Desktop/images/img_align_celeba" #os.path.join(PATH, "images3")

        progTime = dt.datetime.now()
        print("\n1--------------------: ", (progTime - start).seconds, " seconds")
        
        bodyCompare = ''
        saveFileName = ''
        images = []
        fIndex = 0
        for root, dirnames, filenames in os.walk(SOURCE_IMAGES):
            for filename in fnmatch.filter(filenames, '*.*'):
                fullPath = os.path.join(root, filename)
                if inputName == '' and bodyCompare == '':
                    bodyCompare = open(fullPath, 'rb').read()
                    saveFileName = filename
                    fIndex += 1
                    break
                elif fIndex==fileIndex:
                    bodyCompare = open(fullPath, 'rb').read()
                    saveFileName = filename
                    fIndex += 1
                    break
                else:
                    fIndex += 1
                #images.append(os.path.join(root, filename))
                #print(filename)
            if bodyCompare != '':
                print(bodyCompare)
                break
        
        SAVE_IMAGES = "app/static/uploads/" #os.path.join(PATH, "static/app/uploads/")
        saveDir = SAVE_IMAGES + saveFileName
        newFile = open(saveDir, 'wb')
        newFile.write(bodyCompare)
        newFile.close()
        
        end = dt.datetime.now()
        print((end - start).seconds, "seconds", end="")
        data = {
            'success': True,
            'fIndex': fIndex,
            'fName': saveFileName
        }
        return JsonResponse(data)
    except Exception as e:
        print("[Errno {0}] ".format(e))
        data = {
            'success': False,
            'fIndex': -1,
            'fName': ''
        }
        return JsonResponse(data)

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Contact',
            'message':'Your contact page.',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        }
    )

def crawlerMLPage(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/crawlerML.html',
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        }
    )
def crawling(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/crawling.html',
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        }
    )


def webcrawlerStart(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    resultlist = webcrawlerApp();
    data = {
            'success': True,
            'result' : resultlist
        }
    return JsonResponse(data)

def webcrawlerApp():
    cnt = 0
    pageNum = 100
    resultlist = [];
    while cnt<=pageNum:
       r = requests.get('http://minishop.gmarket.co.kr/cam365/List?Title=Best%20Item&CategoryType=General&SortType=MostPopular&DisplayType=List&Page='+str(cnt)+'&PageSize=60&IsFreeShipping=False&HasDiscount=False&HasStamp=False&HasMileage=False&IsInternationalShipping=False&MinPrice=36890&MaxPrice=912120#listTop')
       html = r.text
       soup = BeautifulSoup(html, 'html.parser')
       titles = soup.select('.sbj') 
       for title in titles:
            resultlist.append(title.text);
       cnt += 1
        
    return resultlist;
    
def getCrawlerResultListFnc(request):
    try :
        conn = pg2.connect(DB_CONN_INFO)
        cur = conn.cursor()

        cur.execute('SELECT * FROM public."TBL_CRAWLER_RESULT_LIST";')
        rows = cur.fetchall()

        data = {
            'success': True,
            'crawlerResultList': rows,
        }

        return JsonResponse(data)
    except Exception as e:
        print('postgresql database connection error!')
        print(e)
    finally:
        if conn:
            conn.close()

def uploadExcelFnc(request):
    if request.method == 'POST' and request.FILES['excel']:
        excel = request.FILES['excel']
        fs = FileSystemStorage()
        filename = fs.save(excel.name, excel)
        worksheet = load_workbook(settings.BASE_DIR + '\\' + filename, data_only=True).worksheets[0]
        queryList = []
        for column in worksheet.iter_rows(min_row=2):
            sentence = column[2].value
            if sentence is None:
                break
            queryList.append('INSERT INTO public.\"TBL_CRAWLER_RESULT_LIST\"(\"SENTENCE\") VALUES (\'' + sentence + '\');')

        result = dbInsertQuery(queryList)

        data = {
            'success': result
        }
    return JsonResponse(data)

def dbInsertQuery(queryList):
    try :
        conn = pg2.connect(DB_CONN_INFO)
        cur = conn.cursor()

        for query in queryList:
            cur.execute(query)
        conn.commit()
        print ("Record inserted successfully")

    except Exception as e:
        print(e)
        return False
    else:
        return True
    finally:
        if conn:
            conn.close()
@csrf_exempt
def mlProcessFnc(request):
    query = 'SELECT "SENTENCE" FROM public."TBL_CRAWLER_RESULT_LIST";'
    result = dbSelectQuery(query)
    modelNumberList = []
    if(result):
        for row in result:
            modelNumber = DomainDicMain.run(row[0])
            modelNumberList.append(modelNumber)

        data = {
            'success': True,
            'modelNumberList': modelNumberList
        }
    else:
        data = {
            'success': False    
        }

    return JsonResponse(data)


def dbSelectQuery(query):
    try :
        conn = pg2.connect(DB_CONN_INFO)
        cur = conn.cursor()

        cur.execute(query)
        rows = cur.fetchall()

    except Exception as e:
        print(e)
        return False
    else:
        return rows
    finally:
        if conn:
            conn.close()