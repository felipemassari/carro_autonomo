import cv2 as cv
import numpy as np
from util import *
#intervalos: rua, calcada, semaforo, vermelho1, vermelho2, amarelo, verde

img = cv.imread("teste.png")


cv.imshow("Original", img)
cv.waitKey(0)
cv.destroyAllWindows()

mask = detecta(img, rua, calcada)
cv.imshow("Deteccao de rua e calcada",mask)
cv.waitKey(0)
cv.destroyAllWindows()

roiD = ROI_Direito(img)
roiE = ROI_Esquerdo(img)

mask = detecta(roiD,calcada)
print("pixels de calcada na direita:")
print(contaPixelsDetectados(roiD))
cv.imshow("Deteccao calcada no lado direito",mask)
cv.waitKey(0)
cv.destroyAllWindows()

mask = detecta(roiE,calcada)
print("pixels de calcada na esquerda:")
print(contaPixelsDetectados(roiE))
cv.imshow("Deteccao calcada no lado esquerdo",mask)
cv.waitKey(0)
cv.destroyAllWindows()

print("Desviar quanto o motor:")
print(desvioDoCarro(img))




