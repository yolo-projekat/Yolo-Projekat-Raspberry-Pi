<div align="center">

# ⚙️ YOLO Kontrolni Server
### *Core Backend i Mrežni Gateway za Raspberry Pi 5*

[![Python](https://img.shields.io/badge/Python-3.11%2B-38bdf8?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Raspberry Pi](https://img.shields.io/badge/Hardware-RPi_5-c51a4a?style=for-the-badge&logo=raspberrypi&logoColor=white)](https://www.raspberrypi.com/)
[![WebSockets](https://img.shields.io/badge/Network-WebSockets-075985?style=for-the-badge&logo=socketdotio&logoColor=white)](https://websockets.readthedocs.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-94a3b8?style=for-the-badge)](https://opensource.org/licenses/MIT)

---

<p align="center">
  <b>YOLO Kontrolni Server</b> je srce autonomnog sistema, zadužen za orkestraciju hardverskih resursa.
  <br>Hostovan na <b>Raspberry Pi 5</b> platformi, server omogućava ultra-brzu komunikaciju između drajvera i udaljenih AI klijenata.
</p>

</div>

## 🚀 Ključni Moduli

### 🛰️ Real-Time Komunikacija
* **WebSocket Command Center:** Asinhrona obrada i distribucija komandi kretanja na portu `1606`.
* **High-Speed Vision:** Optimizovan HTTP striming frejmova putem `/capture` endpointa (Port `1607`).
* **Mecanum Kinematics:** Napredni algoritmi za kontrolu kretanja (napred, nazad, dijagonalno i rotacija).

### 📸 Vision Engineering
* **Dynamic Zoom Engine:** Digitalna uveličanja (1.0x - 3.0x) integrisana direktno u `picamera2` bez uticaja na latenciju.
* **Stream Optimization:** MJPEG kompresija prilagođena za stabilan prenos preko Wi-Fi pristupne tačke robota.

### 🛡️ Fail-Safe Sistemi
* **Signal Handling:** Automatska neutralizacija svih GPIO izlaza pri detekciji `SIGINT` ili `SIGTERM` signala.
* **Service Persistence:** Integracija sa `systemd` osigurava maksimalnu dostupnost i automatski oporavak servisa pri boot-u.

---

## 🛠 Tehnološki Stack

| Komponenta | Tehnologija | Uloga |
| :--- | :--- | :--- |
| **OS Platforma** | Raspberry Pi OS (64-bit) | Hardversko jezgro sistema |
| **Language** | Python 3.11+ | Glavna asinhrona logika |
| **Camera Core** | Libcamera / Picamera2 | Video capture i obrada |
| **GPIO Control** | LGPIO / Gpiozero | Upravljanje motorima |
| **Networking** | WebSockets & Aiohttp | Mrežni gateway |

---

## 🔌 Hardverska Konfiguracija

Sistem koristi preciznu mapu pinova za kontrolu motornih drajvera:



* **Global PWM:** GPIO 18 (Kontrola brzine)
* **Motor A / B:** Prednja osovina (GPIO 17, 27 / 22, 23)
* **Motor C / D:** Zadnja osovina (GPIO 24, 25 / 5, 6)

---

## 🔧 Deployment Servisa

Da bi server radio autonomno, koristi se `systemd` automatizacija:

> [!IMPORTANT]
> Proverite status servisa nakon instalacije komandom: `systemctl status kretanje.service`

```bash
# Pokretanje i monitoring servisa
sudo systemctl daemon-reload
sudo systemctl enable --now kretanje.service
journalctl -u kretanje.service -f
🎨 Vizuelni Identitet
<p> ᴅɪᴢᴀᴊɴɪʀᴀɴ ᴅᴀ ʙᴜᴅᴇ ᴅɪsᴋʀᴇᴛᴀɴ, ᴀʟɪ ᴍᴏćᴀɴ.


• ᴜɪ sᴛʏʟᴇ: ʜᴇᴀᴅʟᴇss sᴇʀᴠᴇʀ ᴏᴘᴇʀᴀᴄɪᴊᴇ.


• ᴀᴄᴄᴇɴᴛ ᴄᴏʟᴏʀ: #ᴄ51ᴀ4ᴀ (ʀᴀsᴘʙᴇʀʀʏ ʀᴇᴅ).


• sᴛᴀᴛᴜs: ᴅɪɴᴀᴍɪčᴋᴏ ᴘʀᴀćᴇɴᴊᴇ ᴏᴘᴛᴇʀᴇćᴇɴᴊᴀ ᴘʀᴏᴄᴇsᴏʀᴀ. </p>

<div align="center">

Autor: Danilo Stoletović • Mentor: Dejan Batanjac

ETŠ „Nikola Tesla“ Niš • 2026

</div>
