#encoding: utf-8
"""
    Módulo contendo apenas valores
"""
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


ledVermelho_min = np.array([152,23,175]) 
ledVermelho_max = np.array([180,115,255]) 
ledVermelho = (ledVermelho_min,ledVermelho_max)


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

