from ws2812 import WS2812
from machine import Pin,ADC
import utime 

BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
WHITE = (255, 255, 255)
COLORS = [RED, GREEN, BLUE, YELLOW, CYAN, MAGENTA, WHITE]

led = WS2812(18, 1)
mic = ADC(Pin(27))  # Microphone sur A1 (GP27)

# Paramètres pour la détection des battements
WINDOW_SIZE = 10          # Nombre d'échantillons pour la moyenne mobile
THRESHOLD_FACTOR = 1.5    # Facteur multiplicateur pour le seuil
MIN_INTERVAL = 100        # Intervalle minimum entre les battements (ms)
NOISE_FLOOR = 30000       # Niveau de bruit minimum

# Variables pour le traitement du signal
sample_window = []        # Fenêtre glissante pour les échantillons
last_beat_time = 0       # Horodatage du dernier battement détecté
running_average = 0       # Moyenne mobile des échantillons

def detect_beat(sample, current_time):
    global sample_window, last_beat_time, running_average
    
    # Ajoute l'échantillon à la fenêtre et maintient la taille
    sample_window.append(sample)
    if len(sample_window) > WINDOW_SIZE:
        sample_window.pop(0)
    
    # Calcule la moyenne mobile
    running_average = sum(sample_window) / len(sample_window)
    
    # Calcule le seuil dynamique
    threshold = running_average * THRESHOLD_FACTOR
    
    # Vérifie si on a un battement
    is_beat = False
    if (sample > threshold and                        # L'échantillon dépasse le seuil
        sample > NOISE_FLOOR and                      # Au-dessus du niveau de bruit
        current_time - last_beat_time > MIN_INTERVAL):# Respect de l'intervalle minimum
        
        is_beat = True
        last_beat_time = current_time
    
    return is_beat, threshold, running_average

while True:
    current_time = utime.ticks_ms()
    mic_value = mic.read_u16()
    
    # Détecte si un battement est présent
    beat_detected, threshold, average = detect_beat(mic_value, current_time)
    
    # Affiche les informations de débogage
    print("Val:", mic_value, "Moy:", int(average), "Seuil:", int(threshold), "Beat:", beat_detected)
    
    # Change la couleur de la LED sur un battement
    if beat_detected:
        led.pixels_fill(RED)
    else:
        led.pixels_fill(BLACK)
    led.pixels_show()
    
    utime.sleep_ms(10)  # Échantillonnage à ~100Hz
    utime.sleep(0.1)

