<div align="center">

# ⚙️ YOLO Kontrolni Server
### *Core Backend i Mrežni Gateway za Raspberry Pi 5*

[![Python](https://img.shields.io/badge/Python-3.11%2B-38bdf8?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Raspberry Pi](https://img.shields.io/badge/Hardware-RPi_5-c51a4a?style=for-the-badge&logo=raspberrypi&logoColor=white)](https://www.raspberrypi.com/)
[![WebRTC](https://img.shields.io/badge/Network-WebRTC-075985?style=for-the-badge&logo=webrtc&logoColor=white)](https://webrtc.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-94a3b8?style=for-the-badge)](https://opensource.org/licenses/MIT)

---

<p align="center">
  <b>YOLO Kontrolni Server</b> je srce autonomnog sistema, zadužen za orkestraciju hardverskih resursa.
  <br>Hostovan na <b>Raspberry Pi 5</b> platformi, server omogućava ultra-brzu komunikaciju između drajvera i udaljenih AI klijenata.
</p>

</div>

## 🚀 Ključni Moduli

### 🛰️ Real-Time Komunikacija
* **UDP Command Center:** Ultra-brza obrada komandi kretanja preko UDP protokola na portu `1606`.
* **WebRTC Vision Engine:** Optimizovan video striming niskih latencija putem WebRTC `/offer` endpointa (Port `1607`).
* **Mecanum Kinematics:** Napredni algoritmi za kontrolu kretanja motora sa O(1) vremenskom kompleksnošću.

### 📸 Vision Engineering
* **Shared Camera Track:** Istovremeno opsluživanje N WebRTC klijenata bez konflikata i blokiranja kamere zahvaljujući `asyncio` izolaciji memorije (`PyAV`).
* **Stream Optimization:** RGB24 video prenos optimizovan za direktan rad sa AI procesiranjem i analizom.

### 🛡️ Fail-Safe Sistemi
* **Motor Watchdog:** Otkazivanje UDP mrežnog paketa aktivira sigurnosno zaustavljanje robota kako bi se sprečili sudari pri gubitku signala ("Runaway Robot" prevencija).
* **Signal Handling:** Automatska neutralizacija svih GPIO izlaza pri detekciji `SIGINT` ili `SIGTERM` signala.
* **Service Persistence:** Integracija sa `systemd` osigurava maksimalnu dostupnost i automatski oporavak servisa pri boot-u.

---

## 🛠 Tehnološki Stack

| Komponenta | Tehnologija | Uloga |
| :--- | :--- | :--- |
| **OS Platforma** | Raspberry Pi OS (64-bit) | Hardversko jezgro sistema |
| **Language** | Python 3.11+ | Glavna asinhrona logika (`asyncio`) |
| **Camera Core** | Libcamera / Picamera2 / PyAV | Video capture i obrada |
| **GPIO Control** | LGPIO / Gpiozero | Upravljanje motorima |
| **Networking** | UDP & WebRTC (`aiortc`) & Aiohttp | Mrežni gateway |

---

## 🔌 Hardverska Konfiguracija

Sistem koristi preciznu mapu pinova za kontrolu motornih drajvera:

* **Global PWM:** GPIO 18 (Kontrola brzine)
* **Motor A / B:** Prednja osovina (GPIO 17, 27 / 22, 23)
* **Motor C / D:** Zadnja osovina (GPIO 24, 25 / 5, 6)

---

## 🔧 Deployment Servisa

Da bi server radio autonomno, koristi se `systemd` automatizacija. Pratite ove korake u terminalu:

> [!IMPORTANT]
> Proverite status servisa nakon instalacije komandom: `systemctl status kretanje.service`


🎨 Vizuelni Identitet
Dizajniran da bude diskretan, ali moćan:

UI Style: Headless server operacije (CLI fokus).

Accent Color: #c51a4a (Raspberry Red).

Status: Dinamičko praćenje opterećenja procesora i temperature senzora.

<div align="center">

Autor: Danilo Stoletović • Mentor: Dejan Batanjac

ETŠ „Nikola Tesla“ Niš • 2026

</div>
