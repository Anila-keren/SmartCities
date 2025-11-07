from machine import Pin, ADC
from neopixel import NeoPixel
import time
import random

#Definition des Pins
np = NeoPixel(Pin(18), 1)
mic = ADC(27)

# genérer aleatoirement une couleur grâce à la bibliotheque random
def randomColor():
    return (
        random.randint(0, 255),
        random.randint(0, 255), 
        random.randint(0, 255)
    )

# Parametres de détection des battements
seuil = 1.3  
t_min = 100             
n = 20            

# Variables globales
last_beat = 0
sound_list = []
min_level = 65535
max_level = 0

# Variables pour le calcul des BPM
beat_time_list = []  
bpm_list = []  
last_minute_save = time.ticks_ms()  
current_bpm = 0

#Fonction pour retourner le niveau du capteur son
def get_sound_level():
    return mic.read_u16()

#fonction pour detecter un battement basé sur un pic sonore
def detect_beat(current_level, avg_level): 
    global last_beat, min_level, max_level
    # Mise à jour des niveaux min/max 
    min_level = min(min_level, current_level)
    max_level = max(max_level, current_level) 
    current_time = time.ticks_ms()
    
    # Détecte un pic si le niveau actuel dépasse la moyenne × multiplicateur
    threshold = avg_level * seuil
    if current_level > threshold:
        if time.ticks_diff(current_time, last_beat) > t_min:
            last_beat = current_time
            return True
    
    return False
#Mise à jour de la moyenne mobile des échantillons
def update_average(sound_list, new_value):
    sound_list.append(new_value)
    if len(sound_list) > n:
        sound_list.pop(0)
    
    return sum(sound_list) // len(sound_list) if sound_list else 0

 #Change la couleur de la LED RGB"""
def changeColor(color):
    np[0] = color
    np.write()


#fonction de Calcul du BPM grâce aux  10 derniers battements détectés
def calculate_bpm():
    global beat_time_list, current_bpm
    current_time = time.ticks_ms()
    beat_time_list = [t for t in beat_time_list if time.ticks_diff(current_time, t) < 10000]
    # condition sur le nombre de battement
    if len(beat_time_list) < 2:
        return 0
    intervals = []
    for i in range(1, len(beat_time_list)):
        interval = time.ticks_diff(beat_time_list[i], beat_time_list[i-1])
        intervals.append(interval)
   
    # moyenne des intervalles en ms
    avg_interval = sum(intervals) / len(intervals)
    # Convertion en BPM 
    if avg_interval > 0:
        bpm = 60000 / avg_interval 
        current_bpm = int(bpm)
        return current_bpm
    
    return 0

#Ecriture et sauvegarde dans le fichier 
def log_bpm():
    global bpm_list, last_minute_save
    if len(bpm_list) == 0:
        print("Aucun BPM à sauvegarder cette minute")
        last_minute_save = time.ticks_ms()
        return
    
    # Moyenne des BPM de la dernière minute
    avg_bpm = sum(bpm_list) / len(bpm_list)
    current_time = time.ticks_ms()
    elapsed_minutes = time.ticks_diff(current_time, 0) // 60000
    
    try:
        with open('exercice4.txt', 'a') as f:
            timestamp = f"Minute {elapsed_minutes}"
            line = f"{timestamp} - BPM moyen: {avg_bpm:.1f} (basé sur {len(bpm_list)} mesures)\n"
            f.write(line)
            f.flush()  
        print(" bpm moyenne Sauvegardé")
        
        try:
            import os
            files = os.listdir()
            if 'exercice4.txt' in files:
                print("ce fichier existe bien")
            else:
                print("Abscence du fichier exercice4!")
        except:
            pass
            
    except Exception as e:
        print(f"ERREUR lors de l'écriture: {e}")
    
    # Réinitialise l'historique pour la prochaine minute
    bpm_list.clear()
    last_minute_save = current_time

changeColor((0, 0, 0))

# Crée le fichier BPM dès le démarrage pour vérifier l'accès
try:
    with open('exercice4.txt', 'a') as f:
        f.write("Valeur BPM Moyen\n")
except Exception as e:
    print(f" ERREUR: Impossible de créer le fichier: {e}")



calibration_sound_list = []
calibration_start = time.ticks_ms()

while time.ticks_diff(time.ticks_ms(), calibration_start) < 2000:
    level = get_sound_level()
    calibration_sound_list.append(level)
    time.sleep_ms(10)

# Initialise la moyenne avec les données de calibration
sound_list = calibration_sound_list[-n:]
baseline = sum(sound_list) // len(sound_list)

print(f"valeurMin: {min(calibration_sound_list)}, valeurMax: {max(calibration_sound_list)}")


try:
    i = 0
    while True:
        sound_level = get_sound_level()
        avg_level = update_average(sound_list, sound_level)
        
        i += 1
        if i % 50 == 0:
            print(f"Niveau: {sound_level}, Moyenne: {avg_level}, Seuil: {int(avg_level * seuil)}, BPM actuel: {current_bpm}")
        
        if detect_beat(sound_level, avg_level):
            beat_time = time.ticks_ms()
            beat_time_list.append(beat_time)
            #appel de la focntion du calcul du bpm
            bpm = calculate_bpm()
        
            if bpm > 30 and bpm < 600:  # uniquement les BPM entre 30 et 600
                bpm_list.append(bpm)
    
            color = randomColor()
            changeColor(color)
            print(f" RGB{color}, BPM: {bpm}")
        
        # faire une sauvegarde apres une minute
        if time.ticks_diff(time.ticks_ms(), last_minute_save) >= 60000: 
            log_bpm()
        
        time.sleep_ms(10)
        
except KeyboardInterrupt:
   #eteinte de la rgb à la fin
    changeColor((0, 0, 0))  
    # Sauvegarde les données restantes avant de quitter
    if len(bpm_list) > 0:
        log_bpm()
    
   