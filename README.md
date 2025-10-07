# 🌆 Smartcities

Bienvenue dans le repository **Smartcities** !  
Ce projet a pour objectif de découvrir et de développer des applications autour des **villes intelligentes**, en utilisant le **Raspberry Pi Pico W** et le langage **MicroPython**.

---

## 🧰 Matériel utilisé

### 🔹 Raspberry Pi Pico W  
Le **Raspberry Pi Pico W** est une carte microcontrôleur compacte équipée d’un processeur **RP2040** et d’un module Wi-Fi **CYW43439**.  
Il permet la création de projets embarqués connectés de manière simple et économique.

**Caractéristiques principales :**
- Processeur **RP2040** double cœur ARM Cortex-M0+  
- 264 KB de SRAM  
- 2 MB de mémoire Flash  
- Connectivité **Wi-Fi 2,4 GHz**  
- 26 broches GPIO utilisables  
- Interfaces : UART, SPI, I2C, ADC, PWM  

![Brochage du Raspberry Pi Pico W](https://www.raspberrypi.com/documentation/microcontrollers/images/pico-pinout.svg)

---

## 🧑‍💻 Environnement de développement

### 🔹 MicroPython  
**MicroPython** est une version allégée de **Python 3** spécialement conçue pour les microcontrôleurs.  
Elle permet de programmer facilement la carte Pico W avec une syntaxe simple et rapide à prendre en main.

**Avantages :**
- Syntaxe Python standard  
- Exécution directe sur la carte  
- Contrôle des GPIO et des périphériques  
- Documentation riche et communauté active  

---

## 📁 Structure du repository

Le projet est organisé en plusieurs **sous-répertoires**, chacun dédié à un thème ou une expérimentation précise.  
Chaque dossier contient :
- Un fichier **README.md** explicatif  
- Le **code source**  
- Les **ressources associées** (datasheets, images, explications)

### 🔗 Sous-répertoires :

- [GPIO](./GPIO) : LED simple, bouton-poussoir, interruption  
- [AD-PWM](./AD-PWM) : lecture du potentiomètre, PWM (LED, musique, servo)  
- [LCD](./LCD) : documentation de la librairie LCD, affichage de la valeur d’un potentiomètre  
- [LED_neo](./LED_neo) : utilisation des LEDs NeoPixel, documentation, effet arc-en-ciel  
- [sensors](./sensors) : capteurs de température, humidité, luminosité, PIR  
- [network](./network) : accès réseau avec le RPi Pico W  

