import cv2

cascadefile = "haarcascade_frontalface_default.xml"

img = cv2.imread('sample.jpg')
imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

cascade = cv2.CascadeClassifier(cascadefile)
facelist = cascade.detectMultiScale(imgray, scaleFactor=1.2, minNeighbors = 5)

if (len(facelist) >= 1):
    for face in facelist:
        x,y,w,h = face
        cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)

cv2.imwrite('sample_converted.jpg', img)
