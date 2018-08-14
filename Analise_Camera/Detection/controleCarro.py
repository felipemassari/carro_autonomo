from gpiozero import PWMOutputDevice
from gpiozero import DigitalOutputDevice
from time import sleep
 
#Definicao de pinos
PIN_ESQUERDA = 19	# motor da esquerda
PIN_DIREITA = 6	# motor da direita
 
# Inicializacao
motorEsquerda = PWMOutputDevice(PIN_ESQUERDA, True, 0, 1000)
 
motorDireita = PWMOutputDevice(PIN_DIREITA, True, 0, 1000)

 
def parada():
	motorEsquerda.value = 0
	motorDireita.value = 0
 
def avanca():
	motorEsquerda.value = 0.6
	motorDireita.value = 0.6

def esquerda():
	motorEsquerda.value = 0.2
	motorDireita.value = 0.4
 
def direita():
	motorEsquerda.value = 0.4
	motorDireita.value = 0.2
 
