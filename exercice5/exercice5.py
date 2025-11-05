import network
import ntptime
import time
from machine import Pin, PWM


#Définition des pin et frequence 
servo = PWM(Pin(20))  
servo.freq(50)

#Information de connexion au wifi de mon gsm
SSID = "iPhone Keren"     
PASSWORD = "************"  

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
    duty = int((angle / 180) * 8000 + 1000)
    servo.duty_u16(duty)

#calcul de l'heure locale à partir de l'heure UTC
timezone_offset = 1 * 3600

last_minute = -1  

while True:
    t = time.localtime(time.time() + timezone_offset)
    hour = t[3] % 12
    min = t[4]

    # Mise à du servo lorsque la minute change
    if min != last_minute:
        last_minute = min
        
        #angle du servo moteur
        angle = hour * 15 + min * 0.25
        set_servo_angle(angle)
        print(f"Il est  {t[3]:02d}:{min:02d}  ce qui correspond à cette mesure d'angle{angle:.2f}")
    
    time.sleep(1) 
