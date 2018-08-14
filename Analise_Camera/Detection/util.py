#encoding: utf-8
"""
    Módulo contendo funções usadas para auxiliar desenvolvimento do projeto
"""
import cv2 as cv
import numpy as np
from config import *



def detectaHSV(img,*intervalos):
    """função que recebe uma imagem e varios intervalos e retorna em branco a deteccao de todos os intervalos na imagem
    """
    hsv = cv.cvtColor(img,cv.COLOR_BGR2HSV)
    mask = imagemVazia(img)
    for intervalo in intervalos:
        maskAux = cv.inRange(hsv,intervalo[0],intervalo[1])
        mask = cv.bitwise_or(mask,maskAux)
    return mask

def contaPixelsDetectados(img):
    """conta quantos pixels brancos estao na máscara enviada"""
    return np.sum(img == 255)

def desvioDoCarro(img):
    """Recebe uma imagem binarizada da detecção da calçada e retorna um valor para ser usado como referencia de quanto o carro tem que virar para continuar na pista
    Valores positivos indicam mais pixels detectados à esquerda da imagem
    """
    roiD = ROI_Direito(img)
    roiE = ROI_Esquerdo(img)
    qtdeD = contaPixelsDetectados(roiD)
    qtdeE = contaPixelsDetectados(roiE)
    return fatorDesvio*(qtdeE - qtdeD)

def haObstaculoNaPista(img):
    """verifica se existe um objeto na pista, o criterio utilizado é de que se uma certa porção da pista for obstruída então há um obstáculo, considerando a ROI da camera que enxerga a pista
    """
	roiRua = ROIporPorcentagem(img,50,100,0,100)
	detRua = detectaHSV(roiRua,rua)
	qtdeRua = contaPixelsDetectados(detRua)
	return qtdeRua<qtdeRuaEsperada
    
def ROIporPorcentagem(img,y1,y2,x1,x2):
    """Recebe intervalos dados em porcentagens da ROI desejada e retorna a ROI 
    Por exemplo a metade superior da imagem seria (img,0,50,0,100)
"""
    yMax, xMax = img.shape[0:2]
    return img[(yMax*y1)//100:(yMax*y2)//100,(xMax*x1)//100:(xMax*x2)//100]

def pixelPorPorcentagem(img,y,x):
    """retorna o valor do pixel mais proximo"""
	yMax, xMax = img.shape[0:2]
	return img[yMax*y//100,xMax*x//100]

def ROI_Direito(img):
    """faz uma ROI com o lado direito da imagem"""
    return ROIporPorcentagem(img,0,100,50,100)

def ROI_Esquerdo(img):
    """faz uma ROI com o lado esquerdo da imagem"""
    return ROIporPorcentagem(img,0,100,0,50)

def limiarOtimoCanal(roi1,roi2):
    """retorna limiar para um canal, recebe duas regioes com 3 canais"""
	r1c1,r1c2,r1c3 = cv.split(roi1)
	r2c1,r2c2,r2c3 = cv.split(roi2)
	pass

#terminar descrição
def limiarOtimoCanalPixel(canal):
    """Recebe um canal e calcula o limiar para separar"""	
	valorPixelDireita = pixelPorPorcentagem(canal,50,25)
	valorPixelEsquerda = pixelPorPorcentagem(canal,50,75)
	return valorPixelDireita//2+valorPixelEsquerda//2

def calibraHSV(img):
    """faz a calibracao usando funcao acima, retorna limiar que separa cor da direita da tela e da esquerda 
    """
	hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
	H,S,V = cv.split(hsv)

	thH = limiarOtimoCanal(H)
	thS = limiarOtimoCanal(S)
	thV = limiarOtimoCanal(V)

	direita = (np.array([0,0,0]), np.array([thH,thS,thV]))  
	esquerda = (np.array([thH,thS,thV]), np.array([180,255,255]))  

	return esquerda, direita
	
def imagemVazia(img):
    """retorna uma imagem vazia (todos os pixels pretos) com as mesmas dimensoes de img
    """
	return np.zeros((img.shape[0],img.shape[1]),np.uint8)
	
def numeroDePixelsEmContorno(contour):
    """Calcula numero de pixels dado um contorno"""
	dx = contour[2][0][0] - contour[0][0][0]
	dy = contour[2][0][1] - contour[0][0][1]
	return dy*dx

def mostraImg(img):
    """mostra imagem e espera apertar uma tecla, apenas para debugar"""
	cv.imshow("teste",img)
	cv.waitKey(0)

def sinalMaisForte(roi):
    """retorna o sinal de semaforo detectado mais provavel. O critério utilizado é 
        
    """
	detVermelho = contaPixelsDetectados(detectaHSV(roi,ledVermelho))
	detAmarelo = contaPixelsDetectados(detectaHSV(roi,amarelo))
	detVerde = contaPixelsDetectados(detectaHSV(roi,verde))
	if detVermelho>detAmarelo and detVermelho>detVerde:
		return "Sinal vermelho"
	if detAmarelo>detVermelho and detAmarelo>detVerde:
		return "Sinal amarelo"
	if detVerde>detVermelho and detVerde>detAmarelo:
		return "Sinal verde"
	return "Sem sinal"
	
def semaforoValido(roi,largura,altura):
    """um semáforo valido é aquele que possui vermelho, amarelo ou verde dentro da regiao compreendida por ele. Esta funcao recebe a ROI do semaforo e verifica se ha um minimo dessas cores e se sim, retorna True. É necessário também um mínimo de pixels de semaforo para ser válido
    """
	if largura*altura < thresholdSemaforo:
		return False
	else:
		haAmarelo = contaPixelsDetectados(detectaHSV(roi,amarelo)) > thresholdSinal
		haVerde = contaPixelsDetectados(detectaHSV(roi,verde)) > thresholdSinal
		haVermelho =  contaPixelsDetectados(detectaHSV(roi,vermelho1,vermelho2)) > thresholdSinal
		if haAmarelo or haVerde or haVermelho:
			return True
		else:
			return False 
		
def leSemaforo(img):
    """função que detecta um semáforo e identifica que sinal esta ativo. Caso haja múltiplas regioes detectadas como semáforo, retorna a leitura da primeira região considerada válida(pela função acima)
    """
	mask = detectaHSV(img,semaforo)
	
	#lida com problemas de versao
	if cv.__version__>3:
		contours, _ = cv.findContours(mask,cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)

	else:
		_, contours, _ = cv.findContours(mask,cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)
	
	cor = (255,0,255)#cor do retangulo que encompassa semaforo 
	
	#para cada contorno detectado encontra um bounding box
	for contour in contours:
		
		x,y,largura,altura = cv.boundingRect(contour)
		roi = img[y:y+altura,x:x+largura]
		if(semaforoValido(roi,largura,altura)):
			cv.rectangle(img,(x,y),(x+largura, y+altura),cor,2)
			
			retangulo = cv.minAreaRect(contour)
			
			#lida com problemas de versao
			if cv.__version__>3:
				caixa = cv.boxPoints(retangulo)
			else:
				caixa = cv.cv.boxPoints(retangulo)
				
			caixa = np.int0(caixa)
			cv.drawContours(img,[caixa],0,cor,3)
			return sinalMaisForte(roi)
	return("Sem semáforo")

def criaROIporContorno(img,contour):
    """dado um contorno(saida de cv.findContours), cria uma ROI"""
	try:
		roi = img[contour[0][0][1]:contour[2][0][1],contour[0][0][0]:contour[2][0][0]]
		return roi
	except:
		return imagemVazia(img)

