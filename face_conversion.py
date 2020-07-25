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

'''
Returns a json object that contains the face infos in image.
Refer https://developers.kakao.com/docs/latest/ko/vision/dev-guide#recog-face
for more details.
'''
def detect_face(url):
    API_URL = 'https://kapi.kakao.com/v1/vision/face/detect'
    headers = {'Authorization': 'KakaoAK {}'.format(KAKAO_REST_KEY)}
    data = {'image_url': url}
    response = requests.post(API_URL, data=data, headers=headers)
    return (response.json())

'''
Downloads an image from url and returns the random-generated image name.
If url has no image or access is invalid, return None.
'''
def download_image(url):
    response = requests.get(url, allow_redirects=True)

    # Check type of image
    contentType = response.headers["Content-Type"]
    if (contentType == "image/png"):
        mimeType = "png"
    elif (contentType == "image/jpeg"):
        mimeType = "jpg"
    else:
        return None
    
    # Randomly generate filename
    timestamp = int(time.time())
    randomString = int(random.random()*1E9)
    fileName = "{:d}-{:d}.{:s}".format(timestamp, randomString, mimeType)
    with open("./static/{}".format(fileName), 'wb') as f:
        f.write(response.content)
    return fileName


def convert_image(url):
    filename = "static/"+download_image(url)
    face_json = detect_face(url)
    image = Image.open(filename)
    subimg = Image.open('cat.png')
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
    return filename