#coding: utf-8
#ESZA019−17 − VisaoComputacional − NA − 2Q2018
#EXERCICIO COMPLEMENTAR Q1
#
#RA: 11015812
#NOME:Felipe Massari
#
#E−MAIL:flp.massari@gmail.com
#
#DESCRICAO:
#Codigo leitura da webcam e a partir daí faz passagem para escala
#de cinza utilizando funcao basica do opencv
###-------------------------------------------------------###

import numpy as np
import cv2

cap = cv2.VideoCapture(0)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Passa de RGB para escala de cinza
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


    # Janela com imagem RGB 
    cv2.imshow('RBG',frame)

    # Janela com imagem em escala de cinza  
    cv2.imshow('frame',gray)
   
    if cv2.waitKey(1) & 0xFF == ord('q'):
		break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()