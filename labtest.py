import numpy as np
from imutils.contours import sort_contours
import cv2 as cv
import imutils 

image = cv.imread('./Imagenes/U/U.png')
gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
blurred = cv.GaussianBlur(gray,(5,5),0)
edged = cv.Canny(blurred,30,150)

cnts = cv.findContours(edged.copy(), cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
cnts = sort_contours(cnts, method="left-to-right")[0]

for c in cnts:
    (x, y, w, h) = cv.boundingRect(c)
    if (w >= 35 and w <= 150) and (h >= 35 and h <= 120):
        cv.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv.imwrite('test.png',image)
