import machine
import utime

# Configuration des broches
BUTTON = machine.Pin(16, machine.Pin.IN, machine.Pin.PULL_DOWN)
LED = machine.Pin(18, machine.Pin.OUT)

# Variables pour suivre l'état
etat = 0
compteur_appuis = 0
dernier_appui = 0

def effet_transition():
    # Effet de clignotement rapide court
    for _ in range(2):
        LED.value(1)
        utime.sleep_ms(50)
        LED.value(0)
        utime.sleep_ms(50)

def gestion_bouton(pin):
    global etat, compteur_appuis, dernier_appui
    temps_actuel = utime.ticks_ms()
    
    # Debouncing - ignore les appuis trop rapprochés
    if utime.ticks_diff(temps_actuel, dernier_appui) < 200:
        return
        
    dernier_appui = temps_actuel
    compteur_appuis += 1
    
    # Change d'état tous les deux appuis
    if compteur_appuis >= 2:
        compteur_appuis = 0  # Réinitialise le compteur
        ancien_etat = etat
        etat = (etat + 1) % 3  # Cycle entre 0, 1 et 2
        effet_transition()

# Configuration de l'interruption sur front montant
BUTTON.irq(trigger=machine.Pin.IRQ_RISING, handler=gestion_bouton)

# Boucle principale
while True:
    if etat == 0:
        LED.value(0)  # LED éteinte
    elif etat == 1:
        # Clignotement lent (0.5 Hz)
        LED.value(1)
        utime.sleep(1)  # 1 seconde allumée
        LED.value(0)
        utime.sleep(1)  # 1 seconde éteinte
    elif etat == 2:
        # Clignotement rapide (2 Hz)
        LED.value(1)
        utime.sleep(0.25)  # 250ms allumée
        LED.value(0)
        utime.sleep(0.25)  # 250ms éteinte
