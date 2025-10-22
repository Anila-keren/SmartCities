from machine import I2C
import time

class GroveOLED:
    """Driver pour écran Grove OLED 16x2"""
    
    def __init__(self, i2c, addr=0x3C):
        self.i2c = i2c
        self.addr = addr
        self.init_display()
   
    def init_display(self):
        """Initialise l'écran Grove OLED"""
        commands = [
            0x2A, 0x71, 0x5C, 0x28, 0x08, 0x2A, 0x79, 0xD5, 0x70,
            0x78, 0x09, 0x06, 0x72, 0x00, 0x2A, 0x79, 0xDA, 0x10,
            0xDC, 0x00, 0x81, 0x7F, 0xD9, 0xF1, 0xDB, 0x40, 0x78,
            0x28, 0x01, 0x80, 0x0C
        ]
        for cmd in commands:
            self.write_command(cmd)
            time.sleep_ms(5)
   
    def write_command(self, cmd):
        """Envoie une commande à l'écran"""
        self.i2c.writeto(self.addr, bytes([0x00, cmd]))
   
    def write_data(self, data):
        """Envoie des données à l'écran"""
        self.i2c.writeto(self.addr, bytes([0x40, data]))
   
    def clear(self):
        """Efface l'écran"""
        self.write_command(0x01)
        time.sleep_ms(2)
   
    def set_cursor(self, row, col):
        """Positionne le curseur (row: 0-1, col: 0-15)"""
        addr = 0x80 if row == 0 else 0xC0
        self.write_command(addr + col)
   
    def print(self, text, row=0, col=0):
        """Affiche du texte à la position spécifiée"""
        self.set_cursor(row, col)
        for char in text[:16]:  # Maximum 16 caractères par ligne
            self.write_data(ord(char))