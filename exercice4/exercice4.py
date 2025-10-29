from machine import Pin, ADC
from neopixel import NeoPixel
import time, random


PIN_LED = 18
N_LEDS = 1
MIC_PIN = 27
np = NeoPixel(Pin(18), 1)
mic = ADC(27)

t1 = time.ticks_ms()
delay = 200  
list_signal = [0]*15 #  stockage des 15 dernieres valeurs lu par le capteur de son 

#Fonction permettant de genérer aleatoirement une couleur
def randomColor():
    return (
        random.randint(0,255),
        random.randint(0,255), 
        random.randint(0,255)
    )

try:
    while True:
        ss_val = mic.read_u16()
        moyenne = sum(list_signal)/len(list_signal)  #calcul de la moyenne du bruit à partir de la liste
        if ss_val > moyenne + 3000: #detection du pic sonore élévé
            t2 = time.ticks_ms()
            if time.ticks_diff(t2, t1) > delay:
                t1 = t2
                color = randomColor()
                np[0] = color
                np.write()
                print(ss_val, color)
        list_signal.pop(0)
        list_signal.append(ss_val)  
        time.sleep(0.01)
#eteindre la led rgb a la fin 
except KeyboardInterrupt:
    np[0] = (0,0,0)
    np.write()
