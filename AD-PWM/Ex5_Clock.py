import network
import ntptime
import machine
import time

# ---- CONFIG ----
SSID = "electroProjectWifi"           
PASSWORD = "B1MesureEnv" 
TIMEZONE_OFFSET = 1  # Décalage horaire en heures (ex: UTC+1)

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
    print("\n✅ Connecté ! Adresse IP :", wlan.ifconfig()[0])
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

# ---- Programme principal ----
def main():
    connect_wifi(SSID, PASSWORD)
    get_internet_time()

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

        print("Heure actuelle (UTC{:+d}): {:02d}/{:02d}/{:04d} {:02d}:{:02d}:{:02d}".format(
            TIMEZONE_OFFSET, l_day, l_month, l_year, l_hour, l_minute, l_second))
        time.sleep(1)  # Met à jour chaque seconde

# ---- Exécution ----
if __name__ == "__main__":
    main()
