Evo ispravljenog koda za YOLO Kontrolni Server README. Fokusirao sam se na to da tvoje ime i ime mentora budu savršeno centrirani u donjem delu, uz popravljenu strukturu celog fajla.

Markdown
<div align="center">

# ⚙️ YOLO Kontrolni Server
### *Core Backend i Mrežni Gateway za Raspberry Pi 5*

[![Python](https://img.shields.io/badge/Python-3.11%2B-38bdf8?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Raspberry Pi](https://img.shields.io/badge/Hardware-RPi_5-c51a4a?style=for-the-badge&logo=raspberrypi&logoColor=white)](https://www.raspberrypi.com/)
[![WebSockets](https://img.shields.io/badge/Network-WebSockets-075985?style=for-the-badge&logo=socketdotio&logoColor=white)](https://websockets.readthedocs.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-94a3b8?style=for-the-badge)](https://opensource.org/licenses/MIT)

---

<p align="center">
  <b>Kontrolni Server</b> je srce autonomnog sistema, zadužen za orkestraciju hardverskih resursa. 
  <br>Hostovan na <b>Raspberry Pi 5</b> platformi, server omogućava ultra-brzu komunikaciju između motornih drajvera i udaljenih AI klijenata.
</p>



</div>

## 🚀 Tehničke Mogućnosti

### 🛰️ Real-Time Komunikacija
* **WebSocket Command Center:** Asinhrona obrada komandi na portu `1606` za trenutni odziv kretanja.
* **High-Speed Vision:** HTTP striming frejmova putem `/capture` endpointa (Port `1607`) uz podršku za visoki FPS.
* **Mecanum Kinematics:** Napredni algoritmi kretanja (napred, nazad, dijagonalno, rotacija u mestu).

### 📸 Vision Engineering
* **Dynamic Zoom Engine:** Digitalna uveličanja (1.0x - 3.0x) integrisana direktno u `picamera2` bez uticaja na mrežnu latenciju.
* **Stream Optimization:** MJPEG kompresija optimizovana za prenos preko Wi-Fi pristupne tačke robota.

### 🛡️ Fail-Safe Sistemi
* **Signal Handling:** Automatska neutralizacija svih GPIO izlaza pri detekciji `SIGINT` ili `SIGTERM` signala.
* **Service Persistence:** Integracija sa `systemd` osigurava maksimalnu dostupnost i automatski oporavak servisa pri pokretanju sistema.

---

## 🔌 Hardverska Mapa (GPIO)

Sistem koristi preciznu mapu pinova za kontrolu L298N/L293D drajvera:



| Komponenta | GPIO | Fizički Pin | Uloga |
| :--- | :--- | :--- | :--- |
| **Global PWM** | GPIO 18 | Pin 12 | Kontrola brzine (Speed) |
| **Motor A** | GPIO 17, 27 | Pin 11, 13 | Prednji Levi |
| **Motor B** | GPIO 22, 23 | Pin 15, 16 | Prednji Desni |
| **Motor C** | GPIO 24, 25 | Pin 18, 22 | Zadnji Levi |
| **Motor D** | GPIO 5, 6 | Pin 29, 31 | Zadnji Desni |

---

## 🛠 Instalacija i Deployment

### 1. Priprema Okruženja
```bash
sudo apt update
sudo apt install python3-picamera2 python3-lgpio
mkdir -p /home/kretanje && cd /home/kretanje
2. Virtuelno Okruženje (System Linked)
Bash
python -m venv --system-site-packages venv
source venv/bin/activate
pip install websockets aiohttp gpiozero
3. Deployment Servisa
Da bi se server pokretao automatski prilikom svakog paljenja robota, potrebno je konfigurisati systemd servis.

Bash
sudo nano /etc/systemd/system/kretanje.service
# Nalepite sadržaj kretanje-server.service fajla u editor
sudo systemctl daemon-reload
sudo systemctl enable --now kretanje.service
📊 Dijagnostika i Monitoring
Pratite telemetriju servera i logove kretanja u realnom vremenu komandom:

Bash
journalctl -u kretanje.service -f
🎨 Vizuelni Identitet
Dizajniran da bude diskretan, ali moćan:

UI Style: Headless server operacije.

Accent Color: #c51a4a (Raspberry Red) za hardverske logove.

Status: Dinamičko praćenje opterećenja procesora tokom AI analize.

<div align="center">

Autor: Danilo Stoletović  •  Mentor: Dejan Batanjac

ETŠ „Nikola Tesla“ Niš • 2026

</div>
