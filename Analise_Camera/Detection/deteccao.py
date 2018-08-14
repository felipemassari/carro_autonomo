import cv2 as cv
import numpy as np
from util import *
#intervalos: rua, calcada, semaforo, vermelho1, vermelho2, amarelo, verde

'''
img = cv.imread("./images/teste.png")


cv.imshow("Original", img)
cv.waitKey(0)
cv.destroyAllWindows()

mask = detectaHSV(img, rua, calcada)
cv.imshow("Deteccao de rua e calcada",mask)
cv.waitKey(0)
cv.destroyAllWindows()

roiD = ROI_Direito(img)
roiE = ROI_Esquerdo(img)

mask = detectaHSV(roiD,calcada)
print("pixels de calcada na direita:")
print(contaPixelsDetectados(roiD))
cv.imshow("Deteccao calcada no lado direito",mask)
cv.waitKey(0)
cv.destroyAllWindows()

mask = detectaHSV(roiE,calcada)
print("pixels de calcada na esquerda:")
print(contaPixelsDetectados(roiE))
cv.imshow("Deteccao calcada no lado esquerdo",mask)
cv.waitKey(0)
cv.destroyAllWindows()

print("Desviar quanto o motor:")
print(desvioDoCarro(img))

img = cv.imread("./images/pedestre1.jpg")

pedestreDetectado, deteccao = detectaPedestres(img)
cv.imshow("Pedestres detectados", deteccao)
cv.waitKey(0)
cv.destroyAllWindows()
print("Pedestres detectados = "+ str(pedestreDetectado))

img = cv.imread("./images/carro4.jpeg")

carroDetectado, deteccao = detectaCarros(img)
cv.imshow("Carros detectados", deteccao)
cv.waitKey(0)
print("Carros detectados = "+str(carroDetectado))
'''

#teste de leitura de semaforo de uma imagem
'''
img = cv.imread("./images/semaforo2.jpeg")
mask = detectaHSV(img,semaforo)
mostraImg(mask)
#cv.imshow("sa",img)
#cv.waitKey(0)
print(leSemaforo(img))
'''

#teste de leitura do semaforo da camera
'''
cap = cv.VideoCapture(0)

while(cap.isOpened()):
	ret,frame = cap.read()
	print(leSemaforo(frame))
	cv.imshow("frame",frame)
	if cv.waitKey(1) & 0xFF == ord('q'):
		break

cap.release()
cv.destroyAllWindows()

'''


#teste de deteccao de obstaculos na pista
'''
cap = cv.VideoCapture(0)

while(cap.isOpened()):
	ret,frame = cap.read()
	print(haObstaculoNaPista(frame))
	cv.imshow("frame",frame)
	if cv.waitKey(1) & 0xFF == ord('q'):
		break

cap.release()
cv.destroyAllWindows()
'''

#tentativa de calibracao
'''
cap = cv.VideoCapture(0)

#espera posicionamento
while(cap.isOpened()):
	ret,frame = cap.read()	
	
	cv.imshow("frame",frame)
	if cv.waitKey(1) & 0xFF == ord('q'):
		break

calcada, rua = calibraHSV(frame)

cv.destroyAllWindows()

while(cap.isOpened()):
	ret,frame = cap.read()
	#hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)	
	#H,S,V = cv.split(hsv)
	
	detRua = detectaHSV(frame,rua)
	
	detCalcada = detectaHSV(frame,calcada)
	#ret2,thresh = cv.threshold(H,thH,255,cv.THRESH_BINARY)
	#ret2,thresh = cv.threshold(H,threshold,255,cv.THRESH_BINARY)
	#ret2,thresh = cv.threshold(H,threshold,255,cv.THRESH_BINARY)
	#hsv = cv.merge((H,S,V))
	
	cv.imshow("Calcada",detCalcada)
	cv.imshow("Rua",detRua)
	if cv.waitKey(1) & 0xFF == ord('q'):
		break

cap.release()
cv.destroyAllWindows()
'''
'''
#testa camera
cap = cv.VideoCapture(0)

while(cap.isOpened()):
	ret,frame = cap.read()
	det = detectaHSV(frame,semaforo)
	
	cv.imshow("frame",det)
	if cv.waitKey(1) & 0xFF == ord('q'):
		break

cap.release()
cv.destroyAllWindows()
'''

luzVermelha_min1 = np.array([0,0,130])
luzVermelha_max1 = np.array([18,150,255])
vermelho1 = (luzVermelha_min1,luzVermelha_max1)

luzVermelha_min2 = np.array([150,0,130]) 
luzVermelha_max2 = np.array([180,150,255])
vermelho2 = (luzVermelha_min2,luzVermelha_max2)

branco1= np.array([0,0,207])
branco2= np.array([180,60,255])
brancoDet = (branco1,branco2)

preto1=np.array([0,0,0])
preto2=np.array([180,255,45])
preto=(preto1,preto2)


cap = cv.VideoCapture(0)

while(cap.isOpened()):
	ret,frame = cap.read()
	#det = detectaHSV(frame,semaforo)
	branco = detectaHSV(frame,brancoDet)
	
	kernel = np.ones((5,5),np.uint8)
	branco = cv.erode(branco,kernel,iterations = 5)
	branco = cv.dilate(branco,kernel,iterations = 5)
	
	#branco = cv.bitwise_not(branco)
	blur = cv.GaussianBlur(branco,(5,5),0)
	
	branco = cv.bitwise_and(branco,branco,mask=blur)
	
	
	gray = cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
	ret2,binary = cv.threshold(gray, 140,255,cv.THRESH_BINARY)
	
	detPreto = detectaHSV(frame, preto)
	
	kernel = np.ones((7,7),np.uint8)
	
	detPreto = cv.dilate(detPreto,kernel,iterations = 3)

	sem = cv.bitwise_and(frame,frame,mask=detPreto)
	print(sinalMaisForte(sem))
	cv.imshow("preto",sem)
	#cv.imshow("frame",branco)
	if cv.waitKey(1) & 0xFF == ord('q'):
		break

cap.release()
cv.destroyAllWindows()

