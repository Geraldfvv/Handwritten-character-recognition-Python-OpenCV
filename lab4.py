import numpy as np
from imutils.contours import sort_contours
import os, os.path
import cv2 as cv
import imutils 

def apply_processing(letter):
    path, dirs, files = next(os.walk('./Imagenes/'+letter))
    path1, dirs2, files2 = next(os.walk('./Specimen/'+letter))
    print(dirs)
    i = 0
    dimX = 0
    dimY = 0
    for f in files:
        if (letter == 'A'):
            dimX = 50
            dimY = 20
        elif (letter == 'E'):
            dimX = 40
            dimY = 30
        elif (letter == 'I'):
            dimX = 9
            dimY = 15
        elif (letter == 'O'):
            dimX = 35
            dimY = 35
        elif (letter == 'U'):
            dimX = 35
            dimY = 35
        stract_specimen(letter,i,dimX,dimY,len(files2),'./Imagenes/'+letter+"/"+f)
        i+=1

def stract_specimen(letter,sample,dimX,dimY,index,img):
    image = cv.imread(img)
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    blurred = cv.GaussianBlur(gray,(5,5),0)
    edged = cv.Canny(blurred,30,150)

    cnts = cv.findContours(edged.copy(), cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = sort_contours(cnts, method="left-to-right")[0]

    i = index
    for c in cnts:
        (x, y, w, h) = cv.boundingRect(c)
        if (w >= dimX and w <= 150) and (h >= dimY and h <= 120):
            roi = edged[y:y + h, x:x + w]
            cv.imwrite('./Specimen/'+letter+"/"+letter+str(sample)+"-"+str(i)+'.png',roi)
            i+=1

apply_processing('A')
apply_processing('E')
apply_processing('I')
apply_processing('O')
apply_processing('U')
