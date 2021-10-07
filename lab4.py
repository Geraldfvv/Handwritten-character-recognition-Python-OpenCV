from imutils.contours import sort_contours
from matplotlib import pyplot as plt
import os, os.path
import cv2 as cv
import imutils 

# Aplica el procesamiento a las fotos en la carpetea Imagenes que contienen aproximadamente
# 40 letras cada imagen.
def apply_processing(letter):
    path, dirs, files = next(os.walk('./Imagenes/'+letter))
    path1, dirs2, files2 = next(os.walk('./Specimen/'+letter))
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

# Inicialmente aplica filtros a la imagen para facilitar su procesamiento, despues detecta bordes 
# y guarda las coordenadas del bounding box, se recorre estas coordenadas y se recorta cada letra detectada.
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
            roi = gray[y:y + h, x:x + w]
            cv.imwrite('./Specimen/'+letter+"/"+letter+str(sample)+"-"+str(i)+'.png',roi)
            i+=1

# Aplica bordes a todos los especimenes de una letra en especifico      
def modify_specimens(letter):
    path, dirs, files = next(os.walk('./Specimen/'+letter))
    for f in files:
        image = cv.imread('./Specimen/'+letter+'/'+f)
        applyBorder(image,letter,f)

# Aplica los bordes y dimensionado a una imagen
def applyBorder(image,letra,num):
    borderSizeTop=100
    h, w , c = image.shape
    
    if (w < 100) and (h < 100):
        width = round((borderSizeTop-w)/2)
        height = round((borderSizeTop-h)/2)
        border = cv.copyMakeBorder(image, top=height, bottom=height, left=width, right=width, borderType= cv.BORDER_CONSTANT, value=[255,255,255] )
        resize = cv.resize(border,(100,100))
        cv.imwrite('./SpecimensWithBorders/'+letra+'/'+num,resize)
    
    else:
        scale_percent = 55 # percent of original size
        width = int(w * scale_percent / 100)
        height = int(h * scale_percent / 100)
        dim = (width, height)
        resized = cv.resize(image, dim, interpolation = cv.INTER_AREA)

        h, w, c = image.shape
        widtg = round((borderSizeTop-w)/2)
        height = round((borderSizeTop-h)/2)
        border = cv.copyMakeBorder(resized, top=height, bottom=height, left=widtg, right=widtg, borderType= cv.BORDER_CONSTANT, value=[255,255,255] )
        resize = cv.resize(border,(100,100))
        cv.imwrite('./SpecimensWithBorders/'+letra+'/'+num,resize)

# Extrae el histograma de una imagen
def extract_histogram(img):
    image = cv.imread(img)
    hist = cv.calcHist([image],[0],None,[256],[0,256])

    flat_list = []
    for sublist in hist:
        for item in sublist:
            flat_list.append(item)

    return flat_list

def test():
    





print(flat_list)

histList = []
histList.append(h0)
histList.append(h2)



# Aplicar filtros a las imagenes iniciales

# apply_processing('A')
# apply_processing('E')
# apply_processing('I')
# apply_processing('O')
# apply_processing('U')
