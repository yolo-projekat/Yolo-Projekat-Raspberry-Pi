import websockets
import asyncio
import io
import signal
import sys
from datetime import datetime
from gpiozero import PWMOutputDevice, DigitalOutputDevice
from gpiozero.pins.lgpio import LGPIOFactory
from aiohttp import web
from picamera2 import Picamera2

# --- GPIO & HARDWARE CONFIGURATION ---
factory = LGPIOFactory()
mapa = {
    11: 17, 12: 18, 13: 27, 15: 22,
    16: 23, 18: 24, 22: 25, 29: 5, 31: 6
}

ENABCD = PWMOutputDevice(pin=mapa[12], frequency=50, pin_factory=factory)

motorA_IN1 = DigitalOutputDevice(pin=mapa[11], pin_factory=factory)
motorA_IN2 = DigitalOutputDevice(pin=mapa[13], pin_factory=factory)
motorB_IN3 = DigitalOutputDevice(pin=mapa[15], pin_factory=factory)
motorB_IN4 = DigitalOutputDevice(pin=mapa[16], pin_factory=factory)
motorC_IN1 = DigitalOutputDevice(pin=mapa[18], pin_factory=factory)
motorC_IN2 = DigitalOutputDevice(pin=mapa[22], pin_factory=factory)
motorD_IN3 = DigitalOutputDevice(pin=mapa[29], pin_factory=factory)
motorD_IN4 = DigitalOutputDevice(pin=mapa[31], pin_factory=factory)

motor_pins = [
    motorA_IN1, motorA_IN2, 
    motorB_IN3, motorB_IN4,
    motorC_IN1, motorC_IN2, 
    motorD_IN3, motorD_IN4
]

# --- MOVEMENT LOGIC MAPS ---
MOVEMENTS = {
    "napred":    (1, 1, 1, 1),
    "nazad":     (-1, -1, -1, -1),
    "levo":      (-1, 1, -1, 1),
    "desno":     (1, -1, 1, -1),
    "rot_levo":  (-1, -1, 1, 1), 
    "rot_desno": (1, 1, -1, -1),
    "stop":      (0, 0, 0, 0)
}

DIAGONALS = {
    frozenset(["napred", "desno"]): (1, 1, 0, 0),
    frozenset(["napred", "levo"]):  (0, 0, 1, 1),
    frozenset(["nazad", "desno"]):  (-1, -1, 0, 0),
    frozenset(["nazad", "levo"]):   (0, 0, -1, -1)
}

# --- CAMERA SETUP ---
picam2 = Picamera2()
config = picam2.create_video_configuration(
    main={"size": (640, 480), "format": "RGB888"},
    raw={"size": (3280, 2464)}
)
picam2.configure(config)
picam2.set_controls({"ScalerCrop": (0, 0, 3280, 2464)})
zoom_level = 1.0

# --- HELPER FUNCTIONS ---
def log(message):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}")

def stop_motors():
    ENABCD.value = 0
    for pin in motor_pins:
        pin.off()

def set_motor_state(in1, in2, state):
    if state == 1:
        in1.on(); in2.off()
    elif state == -1:
        in1.off(); in2.on()
    else:
        in1.off(); in2.off()

def execute_move(states, duty_cycle=0.3):
    ENABCD.value = duty_cycle
    for i, state in enumerate(states):
        set_motor_state(motor_pins[i*2], motor_pins[i*2+1], state)

def apply_zoom(level):
    global zoom_level
    zoom_level = max(0.1, min(3.0, level))
    full_w, full_h = 3280, 2464
    w, h = int(full_w / zoom_level), int(full_h / zoom_level)
    x, y = (full_w - w) // 2, (full_h - h) // 2
    try:
        picam2.set_controls({"ScalerCrop": (x, y, w, h)})
        log(f"[ZOOM] Faktor: {zoom_level:.2f}")
    except Exception as e:
        log(f"[ZOOM ERROR] {e}")

# --- HANDLERS ---
async def websocket_handler(websocket, path=None):
    client_ip = websocket.remote_address[0]
    log(f"Novi klijent: {client_ip}")
    try:
        async for message in websocket:
            msg = message.strip().lower()
            
            if msg.startswith("zoom:"):
                try:
                    apply_zoom(float(msg.split(":")[1]))
                    continue
                except: continue

            parts = msg.split('+')
            cmd_set = frozenset(parts)

            if "stop" in cmd_set:
                stop_motors()
            elif len(parts) == 1 and parts[0] in MOVEMENTS:
                # LOWER SPEED FOR ROTATION (0.15 instead of 0.3)
                speed = 0.15 if "rot_" in parts[0] else 0.3
                execute_move(MOVEMENTS[parts[0]], duty_cycle=speed)
            elif len(parts) == 2 and cmd_set in DIAGONALS:
                execute_move(DIAGONALS[cmd_set])
            else:
                await websocket.send("Nevalida komanda")
    except Exception as e:
        log(f"WS Greska: {e}")
        stop_motors()

async def capture_image(request):
    try:
        buffer = io.BytesIO()
        await asyncio.get_event_loop().run_in_executor(
            None, lambda: picam2.capture_file(buffer, format='jpeg')
        )
        return web.Response(body=buffer.getvalue(), content_type='image/jpeg')
    except Exception as e:
        return web.Response(status=500)

# --- SYSTEM CONTROL ---
def shutdown_handler(signum, frame):
    log("Gašenje...")
    stop_motors()
    try: picam2.stop()
    except: pass
    sys.exit(0)

signal.signal(signal.SIGTERM, shutdown_handler)
signal.signal(signal.SIGINT, shutdown_handler)

async def main():
    picam2.start()
    apply_zoom(zoom_level)
    
    ws_server = await websockets.serve(websocket_handler, "0.0.0.0", 1606)
    
    app = web.Application()
    app.router.add_get('/capture', capture_image)
    runner = web.AppRunner(app)
    await runner.setup()
    await web.TCPSite(runner, '0.0.0.0', 1607).start()

    log("Sistem spreman. Rotacija je sada na 50% brzine kretanja.")
    await asyncio.Future()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
