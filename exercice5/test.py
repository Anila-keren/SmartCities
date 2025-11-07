import network
import ntptime
import time
from machine import Pin, PWM


#Définition des pin et frequence du servo moteur
servo = PWM(Pin(20))  
servo.freq(50)

#Information de connexion au wifi
SSID = "iPhone Keren"     
PASSWORD = "oj6q3m751f450"  

#fonction de connexion au wifi
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("Connexion échouée")
        wlan.connect(SSID, PASSWORD)
        while not wlan.isconnected():
            time.sleep(0.5)
    print("Connexion reussie")
    return wlan

#Appel de la focntion de connexion
connect_wifi()

#recupération de l'heure via le serveur ntp
try:
    ntptime.settime()
except:
    print("erreur de la recupération de l'heure")


def set_servo_angle(angle):
    #duty = int((angle / 180) * 8000 + 1000)
    duty_min= 2000
    duty_max= 8500
    duty = int(duty_min +(angle/180) * (duty_max - duty_min))
    servo.duty_u16(duty)



for h in range(13):
    angle = (12 - h) * (180 / 12) # Inversion du sens
    if angle == 180:
        angle = 0 # Pour que 12h = 0°
    print(f"Heure simulee: {h}h a angle {angle} degre")
    set_servo_angle(angle)
    time.sleep(1)
   