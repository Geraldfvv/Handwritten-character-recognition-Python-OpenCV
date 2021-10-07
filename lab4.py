from imutils.contours import sort_contours
from matplotlib import pyplot as plt
import os, os.path
import cv2 as cv
import imutils 
import numpy as nu

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
    ret,binary = cv.threshold(edged, 0, 255, cv.THRESH_BINARY )

    cnts = cv.findContours(binary.copy(), cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = sort_contours(cnts, method="left-to-right")[0]

    i = index
    for c in cnts:
        (x, y, w, h) = cv.boundingRect(c)
        if (w >= dimX and w <= 150) and (h >= dimY and h <= 120):
            roi = binary[y:y + h, x:x + w]
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
        border = cv.copyMakeBorder(image, top=height, bottom=height, left=width, right=width, borderType= cv.BORDER_CONSTANT, value=[0,0,0] )
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
        border = cv.copyMakeBorder(resized, top=height, bottom=height, left=widtg, right=widtg, borderType= cv.BORDER_CONSTANT, value=[0,0,0] )
        resize = cv.resize(border,(100,100))
        cv.imwrite('./SpecimensWithBorders/'+letra+'/'+num,resize)

# Extrae el histograma de una imagen
def extract_histogram(img,ax):
    image = cv.imread(img)
    dim = image.shape
    hist = []

    count = 0
    if (ax == 'X'):
        for i in range(0,dim[0]):
            for j in range(0,dim[1]):
                if (nu.any(image[i,j]) != 0):
                    count = count + 1
            if((i+1)%4 == 0):
                hist.append(count)
                count = 0
        return hist

# Genera un grafico del histograma
def generate_graphic_histogram(img,ax):
    hist = extract_histogram(img,ax)
    hist_formated = []
    for h in hist:
        x = []
        x.append(h)
        hist_formated.append(x)
    return hist_formated

def test(letter):
    path, dirs, files = next(os.walk('./SpecimensWithBorders/'+letter))
    histogram = []
    for f in files: 
        hist = nu.array(extract_histogram(path+"/"+f))
        if (len(histogram)==0):
            histogram = hist
        else:
            zip_list = zip(histogram,hist)
            histogram = [x + y for (x,y) in zip_list]
    
    i = 0
    for num in histogram:
        if (num != 0):
            histogram[i] = round(num / len(files))
        i+=1

    print(sum(histogram))

def apply():
    apply_processing('A')
    apply_processing('E')
    apply_processing('I')
    apply_processing('O')
    apply_processing('U')

    modify_specimens('A')
    modify_specimens('E')
    modify_specimens('I')
    modify_specimens('O')
    modify_specimens('U')

#A = generate_graphic_histogram('./SpecimensWithBorders/A/A0-0.png','X') 
#E = generate_graphic_histogram('./SpecimensWithBorders/E/E0-0.png','X') 
#I = generate_graphic_histogram('./SpecimensWithBorders/I/I0-0.png','X') 
#O = generate_graphic_histogram('./SpecimensWithBorders/O/O0-0.png','X') 

#fig, ax = plt.subplots(2,2)
#ax[0,0].plot(A)
#ax[0,1].plot(E)
#ax[1,0].plot(I)
#ax[1,1].plot(O)
#plt.show()
