from machine import Pin, ADC, I2C, PWM
import time
from dht import DHT11
from grove_oled import GroveOLED



dht11 = DHT11(Pin(20))
i2c = I2C(1, scl=Pin(7), sda=Pin(6), freq=100000)
oled = GroveOLED(i2c, addr= 0x3E)
pot = ADC(Pin(26))
led = Pin(16, Pin.OUT)
led.value(0)
led_state = False
last_toggle_time = 0
buzzer = PWM(Pin(18))
buzzer.freq(4000)
buzzer.duty_u16(0)



def getPotTemp():
    val_pot = pot.read_u16()
    v_max_pot = 65535
    return round(15 + (val_pot / v_max_pot) * 20, 1)
#fonction delecture de la température ambiante grâce au capteur de température
def getAmbTemp():  
    try:
        dht11.measure()
        return dht11.temperature()
    except OSError as e:
        print(f"Erreur sur le capteur: {e}")
        return None


while True:
    try:
        t = time.ticks_ms()
        ambient_temp = getAmbTemp()
        #Verification de la fonction de lecture de température du capteur
        if ambient_temp is None:
            oled.clear()
            oled.print("Erreur DHT11", 0, 0)
            time.sleep(1)
            continue
        setpoint = getPotTemp()      
        #Différnece entre la valeur envoyée par le potentionmetre et la température mesurée par le capteur
        x = ambient_temp - setpoint
        oled.clear()
        oled.print(f"Set: {setpoint:.1f}C", 0, 0)
        
        if x <= 3:
            oled.print(f"Ambient: {ambient_temp:.1f}C", 1, 0)
        else:
           
            oled.print(f"Ambient:{ambient_temp:.1f}C ALARM", 1, 0)
        
        if ambient_temp > setpoint: 
            if x > 3:             
                period_ms = 250
                buzzer.duty_u16(50000) 
                print(f"Sonnerie du buzzer")
            else:
                period_ms = 1000
                buzzer.duty_u16(0)
                           
            # Clignotement de la led
            if time.ticks_diff(t, last_toggle_time) >= period_ms:
                led_state = not led_state
                led.value(led_state)
                last_toggle_time = t
        else:        
            led.value(0)
            buzzer.duty_u16(0)
            led_state = False
            print(f" potTemp={setpoint}C AmbTemp ={ambient_temp}C")       
        # temp d attente avant la prochaine lecture
        time.sleep(1)
            
    except KeyboardInterrupt:
        led.value(0)
        buzzer.duty_u16(0)
        buzzer.deinit()
        oled.clear()
        break
        

