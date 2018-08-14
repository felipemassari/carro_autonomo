import cv2 as cv
import numpy as np
import time
from util import *
from controleCarro import *

cap = cv.VideoCapture(0)

color = (0, 0, 0)
# Capture frame-by-frame
ret, frame = cap.read()

while (True):
 # Capture frame-by-frame
	ret, frame = cap.read()

	#frameDet = detectaHSV(frame, calcada)

	
	tamanho = frame.shape

	x1 = tamanho[1]/2 
	y1 = tamanho[0]/2 + 100
	x2 = tamanho[1]/2 
	y2 = tamanho[0]/2 - 100

	frame2 = ROIporPorcentagem(frame,0,50,0,50)

	cv.rectangle(frame, (x1-300, y1), (x2+300, y2), color, 2)
	cv.circle(frame, (x1, y1-100), 2, color, thickness=3, lineType=8, shift=0) 

	
	#cv.imshow('frame',frame)
	
	gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)	
	
	ret2,binary = cv.threshold(gray, 180,255,cv.THRESH_BINARY)
	
	roi = ROIporPorcentagem(binary,50,100,0,100)
	
	
	thrCarro = 5000
	#print(desvioDoCarro(roi))
	if desvioDoCarro(roi)>thrCarro:
		esquerda()
	elif desvioDoCarro(roi)<-1*thrCarro:
		direita()
	else:
		avanca()
		
	#cv.imshow('gray',gray)
	
	cv.imshow('binary',binary)

	if cv.waitKey(1) & 0xFF == ord('q'):
		break

# When everything done, release the capture

cap.release()
cv.destroyAllWindows()
