import asyncio
import logging
import signal
import sys
import time

import numpy as np
from aiohttp import web
from aiortc import RTCPeerConnection, RTCSessionDescription, VideoStreamTrack
from av import VideoFrame
from gpiozero import PWMOutputDevice, DigitalOutputDevice
from gpiozero.pins.lgpio import LGPIOFactory
from picamera2 import Picamera2

# --- CONFIGURATION & LOGGING ---
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)

# --- GPIO PIN MAPPING ---
factory = LGPIOFactory()
PIN_MAP = {11: 17, 12: 18, 13: 27, 15: 22, 16: 23, 18: 24, 22: 25, 29: 5, 31: 6}

ENABCD = PWMOutputDevice(pin=PIN_MAP[12], frequency=50, pin_factory=factory)
motor_pins = [DigitalOutputDevice(pin=PIN_MAP[p], pin_factory=factory) for p in (11, 13, 15, 16, 18, 22, 29, 31)]

# --- O(1) MOVEMENT LOOKUPS ---
MOVEMENTS = {
    "napred":    (1, 1, 1, 1),
    "nazad":     (-1, -1, -1, -1),
    "levo":      (-1, 1, -1, 1),
    "desno":     (1, -1, 1, -1),
    "rot_levo":  (-1, -1, 1, 1),
    "rot_desno": (1, 1, -1, -1),
    "stop":      (0, 0, 0, 0),
}

DIAGONALS = {
    frozenset(["napred", "desno"]): (1, 1, 0, 0),
    frozenset(["napred", "levo"]):  (0, 0, 1, 1),
    frozenset(["nazad", "desno"]):  (-1, -1, 0, 0),
    frozenset(["nazad", "levo"]):   (0, 0, -1, -1),
}

ROTATION_CMDS = frozenset(["rot_levo", "rot_desno"])
SPEED_NORMAL = 0.3
SPEED_ROTATION = 0.15

# --- GLOBAL STATE ---
LAST_CMD_TIME = 0.0
WATCHDOG_TIMEOUT = 0.5  # Seconds
CAMERA_ACTIVE = True
LATEST_FRAME_ARRAY = None
FRAME_EVENT = asyncio.Event()

# --- HARDWARE CONTROL ---
def set_motor_state(in1, in2, state):
    if state == 1: in1.on(); in2.off()
    elif state == -1: in1.off(); in2.on()
    else: in1.off(); in2.off()

def stop_motors():
    if ENABCD.value != 0:
        ENABCD.value = 0
        for pin in motor_pins: pin.off()

def execute_move(states, duty_cycle=SPEED_NORMAL):
    if ENABCD.value != duty_cycle:  # Prevent redundant I/O calls
        ENABCD.value = duty_cycle
    for i, state in enumerate(states):
        set_motor_state(motor_pins[i * 2], motor_pins[i * 2 + 1], state)

# --- WATCHDOG TASK ---
async def motor_watchdog():
    """Prevents runaway robot on UDP packet loss."""
    while True:
        if ENABCD.value > 0 and (time.time() - LAST_CMD_TIME > WATCHDOG_TIMEOUT):
            logger.warning("UDP timeout. Engaging emergency stop.")
            stop_motors()
        await asyncio.sleep(0.1)

# --- UDP PROTOCOL ---
class RobotUDPControl(asyncio.DatagramProtocol):
    def connection_made(self, transport):
        self.transport = transport
        logger.info("UDP Control bound to 0.0.0.0:1606")

    def datagram_received(self, data, addr):
        global LAST_CMD_TIME
        LAST_CMD_TIME = time.time()  # Reset watchdog
        
        try:
            msg = data.decode('utf-8').strip().lower()
            parts = msg.split('+')
            cmd_set = frozenset(parts)

            if "stop" in cmd_set:
                stop_motors()
            elif len(parts) == 1 and parts[0] in MOVEMENTS:
                cmd = parts[0]
                speed = SPEED_ROTATION if cmd in ROTATION_CMDS else SPEED_NORMAL
                execute_move(MOVEMENTS[cmd], duty_cycle=speed)
            elif len(parts) == 2 and cmd_set in DIAGONALS:
                execute_move(DIAGONALS[cmd_set], duty_cycle=SPEED_NORMAL)
        except Exception as e:
            logger.error(f"UDP parse error: {e}")

# --- CAMERA PRODUCER (SINGLETON) ---
async def camera_producer(picam2):
    """Fetches frames constantly to shared memory, decoupled from WebRTC clients."""
    global LATEST_FRAME_ARRAY
    loop = asyncio.get_running_loop()
    
    while CAMERA_ACTIVE:
        try:
            # Threaded capture prevents blocking asyncio loop
            array = await loop.run_in_executor(None, picam2.capture_array, "main")
            LATEST_FRAME_ARRAY = array
            FRAME_EVENT.set()
            FRAME_EVENT.clear()
            await asyncio.sleep(0.033) # Max ~30fps to prevent CPU saturation
        except Exception as e:
            logger.error(f"Camera Producer error: {e}")
            await asyncio.sleep(1)

# --- WEBRTC VIDEO TRACK (CONSUMER) ---
class SharedCameraTrack(VideoStreamTrack):
    """Consumes the global frame array, allowing N clients without hardware contention."""
    def __init__(self):
        super().__init__()

    async def recv(self):
        pts, time_base = await self.next_timestamp()
        
        await FRAME_EVENT.wait() # Efficient wait for next frame
        if LATEST_FRAME_ARRAY is None:
            raise Exception("No frame available")

        # PyAV isolates memory, making it thread-safe for multiple tracks
        frame = VideoFrame.from_ndarray(LATEST_FRAME_ARRAY, format="rgb24")
        frame.pts = pts
        frame.time_base = time_base
        return frame

# --- WEBRTC SIGNALING ---
pcs = set()

async def rtc_offer(request):
    params = await request.json()
    offer = RTCSessionDescription(sdp=params["sdp"], type=params["type"])

    pc = RTCPeerConnection()
    pcs.add(pc)

    @pc.on("iceconnectionstatechange")
    async def on_iceconnectionstatechange():
        if pc.iceConnectionState in ["failed", "closed", "disconnected"]:
            logger.info(f"Closing dead WebRTC connection.")
            await pc.close()
            pcs.discard(pc)

    pc.addTrack(SharedCameraTrack())
    await pc.setRemoteDescription(offer)
    answer = await pc.createAnswer()
    await pc.setLocalDescription(answer)

    return web.json_response({"sdp": pc.localDescription.sdp, "type": pc.localDescription.type})

async def on_shutdown(app):
    coros = [pc.close() for pc in pcs]
    await asyncio.gather(*coros)
    pcs.clear()

# --- LIFECYCLE MANAGEMENT ---
def initiate_shutdown():
    logger.info("Graceful shutdown sequence initiated...")
    global CAMERA_ACTIVE
    CAMERA_ACTIVE = False
    stop_motors()
    sys.exit(0)

async def main():
    loop = asyncio.get_running_loop()
    for sig in (signal.SIGTERM, signal.SIGINT):
        loop.add_signal_handler(sig, initiate_shutdown)

    # Initialize PiCamera
    picam2 = Picamera2()
    picam2.configure(picam2.create_video_configuration(
        main={"size": (640, 480), "format": "RGB888"}
    ))
    picam2.start()

    # Start Background Tasks
    asyncio.create_task(camera_producer(picam2))
    asyncio.create_task(motor_watchdog())

    # Start UDP Server
    transport, protocol = await loop.create_datagram_endpoint(
        lambda: RobotUDPControl(),
        local_addr=("0.0.0.0", 1606)
    )

    # Start HTTP WebRTC Signaling
    app = web.Application()
    
    # Handle CORS for frontend integration
    import aiohttp_cors
    cors = aiohttp_cors.setup(app, defaults={"*": aiohttp_cors.ResourceOptions(
        allow_credentials=True, expose_headers="*", allow_headers="*"
    )})
    route = app.router.add_post("/offer", rtc_offer)
    cors.add(route)
    
    app.on_shutdown.append(on_shutdown)
    
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 1607)
    await site.start()

    logger.info("System Online. Ready for WebRTC and UDP commands.")
    
    try:
        await asyncio.Event().wait()
    except asyncio.CancelledError:
        pass
    finally:
        transport.close()
        picam2.stop()

if __name__ == "__main__":
    try:
        # Requires: pip install aiortc av numpy aiohttp-cors gpiozero picamera2
        asyncio.run(main())
    except KeyboardInterrupt:
        pass