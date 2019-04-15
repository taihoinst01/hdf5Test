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

def crawlerResultFnc(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/crawlerResult.html',
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        }
    )