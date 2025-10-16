from lcd1602 import LCD1602
from machine import Pin, I2C, ADC, PWM
from utime import sleep
from dht11 import *

# Affichage LCD, lecture température, gestion LED et buzzer d'alarme

# LCD sur I2C1 (SDA=GP18, SCL=GP19)
i2c1 = I2C(1)
d = LCD1602(i2c1, 2, 16)
d.display()

# DHT11 sur D16 (GPIO16)
dht = DHT(16)

# Potentiomètre sur GP26 (A0) pour la consigne
adc = ADC(Pin(26))

# LED d'alarme sur D18
led = Pin(18, Pin.OUT)

# Buzzer sur A1 (GP27), piloté en PWM
buzzer = PWM(Pin(27))
buzzer.freq(1000)      # Fréquence par défaut
buzzer.duty_u16(0)     # Buzzer éteint au démarrage

led_state = 0  # État de la LED (0 = éteinte, 1 = allumée)

# Conversion de la valeur ADC en température de consigne (15°C à 35°C)
def adc_to_temp(adc_value):
    return 15 + (adc_value / 65535) * (35 - 15)

while True:
    # Lecture du potentiomètre et calcul de la consigne
    adc_value = adc.read_u16()
    temp_consigne = adc_to_temp(adc_value)
    # Lecture de la température mesurée
    temp_mesuree = dht.readTemperature()

    # Préparation des chaînes à afficher
    set_str = "Set: {:.1f}C ".format(temp_consigne)
    ambient_str = "Ambient: {:.1f}C ".format(temp_mesuree)
    amb_str = "Amb: {:.1f}C ".format(temp_mesuree)
    alarm_line1 = set_str + amb_str
    alarm_msg = "ALARM"

    # Gestion de l'alarme : température > consigne + 3°C
    if temp_mesuree > temp_consigne + 3:
        # Défilement de la ligne 1 et clignotement LED/buzzer + affichage ALARM
        for pos in range(0, len(alarm_line1) - 15):
            d.clear()
            d.setCursor(0, 0)
            d.print(alarm_line1[pos:pos+16])
            d.setCursor(0, 1)
            d.print(alarm_msg)
            led.value(1)
            buzzer.duty_u16(32768)  # Active le buzzer (50% PWM)
            buzzer.freq(2000)       # Fréquence d'alarme (2 kHz)
            sleep(0.3)
            d.setCursor(0, 1)
            d.print("     ")  # Efface ALARM
            led.value(0)
            buzzer.duty_u16(0)      # Coupe le buzzer
            sleep(0.3)
            # Mise à jour des valeurs pour sortir de l'alarme si besoin
            adc_value = adc.read_u16()
            temp_consigne = adc_to_temp(adc_value)
            temp_mesuree = dht.readTemperature()
            set_str = "Set: {:.1f}C ".format(temp_consigne)
            amb_str = "Amb: {:.1f}C ".format(temp_mesuree)
            alarm_line1 = set_str + amb_str
            if temp_mesuree <= temp_consigne + 3:
                break
    else:
        # Affichage normal : consigne et température ambiante
        d.clear()
        d.setCursor(0, 0)
        d.print(set_str)
        d.setCursor(0, 1)
        d.print(ambient_str)
        # LED clignote lentement si température > consigne
        if temp_mesuree > temp_consigne:
            led.value(led_state)
            led_state = 1 - led_state
            buzzer.duty_u16(0)  # Pas de son hors alarme
        else:
            led.value(0)
            buzzer.duty_u16(0)
            led_state = 0
        sleep(1)

