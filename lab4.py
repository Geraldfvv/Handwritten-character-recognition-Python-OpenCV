from imutils.contours import sort_contours
from matplotlib import pyplot as plt
import os, os.path
import cv2 as cv
import imutils 
import numpy as nu
import random

# Aplica el procesamiento a las fotos en la carpetea Imagenes que contienen aproximadamente
# 40 letras cada imagen.
def apply_processing(letter):
    path, dirs, files = next(os.walk('./Imagenes/'+letter))
    path1, dirs2, files2 = next(os.walk('./Specimen/'+letter))

    print("- Extracting " + letter + "'s : " + str(len(files)) + " Images ...")

    i = 0
    dimX = 35
    dimY = 35
    for f in files:
        if (letter == 'I'):
            dimX = 8
            dimY = 40
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
    print("- Processing " + letter + "'s : " + str(len(files)) + " Images ...")

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
        width = round(w * scale_percent / 100)
        height = round(h * scale_percent / 100)
        dim = (width, height)
        resized = cv.resize(image, dim, interpolation = cv.INTER_AREA)

        h, w, c = image.shape
        width = abs(int((borderSizeTop-w)/2))
        height = abs(int((borderSizeTop-h)/2))
        border = cv.copyMakeBorder(resized, top=height, bottom=height, left=width, right=width, borderType= cv.BORDER_CONSTANT, value=[0,0,0] )
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
def generate_graphic_histogram(hist):
    hist_formated = []
    for h in hist:
        x = []
        x.append(h)
        hist_formated.append(x)
    return hist_formated

# Genera un promedio del histograma con todos los especimenes
def calculate_average(letter,list):
    files = list[0]
    histogram = []
    print("- Average histogram letter " + letter + " : " + str(len(files)) + " Images ...")

    for f in files: 
        hist = nu.array(extract_histogram('./SpecimensWithBorders/'+letter+"/"+ f,'X'))
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

    return (histogram)

# Muestra los histograma promedio de cada letra
def show_histogram(A,E,I,O,U):
    fig, ax = plt.subplots(2,3)
    ax[0,0].plot(generate_graphic_histogram(A))
    ax[0,0].set_title('Histogram A')

    ax[0,1].plot(generate_graphic_histogram(E) )
    ax[0,1].set_title('Histogram E')

    ax[0,2].plot(generate_graphic_histogram(I) )
    ax[0,2].set_title('Histogram I')

    ax[1,0].plot(generate_graphic_histogram(O) )
    ax[1,0].set_title('Histogram O')

    ax[1,1].axis('off')

    ax[1,2].plot(generate_graphic_histogram(U) )
    ax[1,2].set_title('Histogram U')

    plt.show()

# Crea dos listas, una con el 70% de las muestras y otra con el
def select_specimen(letter):
    path, dirs, files = next(os.walk('./SpecimensWithBorders/'+letter))
    nelements = round(len(files)*0.7)
    specimens70 = []
    specimens30 = []
    specimens = []

    while len(specimens70) < nelements:
        file = files[random.randint(0,len(files)-1)]
        if file not in specimens70:
            specimens70.append(file)
    
    specimens30 = list(set(files) - set(specimens70))
    specimens.append(specimens70)
    specimens.append(specimens30)
    return (specimens)

def main():
    print("============================ Extracting specimens")
    
    #apply_processing('A')
    #apply_processing('E')
    #apply_processing('I')
    #apply_processing('O')
    #apply_processing('U')

    print("============================ Recizing and centering")
    
    #modify_specimens('A')
    #modify_specimens('E')
    #modify_specimens('I')
    #modify_specimens('O')
    #modify_specimens('U')

    print("============================ Selecting specimens")

    a_specimens = select_specimen('A')
    e_specimens = select_specimen('E')
    i_specimens = select_specimen('I')
    o_specimens = select_specimen('O')
    u_specimens = select_specimen('U')

    print("============================ Making average histogram")
    avgA = avgE = avgI = avgO = avgU = '' 

    avgA = calculate_average('A',a_specimens)
    avgE = calculate_average('E',e_specimens)
    avgI = calculate_average('I',i_specimens)
    avgO = calculate_average('O',o_specimens)
    avgU = calculate_average('U',u_specimens)

    file = open("histograms.txt","w",encoding="utf-8")
    file.write(str(avgA)+"\n")
    file.write(str(avgE)+"\n")
    file.write(str(avgI)+"\n")
    file.write(str(avgO)+"\n")
    file.write(str(avgU)+"\n")
    file.close()
    
    if (avgA == avgE == avgI == avgO == avgU == '' ):
        file = open("histograms.txt","r")
        i = 0
        for line in file:
            hist = line.replace("[","")
            hist = hist.replace("]","")
            hist = hist.replace("\n","")
            hist = list(hist.split(','))
            hist = [int(i) for i in hist]
            if i == 0 :
                avgA = hist
                i+=1
            elif i == 1 :
                avgE = hist
                i+=1
            elif i == 2 :
                avgI = hist
                i+=1
            elif i == 3 :
                avgO = hist
                i+=1
            elif i == 4 :
                avgU = hist
                i+=1
        file.close()
    show_histogram(avgA,avgE,avgI,avgO,avgU)

#main()

