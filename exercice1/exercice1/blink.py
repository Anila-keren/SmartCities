import machine  
from machine import Pin , PWM , Timer
import time
BUTTON = machine.Pin(20,machine.Pin.IN , machine.Pin.PULL_DOWN)
LED = machine.Pin(16,machine.Pin.OUT)
freq1 = 0.5
freq2 = 5


TIMER = Timer()

button_pressed = False
i = 0
def toggle_led(_):
    LED.toggle()

while True:
    val = BUTTON.value()
   # print(f'l\'état du bouton est {val}')
    if val == 1 and button_pressed == False:
        i += 1
        if i > 2:
            i=0
        button_pressed = True
        if i == 0:
          TIMER.deinit()
          LED.off()
          print("Etat initial la led est eteinte")
        elif i == 1:
            period_ms = int(1000 / (freq1 * 2))
            TIMER.init(period=period_ms, mode=Timer.PERIODIC, callback=toggle_led)
            print("La led clignote apres chaque 2 secondes")
        elif i == 2:
            period_ms = int(1000 / (freq2 * 2))
            TIMER.init(period=period_ms, mode=Timer.PERIODIC, callback=toggle_led)
            print("la led clignote plus vite")
            
    elif val == 0 and button_pressed == True:
        button_pressed = False

    time.sleep(0.01)