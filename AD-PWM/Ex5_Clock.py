import network
import ntptime
import machine
import time

# ---- CONFIG ----
SSID = "electroProjectWifi"           
PASSWORD = "B1MesureEnv" 
TIMEZONE_OFFSET = 1  # Décalage horaire en heures (ex: UTC+1)
# ---- Servo ----
# Pin du servo (D20 -> GPIO20)
SERVO_PIN = 20
# Fréquence standard pour servomoteur
SERVO_FREQ = 50
# Plages d'impulsion (en microsecondes) à ajuster selon le servo
SERVO_MIN_US = 500   # 0°
SERVO_MAX_US = 2500  # 180°

# ---- Connexion Wi-Fi ----
def connect_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)  # Interface Wi-Fi en mode station
    wlan.active(True)
    if not wlan.isconnected():
        print("Connexion au Wi-Fi...")
        wlan.connect(ssid, password)
        while not wlan.isconnected():
            time.sleep(0.5)
            print(".", end="")
    print("\n Connecté ! Adresse IP :", wlan.ifconfig()[0])
    return wlan

# ---- Récupération de l'heure via NTP ----
def get_internet_time():
    try:
        print("Synchronisation avec le serveur NTP...")
        ntptime.host = "pool.ntp.org"  # Serveur de temps
        ntptime.settime()  # Met à jour la RTC (horloge interne) en UTC
        print("Heure synchronisée avec NTP !")
    except Exception as e:
        print("Erreur de synchronisation :", e)

# ---- Calcul de l'angle du servo selon l'heure ----
def heure_vers_angle(heures, minutes):
    """
    Convertit l'heure en angle pour le cadran 12h :
    12h -> 0°, 6h -> 90°, 24h -> 180°
    Donc chaque heure = 15°.
    """
    heure_mod12 = heures % 12
    angle = (heure_mod12 + minutes / 60.0) * 15.0
    return angle


# Convertit un angle (0-180) en largeur d'impulsion en µs
def angle_to_pulse_us(angle):
    if angle < 0:
        angle = 0
    if angle > 180:
        angle = 180
    span = SERVO_MAX_US - SERVO_MIN_US
    return SERVO_MIN_US + (angle / 180.0) * span


# Convertit la largeur d'impulsion (µs) en duty_u16 pour machine.PWM
def pulse_us_to_duty_u16(pulse_us):
    # période = 1 / SERVO_FREQ -> en µs
    period_us = 1000000 // SERVO_FREQ
    duty_fraction = pulse_us / period_us
    return int(duty_fraction * 65535)

# ---- Programme principal ----
def main():
    connect_wifi(SSID, PASSWORD)
    get_internet_time()

    # Initialisation du servo
    try:
        servo_pin = machine.Pin(SERVO_PIN)
        servo_pwm = machine.PWM(servo_pin)
        servo_pwm.freq(SERVO_FREQ)
    except Exception as e:
        print("[servo] Impossible d'initialiser le servo:", e)
        servo_pwm = None

    rtc = machine.RTC()
    while True:
        # Récupère l’heure courante (UTC) et applique le décalage TIMEZONE_OFFSET
        (year, month, day, weekday, hour, minute, second, subsecond) = rtc.datetime()
        # Conversion via timestamp si possible pour gérer correctement les changements de jour
        try:
            ts = time.mktime((year, month, day, hour, minute, second, 0, 0))
            local_ts = ts + TIMEZONE_OFFSET * 3600
            lt = time.localtime(local_ts)
            # time.localtime retourne (year, month, mday, hour, minute, second, weekday, yearday)
            l_year, l_month, l_day, l_hour, l_minute, l_second, _, _ = lt
        except Exception:
            # Fallback naïf si mktime/localtime indisponible : ajuste l'heure uniquement
            l_year, l_month, l_day = year, month, day
            l_hour = (hour + TIMEZONE_OFFSET) % 24
            l_minute = minute
            l_second = second

        # --- Étape 2 : Calcul de l'angle du servo selon l'heure ---
        angle = heure_vers_angle(l_hour, l_minute)

        # Affichage pour vérification
        print("Heure locale (UTC{:+d}) : {:02d}:{:02d}:{:02d}  -->  Angle du servo : {:.2f}".format(
            TIMEZONE_OFFSET, l_hour, l_minute, l_second, angle))
        # Met à jour la position du servo si possible
        if servo_pwm is not None:
            pulse = angle_to_pulse_us(angle)
            duty = pulse_us_to_duty_u16(pulse)
            try:
                servo_pwm.duty_u16(duty)
            except Exception as e:
                # Certaines versions de MicroPython utilisent servo_pwm.duty() ou autre API
                try:
                    servo_pwm.duty_u16(duty >> 8)
                except Exception:
                    print("[servo] Échec mise à jour PWM:", e)

        time.sleep(1)

# ---- Exécution ----
if __name__ == "__main__":
    main()
