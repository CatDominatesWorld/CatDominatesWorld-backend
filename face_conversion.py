import requests, json
from config import KAKAO_REST_KEY
import time
import random
import sys
import argparse
import requests
import cv2
import numpy as np
import math
from PIL import Image, ImageFilter
from urllib.request import urlopen
import base64, mimetypes, os

'''
Returns a json object that contains the face infos in image.
Refer https://developers.kakao.com/docs/latest/ko/vision/dev-guide#recog-face
for more details.
'''
def detectFace(path):
    API_URL = 'https://kapi.kakao.com/v1/vision/face/detect'
    headers = {'Authorization': 'KakaoAK {}'.format(KAKAO_REST_KEY)}
    files = { 'file' : open(path, 'rb')}
    response = requests.post(API_URL, headers=headers, files=files)
    return (response.json())


'''
Save image at static directory. Return the random-generated filename.
'''
def saveImage(content, imageType):
    # Randomly generate filename
    timestamp = int(time.time())
    randomString = int(random.random()*1E9)
    fileName = "{:d}-{:d}.{:s}".format(timestamp, randomString, imageType)
    with open("./static/{}".format(fileName), 'wb') as f:
        f.write(content)
    return fileName

'''
Downloads an image from url
'''
def download_image(url):
    try:
        with urlopen(url) as response:
            data = response.read()
            contentType = response.info().get_content_type()
        
        if (contentType == "image/png"):
            imageType = "png"
        elif (contentType == "image/jpeg"):
            imageType = "jpg"
        else:
            return None

        return saveImage(data, imageType)
    except ValueError:
        print("Image download failed {}".format(url))
        return None

"""Convert a file (specified by a path) into a data URI."""
def img_to_data(path):
    if not os.path.exists(path):
        raise FileNotFoundError
    mime, _ = mimetypes.guess_type(path)
    print(mime)
    with open(path, 'rb') as fp:
        data = fp.read()
        data64 = (base64.b64encode(data)).decode("utf-8")
        return "data:{};base64,{}".format(mime, data64)


def convert_image(url):
    if (url is None):
        return None
    name = download_image(url)
    if (name is None):
        return None
    filename = "static/" + name
    face_json = detectFace(filename)
    image = Image.open(filename)
    subimg = Image.open('cat.png')
    if 'faces' not in face_json['result'].keys():
        return None
    for face in face_json['result']['faces']:
        x = int(face['x']*image.width)
        w = int(face['w']*image.width)
        y = int(face['y']*image.height)
        h = int(face['h']*image.height)
        pitch = float(face['pitch'])
        yaw = float(face['yaw'])
        roll = float(face['roll'])

        box = subimg.resize((int(w*1.5),int(h*1.5)),Image.NEAREST)
        box = box.rotate(roll / (np.pi/180))
        image.paste(box, (x-int(w*0.5/2),y-int(h*0.5/2)), box)
    
    image.save(filename)
    return img_to_data(filename)
