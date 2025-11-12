import network
import ntptime
import time
from machine import Pin, PWM


#Définition des pin et frequence du servo moteur
servo = PWM(Pin(20))  
servo.freq(50)
btn_p = Pin(16 , Pin.IN , Pin.PULL_UP)
F_H = [0,1 ,-5]
i = 1
format_24h = False


dernier_clic =0
temps_dbl_clic = 500
update_needed = False

#Information de connexion au wifi
SSID = "iPhone Keren"     
PASSWORD = "***********"  

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

def calcul_angle_12h(hour , min):
   return  (hour % 12) * 15 + min * 0.25

def calcul_angle_24h(hour , min):
     return  hour * 7.5 + min * 0.125


def click_btn (pin):
    global i, dernier_clic, format_24h , update_needed
    
    actual_time = time.ticks_ms()
    if time.ticks_diff(actual_time , dernier_clic) < temps_dbl_clic :
        format_24h  = not format_24h
        mode_str = "24 heures " if  format_24h else " 12 heures "
        print(f"Mode changé : {mode_str}")
        dernier_clic = 0
        update_needed = True
    else :
        i = (i +1 )% len(F_H)
        fuseau = F_H[i]
        signe = "+" if fuseau >= 0 else ""
        print(f"Fuseau horaire changé : UTC{signe}{fuseau}")
        dernier_clic = actual_time
        update_needed = True


btn_p.irq( trigger= Pin.IRQ_FALLING , handler = click_btn)
    
#recupération de l'heure via le serveur ntp
try:
    ntptime.settime()
except:
    print("erreur de la recupération de l'heure")


def set_servo_angle(angle):
    duty = int((angle / 180) * 8000 + 1000)
    servo.duty_u16(duty)



last_minute = -1  

while True:
   
    timezone_offset = F_H[i] * 3600
    t = time.localtime(time.time() + timezone_offset)
    hour = t[3] 
    min = t[4]
    sec = t[5]

    # Mise à du servo lorsque la minute change
    if min != last_minute or update_needed:
        last_minute = min
        update_needed = False
        #calcul de l'angle en focntion du format horaire
        if format_24h :
            angle = calcul_angle_24h(hour , min)
            mode_affichage = "24 h"
        else :
            angle = calcul_angle_12h(hour , min)
            mode_affichage= "12 h"
       
        set_servo_angle(angle)
        fuseau = F_H[i]
        signe = "+" if fuseau >= 0 else ""
        print(f"[{mode_affichage}] Il est {hour:02d}:{min:02d}:{sec:02d} (UTC{signe}{fuseau})  Angle: {angle:.2f}")
       
    time.sleep(1) 
