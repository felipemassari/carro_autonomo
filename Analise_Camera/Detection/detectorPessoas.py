import cv2

#imagem = 'teste1.jpg'
#imagem = 'teste2.jpg'
#imagem = 'teste3.jpg'
#imagem = 'teste4.jpeg'
#imagem = 'teste5.jpeg'
#imagem = 'teste6.jpeg'
#imagem = 'teste7.jpg'
imagem = 'teste8.jpeg'
#imagem = 'teste9.jpeg'

path = "./images/"

img = cv2.imread(path+imagem)
classificador = cv2.CascadeClassifier('./haarcascades/haarcascade_fullbody.xml')

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
pedestres = classificador.detectMultiScale(gray,1.005,2)

for (x,y,w,h) in pedestres:
    cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,0))

cv2.imshow('Pedestres', img)
cv2.waitKey(0)
    
