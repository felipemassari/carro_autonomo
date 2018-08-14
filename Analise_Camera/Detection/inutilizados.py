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
