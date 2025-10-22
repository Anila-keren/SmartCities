import machine
import time

class DHT11:
    def __init__(self, pin):
        self.pin = machine.Pin(pin, machine.Pin.OUT)
        self.temperature = 0
        self.humidity = 0

    def measure(self):
        self.pin.init(machine.Pin.OUT)
        self.pin.value(0)
        time.sleep_ms(20)
        self.pin.value(1)
        self.pin.init(machine.Pin.IN)
        
        # Attend le début du signal
        t = time.ticks_us()
        while self.pin.value() == 1:
            if time.ticks_diff(time.ticks_us(), t) > 100:
                return False

        # Lis les 40 bits
        data = []
        for i in range(40):
            while self.pin.value() == 0:
                pass
            t = time.ticks_us()
            while self.pin.value() == 1:
                pass
            if time.ticks_diff(time.ticks_us(), t) > 40:
                data.append(1)
            else:
                data.append(0)

        # Convertir en octets
        bits = "".join(str(b) for b in data)
        humidity = int(bits[0:8], 2)
        temperature = int(bits[16:24], 2)
        checksum = int(bits[32:40], 2)

        if ((humidity + temperature) & 0xFF) == checksum:
            self.humidity = humidity
            self.temperature = temperature
            return True
        else:
            return False
