<div align="center">

# 🗄️ [ARHIVIRANO] YOLO Kontrolni Server
### *Istorijski Bare-Metal Backend za Raspberry Pi 5*

> [!WARNING]  
> **STATUS REPOZITORIJUMA: ARHIVIRAN (DEPRECATED)**
> 
> Ovaj repozitorijum sadrži prvobitnu *bare-metal* verziju kontrolnog servera (pokretanu direktno na host operativnom sistemu) i više se ne održava. Kompletan backend je sada **dokerizovan (Docker)** i premešten u novi, odvojeni repozitorijum.
>
> **Inženjersko objašnjenje tranzicije:** Iako je direktno pokretanje asinhronih Python skripti uz `systemd` servise funkcionisalo, održavanje stabilnosti sistema postalo je nemoguće zbog specifičnih zahteva hardverskih biblioteka i Python okruženja.
> 
> **Edukativni i infrastrukturni benefiti:** Prelazak na Docker arhitekturu donosi izolovan i predvidljiv *deployment*. Učenicima je omogućeno bezbedno eksperimentisanje sa AI i mrežnim kodom unutar sandbox kontejnera, bez rizika od oštećenja glavnog operativnog sistema.

[![Python](https://img.shields.io/badge/Python-3.11%2B-38bdf8?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Docker](https://img.shields.io/badge/Target-Docker-2496ed?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![Raspberry Pi](https://img.shields.io/badge/Hardware-RPi_5-c51a4a?style=for-the-badge&logo=raspberrypi&logoColor=white)](https://www.raspberrypi.com/)
[![WebRTC](https://img.shields.io/badge/Network-WebRTC-075985?style=for-the-badge&logo=webrtc&logoColor=white)](https://webrtc.org/)

---

<p align="center">
  <i>Istorijska arhiva: Originalni kod za mrežni gateway i hardversku orkestraciju na Raspberry Pi 5 platformi pre prelaska na kontejnerizaciju.</i>
</p>

</div>

## ⚠️ Problem: Python Dependency Hell

Glavni razlog za napuštanje ovog pristupa je tzv. **"Dependency Hell"** specifičan za rad sa ugrađenim (embedded) sistemima i Python bibliotekama:

* **Sistemski konflikti:** Biblioteke poput `aiortc` zahtevaju specifične verzije `OpenSSL` i `PyAV` (koja se oslanja na `FFmpeg` shared objekte). Ažuriranje sistemskog paketa na Raspberry Pi OS-u često bi dovelo do pucanja Python linkova, čineći server neupotrebljivim.
* **PEP 668 Restrikcije:** Moderni Debian-bazirani sistemi (Bookworm+) blokiraju `pip install` izvan virtuelnih okruženja radi zaštite OS-a, što je komplikovalo automatizaciju `systemd` servisa i pristup hardverskim GPIO pinovima.
* **Kompilacija na uređaju:** Mnoge Python biblioteke za AI i video obradu zahtevaju sate kompilacije direktno na procesoru Raspberry Pi-ja. Docker omogućava korišćenje *pre-built* image-a, smanjujući vreme setup-a sa 45 minuta na ispod 2 minuta ($O(1)$ deployment).

---

## 🚀 Originalni Ključni Moduli (Istorija)

### 🛰️ Real-Time Komunikacija
* **UDP Command Center:** Ultra-brza obrada komandi kretanja preko UDP protokola na portu `1606`.
* **WebRTC Vision Engine:** Optimizovan video striming niskih latencija putem WebRTC `/offer` endpointa (Port `1607`).
* **Mecanum Kinematics:** Napredni algoritmi za kontrolu kretanja motora sa preciznim PWM mapiranjem.

### 📸 Vision Engineering
* **Shared Camera Track:** Istovremeno opsluživanje N WebRTC klijenata bez konflikata zahvaljujući `asyncio` izolaciji memorije.
* **Fail-Safe Sistemi:** `Motor Watchdog` mehanizam koji zaustavlja robot u slučaju gubitka mrežnog signala ("Runaway Robot" prevencija).

---

## 🛠 Stari Tehnološki Stack

| Komponenta | Tehnologija | Uloga u ovoj verziji (Napušteno) |
| :--- | :--- | :--- |
| **OS Platforma** | Raspberry Pi OS (64-bit) | Hardversko jezgro sistema |
| **Language** | Python 3.11+ | Glavna asinhrona logika (`asyncio`) |
| **Camera Core** | Libcamera / PyAV | Video capture i obrada |
| **GPIO Control** | LGPIO / Gpiozero | Upravljanje motorima |
| **Networking** | UDP & WebRTC (`aiortc`) | Mrežni gateway |

---

## 🔌 Hardverska Konfiguracija (Nepromenjeno)

Bez obzira na softversku tranziciju, fizička mapa pinova ostaje ista:

* **Global PWM:** GPIO 18 (Brzina)
* **Motor A / B (Front):** GPIO 17, 27 / 22, 23
* **Motor C / D (Rear):** GPIO 24, 25 / 5, 6

---

<div align="center">

**Autor:** Danilo Stoletović • **Mentor:** Dejan Batanjac  
**ETŠ „Nikola Tesla“ Niš • 2026**

</div>
