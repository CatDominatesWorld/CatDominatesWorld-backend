import cv2

cascadefile = "haarcascade_frontalface_default.xml"

img = cv2.imread('sample.jpg')
imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

cascade = cv2.CascadeClassifier(cascadefile)
facelist = cascade.detectMultiScale(imgray, scaleFactor=2.08, minNeighbors = 1)

print(facelist)
if (len(facelist) >= 1):
    for face in facelist:
        x,y,w,h = face
        cv2.rectangle(img, (x,y), (x+w,y+h), (25,0,0), 2)

cv2.imwrite('sample_converted.jpg', img)
