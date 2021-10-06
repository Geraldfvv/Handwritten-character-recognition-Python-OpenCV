import numpy as np
import cv2


def letters():
    x = 0
    while x <= 40:
        num = str(x)
        image = cv2.imread('./Specimen/A/A0-'+num+'.png')
        applyBorder(image,'A','0',num)
        x += 1

    x = 0    
    while x <= 35:
        num = str(x)
        image = cv2.imread('./Specimen/A/A1-'+num+'.png')
        applyBorder(image,'A','1',num)
        x += 1
    
    x = 0    
    while x <= 39:
        num = str(x)
        image = cv2.imread('./Specimen/E/E0-'+num+'.png')
        applyBorder(image,'E','0',num)
        x += 1
    
    x = 0    
    while x <= 20:
        num = str(x)
        image = cv2.imread('./Specimen/E/E1-'+num+'.png')
        applyBorder(image,'E','1',num)
        x += 1

    x = 0    
    while x <= 38:
        num = str(x)
        image = cv2.imread('./Specimen/I/I0-'+num+'.png')
        applyBorder(image,'I','0',num)
        x += 1
    
    x = 0    
    while x <= 39:
        num = str(x)
        image = cv2.imread('./Specimen/I/I1-'+num+'.png')
        applyBorder(image,'I','1',num)
        x += 1
    
    x = 0    
    while x <= 39:
        num = str(x)
        image = cv2.imread('./Specimen/O/O0-'+num+'.png')
        applyBorder(image,'O','0',num)
        x += 1
    
    x = 0    
    while x <= 31:
        num = str(x)
        image = cv2.imread('./Specimen/O/O1-'+num+'.png')
        applyBorder(image,'O','1',num)
        x += 1
    
    x = 0    
    while x <= 39:
        num = str(x)
        image = cv2.imread('./Specimen/U/U0-'+num+'.png')
        applyBorder(image,'U','0',num)
        x += 1
    
    x = 0    
    while x <= 37:
        num = str(x)
        image = cv2.imread('./Specimen/U/U1-'+num+'.png')
        applyBorder(image,'U','1',num)
        x += 1

def applyBorder(image,letra,format,num):
    
    row, col= image.shape[:2]
    bottom= image[row-2:row, 0:col]
    mean= cv2.mean(bottom)[0]
    borderSizeTop=100
    h, w, c = image.shape
    
    if (w < 100) and (h < 100):
        widtg = round((borderSizeTop-w)/2)
        height = round((borderSizeTop-h)/2)
        border = cv2.copyMakeBorder(image, top=height, bottom=height, left=widtg, right=widtg, borderType= cv2.BORDER_CONSTANT, value=[0,0,0] )
        cv2.imwrite('./SpecimensWithBorders/'+letra+'/'+letra+format+'-'+num+'.png',border)
    
    else:
        scale_percent = 55 # percent of original size
        width = int(w * scale_percent / 100)
        height = int(h * scale_percent / 100)
        dim = (width, height)
        resized = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)

        h, w, c = image.shape
        widtg = round((borderSizeTop-w)/2)
        height = round((borderSizeTop-h)/2)
        border = cv2.copyMakeBorder(resized, top=height, bottom=height, left=widtg, right=widtg, borderType= cv2.BORDER_CONSTANT, value=[0,0,0] )
        cv2.imwrite('./SpecimensWithBorders/'+letra+'/'+letra+format+'-'+num+'.png',border)

letters()