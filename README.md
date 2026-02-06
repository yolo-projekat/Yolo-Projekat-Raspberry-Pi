# 🤖 YOLO vozilo Control Server

Ovaj projekat omogućava daljinsko upravljanje robotom sa 4 točka putem **WebSockets** protokola, uz strimovanje slike sa kamere putem **HTTP** servera. Optimizovan je za Raspberry Pi uređaje i koristi `picamera2` za napredne funkcije poput digitalnog zumiranja.

## 📋 Karakteristike
* **Kontrola u realnom vremenu:** Preko WebSocket protokola na portu `1606`.
* **Kamera:** Pristup frejmu kamere preko HTTP rute `/capture` na portu `1607`.
* **Mecanum kretanje:** Podrška za napred, nazad, levo, desno, dijagonalno i rotaciju.
* **Dinamički Zoom:** Digitalno uveličanje slike (1.0x - 3.0x) bez prekida strima.
* **Bezbednost:** Automatsko gašenje svih motora pri prekidu skripte (SIGINT/SIGTERM).

## 🔌 GPIO Konfiguracija
Sistem koristi sledeću mapu pinova na Raspberry Pi zaglavlju:



* **Zajednički PWM (Brzina):** GPIO 18 (Pin 12)
* **Motor A (Prednji levi):** GPIO 17 (Pin 11) & GPIO 27 (Pin 13)
* **Motor B (Prednji desni):** GPIO 22 (Pin 15) & GPIO 23 (Pin 16)
* **Motor C (Zadnji levi):** GPIO 24 (Pin 18) & GPIO 25 (Pin 22)
* **Motor D (Zadnji desni):** GPIO 5 (Pin 29) & GPIO 6 (Pin 31)

---

## 🛠 Instalacija

### 1. Sistemski paketi
Potrebno je instalirati biblioteke za kontrolu GPIO pinova i kamere:
```bash
sudo apt update
sudo apt install python3-picamera2 python3-lgpio

###2. Postavljanje koda
Preporučena lokacija projekta je /home/kretanje:

Bash
mkdir -p /home/kretanje
cd /home/kretanje
# Ovde kopirajte fajl server15.py

###3. Virtuelno okruženje
Zbog zavisnosti od sistemskih drajvera, okruženje se pravi sa --system-site-packages:

Bash
python -m venv --system-site-packages venv
source venv/bin/activate
pip install websockets aiohttp gpiozero

###⚙️ Podešavanje Systemd Servisa
Da bi se server pokretao automatski prilikom svakog paljenja robota:

Kreirajte servis fajl:

Bash
sudo nano /etc/systemd/system/kretanje.service
i tu nalepite kretanje-server.service iz skripte

###Aktivirajte servis:

Bash
sudo systemctl daemon-reload
sudo systemctl enable kretanje.service
sudo systemctl start kretanje.service

###📊 Monitoring
Status servisa i logove kretanja možete pratiti komandom:

Bash
journalctl -u kretanje.service -f
