import cv2 as cv
import numpy as np

#supondo marrom (pedaco de madeira)
rua_min = np.array([15,80,80])
rua_max = np.array([25,255,255])
rua = (rua_min,rua_max)

#supondo cor branca
calcada_min = np.array([0,0,80]) 
calcada_max = np.array([180,25,255])
calcada = (calcada_min,calcada_max)

#supondo cor preta - usar como ROI=>encontrar luz dentro da regiao
semaforo_min = np.array([0,0,0])  
semaforo_max = np.array([180,255,40])
semaforo = (semaforo_min,semaforo_max)

#necessario 2 valores => vermelho esta entre ~350 a ~10 graus em HSV
luzVermelha_min1 = np.array([0,170,150])
luzVermelha_max1 = np.array([7,255,255])
vermelho1 = (luzVermelha_min1,luzVermelha_max1)

luzVermelha_min2 = np.array([175,170,150]) 
luzVermelha_max2 = np.array([180,255,255])
vermelho2 = (luzVermelha_min2,luzVermelha_max2)

luzAmarela_min = np.array([22,170,150])
luzAmarela_max = np.array([30,255,255])
amarelo = (luzAmarela_min,luzAmarela_max)

luzVerde_min = np.array([40,170,150])
luzVerde_max = np.array([70,255,255])
verde = (luzVerde_min,luzVerde_max)

#valores para calibrar depois
fatorDesvio = 1.0 #usado para calcular o valor enviado aos motores
qtdeRuaEsperada = 70000 #qtos pixels de rua se espera ver

#cor detectada - em branco
#0-preto / 1-branco

#funcao que recebe uma imagem e varios intervalos e retorna em branco a deteccao de todos os intervalos na imagem
def detecta(img,*intervalos):
    hsv = cv.cvtColor(img,cv.COLOR_BGR2HSV)
    mask = np.zeros((img.shape[0],img.shape[1]),np.uint8)
    for intervalo in intervalos:
        maskAux = cv.inRange(hsv,intervalo[0],intervalo[1])
        mask = cv.bitwise_or(mask,maskAux)
    return mask

#faz uma ROI com o lado direito da imagem
def ROI_Direito(img):
    return ROIporPorcentagem(img,0,100,50,100)
    #return img[0:img.shape[0],img.shape[1]//2:img.shape[1]]

#faz uma ROI com o lado esquerdo da imagem
def ROI_Esquerdo(img):
    return ROIporPorcentagem(img,0,100,0,50)

#conta quantos pixels brancos estao na imagem enviada
def contaPixelsDetectados(img):
    return np.sum(img == 255)

#retorna um valor para ser usado como referencia de quanto o carro tem que virar para continuar na pista
def desvioDoCarro(img):
    roiD = ROI_Direito(img)
    roiE = ROI_Esquerdo(img)
    qtdeD = contaPixelsDetectados(roiD)
    qtdeE = contaPixelsDetectados(roiE)
    #valores positivos => desvio para a direita
    return fatorDesvio*(qtdeD - qtdeE)

#verifica se existe um objeto na pista, o criterio por enquanto eh se muito da rua estiver bloqueado entao tem um obstaculo
'''
Depois sera necessario melhorar: tenho que saber que regiao da camera
estara vendo a rua para nao considerar o horizonte, que sera visto como
obstaculo por enquanto. Vou ter que fazer uma ROI para considerar soh
abaixo do horizonte, mas nao sei como a camera vai estar posicionada no
carro. Eh possivel tambem mudar para detectar traseira de carros com
haarcascades prontos (que nem fiz para pedestres) mas nao consegui fazer
ser confiavel, dah muitas deteccoes erradas
'''
def haObstaculoNaPista(img):
    detRua = detecta(img,rua)
    qtdeRua = contaPixelsDetectados(detRua)
    return qtdeRua<qtdeRuaEsperada
    
'''
o---> x
|
|
v
y
'''
#recebe intervalos dados em porcentagens da ROI desejada e retorna a ROI 
def ROIporPorcentagem(img,y1,y2,x1,x2):
    yMax, xMax = img.shape[0:2]
    return img[(yMax*y1)//100:(yMax*y2)//100,(xMax*x1)//100:(xMax*x2)//100]
