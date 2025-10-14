from machine import Pin, PWM, ADC
from time import sleep


buzzer = PWM(Pin(18))
rotary_angle_sensor = ADC(2)
btn_P = Pin(16, Pin.IN, Pin.PULL_UP)
led = Pin(20, Pin.OUT)

DO  = 1046
RE  = 1175
MI  = 1318
FA  = 1397
SOL = 1568
LA  = 1760
SI  = 1967
DO2 = 2093


melodie1 = [(DO, 0.4), (RE, 0.4), (MI, 0.4), (FA, 0.4), (SOL, 0.4), (LA, 0.4), (SI, 0.4), (DO2, 0.6)]
melodie2 = [(DO, 0.4), (MI, 0.4), (SOL, 0.4), (DO2, 0.6), (SI, 0.4), (SOL, 0.4), (RE, 0.4), (FA, 0.6)]
melodie3 = [(MI, 0.3), (MI, 0.3), (FA, 0.3), (SOL, 0.3), (SOL, 0.3), (FA, 0.3), (MI, 0.3), (RE, 0.5)]  

lst_melodies = [melodie1, melodie2, melodie3]
index = 0 
prev_btn = 1


while True:
    current_btn = btn_P.value()
    
    if prev_btn == 1 and current_btn == 0:
        index = (index + 1) % len(lst_melodies)
        print(f"c\'est la mélodie {index + 1}")
        sleep(0.3)  

    prev_btn = current_btn
    for (note, duree) in lst_melodies[index]:
        vol = rotary_angle_sensor.read_u16()  
        print(f"le volume est {vol}")
        duty = int(vol * 0.2)  
        buzzer.freq(note)
        buzzer.duty_u16(duty)
        led.toggle()  
        sleep(duree)

    buzzer.duty_u16(0)
    led.value(0)
