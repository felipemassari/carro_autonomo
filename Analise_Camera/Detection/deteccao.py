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
img = cv.imread("./images/teste4.png")
print(leSemaforo(img))
