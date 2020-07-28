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
import urllib
import base64, os
import io

'''
Returns a json object that contains the face infos in image.
Refer https://developers.kakao.com/docs/latest/ko/vision/dev-guide#recog-face
for more details.
Input is the bytearray of an image content.
'''
def detectFace(content):
    API_URL = 'https://kapi.kakao.com/v1/vision/face/detect'
    headers = {'Authorization': 'KakaoAK {}'.format(KAKAO_REST_KEY)}
    files = { 'file' : content }
    response = requests.post(API_URL, headers=headers, files=files)
    return response.json()


''' Downloads an image from url '''
def download_image(url):
    try:
        with urlopen(url) as response:
            data = response.read()
            contentType = response.info().get_content_type()
        if (contentType not in ["image/png", "image/jpeg"]):
            return None, None
        return data, contentType
    except (ValueError, urllib.error.HTTPError):
        print("Image download failed {}".format(url))
        return None, None


''' Convert a file (specified by a path) into a data URI '''
def img_to_data(output, contentType):
    data64 = (base64.b64encode(output)).decode("utf-8")
    return "data:{};base64,{}".format(contentType, data64)


'''
Select image from pitch and yaw value
'''
def angle(pitch, yaw):
    cat='error'
    if pitch>-0.5 and pitch<0.5:
        if yaw>-0.35 and yaw<0.35:
            cat='front.PNG'
        elif yaw>=0.35 and yaw<0.75:
            cat='half-right.PNG'
        elif yaw>=0.75 and yaw<=1:
            cat='right.PNG'
        elif yaw<=-0.75:
            cat='left.PNG'
        elif yaw>-0.75 and yaw<=-0.35:
            cat='half-left.PNG'
    elif pitch>=0.5 and pitch<=1:
        if yaw>-0.35 and yaw<0.35:
            cat='up.PNG'
        elif yaw>=0.35 and yaw<=1:
            cat='half-up-right.PNG'
        elif yaw<=-0.35:
            cat='half-up-left.PNG'
    elif pitch<=-0.5 and pitch>=-1:
        if yaw>-0.35 and yaw<0.35:
            cat='down.PNG'
        elif yaw>=0.35 and yaw<=1:
            cat='half-down-right.PNG'
        elif yaw<=-0.35:
            cat='half-down-left.PNG'
    return cat


def convert_image(url):
    contentTypeToFormat = {"image/jpeg":"JPEG", "image/png":"PNG"}
    content, contentType = download_image(url)
    if (content is None):
        return None
    face_json = detectFace(content)
    image = Image.open(io.BytesIO(content))
    #subimg = Image.open('cat.png')
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
        name = angle(pitch, yaw)
        if (name == 'error'):
            print("Face detection error :{}".format(url))
            return None
        subimg = Image.open('asset/'+name)
        # box = subimg.resize((w,h),Image.NEAREST)
        box = subimg.resize((int(w*2.5),int(h*2.5)))
        box = box.rotate(roll / (np.pi/180))
        # image.paste(box, (x,y), box)
        image.paste(box, (x-int(w*1.5/2),y-int(h*2/2)), box)
    
    output = io.BytesIO()
    image.save(output, contentTypeToFormat[contentType])
    return img_to_data(output.getvalue(), contentType)
