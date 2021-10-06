import numpy as np
import cv2

im = cv2.imread('./Specimen/A0.png')
row, col= im.shape[:2]
bottom= im[row-2:row, 0:col]
mean= cv2.mean(bottom)[0]

borderSizeTop=100
h, w, c = im.shape

if (w < 100) and (h < 100):
    widtg = round((borderSizeTop-w)/2)
    height = round((borderSizeTop-h)/2)
    border=cv2.copyMakeBorder(im, top=height, bottom=height, left=widtg, right=widtg, borderType= cv2.BORDER_CONSTANT, value=[0,0,0] )
    cv2.imwrite('border.png',border)

else:
    scale_percent = 60 # percent of original size
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)
    resized = cv2.resize(src, dsize[, dst[, fx[, fy[, interpolation]]]])

#Cambios