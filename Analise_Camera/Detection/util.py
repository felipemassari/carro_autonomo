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
semaforo_max = np.array([180,255,60])
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

luzVerde_min = np.array([54,94,150])
luzVerde_max = np.array([80,164,255])
verde = (luzVerde_min,luzVerde_max)

#valores para calibrar depois
fatorDesvio = 1.0 #usado para calcular o valor enviado aos motores
qtdeRuaEsperada = 70000 #qtos pixels de rua se espera ver
thresholdSemaforo = 800 #qtos pixels para se considerar um semaforo
thresholdSinal = 400 #qtos pixels para se considerar sinal do semaforo

#cor detectada - em branco
#0-preto / 1-branco


#funcao que recebe uma imagem e varios intervalos e retorna em branco a deteccao de todos os intervalos na imagem
def detectaHSV(img,*intervalos):
    hsv = cv.cvtColor(img,cv.COLOR_BGR2HSV)
    mask = imagemVazia(img)
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

#verifica se existe um objeto na pista, o criterio por enquanto eh se
#muito da rua estiver bloqueado entao tem um obstaculo, considerando 
#a ROI da camera que enxerga a pista

def haObstaculoNaPista(img):
	roiRua = ROIporPorcentagem(img,50,100,0,100)
	detRua = detectaHSV(roiRua,rua)
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
#Por exemplo a metade superior da imagem seria (img,0,50,0,100)
def ROIporPorcentagem(img,y1,y2,x1,x2):
    yMax, xMax = img.shape[0:2]
    return img[(yMax*y1)//100:(yMax*y2)//100,(xMax*x1)//100:(xMax*x2)//100]

#retorna o valor do pixel mais proximo 
def pixelPorPorcentagem(img,y,x):
	yMax, xMax = img.shape[0:2]
	return img[yMax*y//100,xMax*x//100]

#retorna limiar para um canal, recebe duas regioes com 3 canais
def limiarOtimoCanal(roi1,roi2):
	r1c1,r1c2,r1c3 = cv.split(roi1)
	r2c1,r2c2,r2c3 = cv.split(roi2)
	pass

#retorna o limiar para um canal pelo
def limiarOtimoCanalPixel(canal):
	
	valorPixelDireita = pixelPorPorcentagem(canal,50,25)
	valorPixelEsquerda = pixelPorPorcentagem(canal,50,75)
	return valorPixelDireita//2+valorPixelEsquerda//2

#faz a calibracao usando funcao acima, retorna limiar que separa cor da
#direita da tela e da esquerda 
def calibraHSV(img):
	hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
	H,S,V = cv.split(hsv)

	thH = limiarOtimoCanal(H)
	thS = limiarOtimoCanal(S)
	thV = limiarOtimoCanal(V)

	direita = (np.array([0,0,0]), np.array([thH,thS,thV]))  
	esquerda = (np.array([thH,thS,thV]), np.array([180,255,255]))  

	return esquerda, direita
	
#retorna um booleano que indica se pelo menos um pedestre foi detectado e
#a imagem com retangulos indicando os pedestres detectados
def detectaPedestres(img):
	gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
	classificador = cv.CascadeClassifier('./haarcascades/haarcascade_fullbody.xml')
	pedestres =[]
	pedestres = classificador.detectMultiScale(gray,1.1,3)

	for (x,y,w,h) in pedestres:
		cv.rectangle(img,(x,y),(x+w,y+h),(255,0,255))

	pedestreDetectado = False
	if len(pedestres)!=0:
		pedestreDetectado = True
		
	return pedestreDetectado,img
	
#retorna um booleano que indica se pelo menos um carro foi detectado e
#a imagem com retangulos indicando os carros detectados
def detectaCarros(img):
	gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
	#haarcascade de https://github.com/andrewssobral/vehicle_detection_haarcascades
	classificador = cv.CascadeClassifier('./haarcascades/cars.xml')
	carros =[]
	carros = classificador.detectMultiScale(gray,1.05,2)

	for (x,y,w,h) in carros:
		cv.rectangle(img,(x,y),(x+w,y+h),(255,0,0))

	carroDetectado = False
	if len(carros)!=0:
		carroDetectado = True
		
	return carroDetectado,img
	
#retorna uma imagem vazia (todos os pixels pretos) com as mesmas dimensoes de img
def imagemVazia(img):
	return np.zeros((img.shape[0],img.shape[1]),np.uint8)
	
#Calcula numero de pixels dado um contorno
def numeroDePixelsEmContorno(contour):
	dx = contour[2][0][0] - contour[0][0][0]
	dy = contour[2][0][1] - contour[0][0][1]
	return dy*dx

#mostra imagem e espera apertar uma tecla, apenas para debugar
def mostraImg(img):
	cv.imshow("teste",img)
	cv.waitKey(0)

#retorna o sinal de semaforo detectado mais provavel
def sinalMaisForte(roi):
	detVermelho = contaPixelsDetectados(detectaHSV(roi,vermelho1,vermelho2))
	detAmarelo = contaPixelsDetectados(detectaHSV(roi,amarelo))
	detVerde = contaPixelsDetectados(detectaHSV(roi,verde))
	if detVermelho>detAmarelo and detVermelho>detVerde:
		return "Sinal vermelho"
	if detAmarelo>detVermelho and detAmarelo>detVerde:
		return "Sinal amarelo"
	if detVerde>detVermelho and detVerde>detAmarelo:
		return "Sinal verde"
	return "Sem sinal"
	
#um semaforo valido eh aquele que possui vermelho, amarelo ou verde dentro #da regiao compreendida por ele. Esta funcao recebe a ROI do semaforo
#e verifica se ha um minimo dessas cores e se sim, retorna True
#Eh necessario tambem um minimo de pixels de semaforo para ser valido
def semaforoValido(roi,largura,altura):
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
		
#funcao que detecta um semaforo e identifica que sinal esta ativo
#Caso haja multiplas regioes detectadas como semaforo, retorna a 
#leitura da primeira regiao considerada valida(funcao acima)
def leSemaforo(img):
	mask = detectaHSV(img,semaforo)
	_, contours, _ = cv.findContours(mask,cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)
	cor = (255,0,255)
	
	#para cada contorno detectado encontra um bounding box
	for contour in contours:
		#print(contour)
		#print("1")
		
		
		x,y,largura,altura = cv.boundingRect(contour)
		roi = img[y:y+altura,x:x+largura]
		if(semaforoValido(roi,largura,altura)):
			cv.rectangle(img,(x,y),(x+largura, y+altura),cor,2)
			
			retangulo = cv.minAreaRect(contour)
			caixa = cv.boxPoints(retangulo)
			caixa = np.int0(caixa)
			cv.drawContours(img,[caixa],0,cor,3)
			return sinalMaisForte(roi)
	#roi = img[y:y+altura,x:x+largura]
	
	return("Sem semaforo")


'''
def leSemaforo(img):
	mask = detectaHSV(img,semaforo)
	cv.imshow("mask",mask)
	cv.waitKey(0)
	_, contours, _ = cv.findContours(mask,cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)
	
	for contour in contours:
		print("--------")
		print(contour)
		if (contour[0].size)
		roi = criaROIporContorno(img,contour)
		if semaforoValido(roi, contour):
			return sinalMaisForte(roi)
			
			#cv.rectangle(img2,tuple(contour[0][0]),tuple(contour[2][0]),(255,255,255),-1)
	#cv.imshow("asd",img2)
	#cv.waitKey(0)
'''
#dado um contorno(saida de cv.findContours), cria uma ROI
def criaROIporContorno(img,contour):
	try:
		roi = img[contour[0][0][1]:contour[2][0][1],contour[0][0][0]:contour[2][0][0]]
		return roi
	except:
		return imagemVazia(img)


'''
Abaixo estao funcoes que nao serao utilizadas mas vou deixar aqui por enquanto caso acabem tendo alguma utilidade
'''
def ROISemaforo(img):
	mask = detectaHSV(img,semaforo)
	contours, hierarchy = cv.findContours(mask,cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)
	#img2 = desenhaContornos(img, contours, hierarchy)
	
	cv.imshow("asd",img2)
	cv.waitKey(0)
	
def desenhaContornos(img, contours, hierarchy):
	index = 0
	image = np.zeros(img.shape, np.uint8)
	#print(contours[0])
	cor = (255,255,255)
	
	#image = np.zeros((img.shape[0],img.shape[1]), np.uint32)
	#caso onde eh encontrada apenas um contorno
	if hierarchy[0][index][0]==-1:
		cv.drawContours(image,contours,0,cor)
	else:
		#caso onde eh encontrado mais de um contorno
		while (index>=0):
		
			index = hierarchy[0][index][0]
			#print(index)
		
			if index>=0:
				cv.drawContours(image,contours,index,cor) 

		'''
		image = cv.drawContours(image,contours,index,(0,0,0),3)
		'''
	return np.float32(image)
