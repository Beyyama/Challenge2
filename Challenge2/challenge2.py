import cv2
import time
import numpy as np
import os
import subprocess
import sys
from picamera2 import Picamera2
from time import sleep
from picarx import Picarx

# === Auto-Install (Requirements) ===
def install_requirements():
    try:
        import cv2, numpy, picamera2
    except ImportError:
        print("🔧 Installiere benötigte Pakete...")
        os.system("sudo apt update")
        os.system("sudo apt install python3-opencv python3-numpy python3-picamera2 espeak mpg123 -y")

install_requirements()

# === Initialisierung ===
px = Picarx()
speed = 20

picam2 = Picamera2()
picam2.preview_configuration.main.size = (320, 240)
picam2.preview_configuration.main.format = "RGB888"
picam2.preview_configuration.align()
picam2.start()

# === Helligkeitsgrenzen ===
BRIGHT_THRESHOLD = 160
MIN_BRIGHT_PIXELS = 1000
max_drive_time = 6  # Sekunden

# === Pfade ===
script_dir = os.path.dirname(os.path.abspath(__file__))
music_path = os.path.join(script_dir, "sound.mp3")

# === Funktionen ===
def speak(text):
    """Sprachausgabe"""
    try:
        os.system(f'espeak "{text}" 2>/dev/null')
    except:
        pass

def analyze_lane(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    roi = gray[160:240, :]
    _, binary = cv2.threshold(roi, BRIGHT_THRESHOLD, 255, cv2.THRESH_BINARY)

    third_width = binary.shape[1] // 3
    left = binary[:, :third_width]
    center = binary[:, third_width:2 * third_width]
    right = binary[:, 2 * third_width:]

    sum_left = np.sum(left == 255)
    sum_center = np.sum(center == 255)
    sum_right = np.sum(right == 255)

    print(f"Helligkeit - Links: {sum_left}, Mitte: {sum_center}, Rechts: {sum_right}")

    if sum_left < MIN_BRIGHT_PIXELS:
        return 'avoid_left'
    elif sum_right < MIN_BRIGHT_PIXELS:
        return 'avoid_right'
    else:
        return 'center_ok'

def steer(direction):
    if direction == 'center_ok':
        px.set_dir_servo_angle(0)
        print("→ Geradeaus")
    elif direction == 'avoid_left':
        px.set_dir_servo_angle(20)
        print("↷ Linke Seite dunkel – Lenke nach rechts")
    elif direction == 'avoid_right':
        px.set_dir_servo_angle(-20)
        print("↶ Rechte Seite dunkel – Lenke nach links")


# === Begrüßung ===
print("🎤 Willkommen zur zweiten Challenge!")
speak("Willkommen zur zweiten Challenge! Ich fahre jetzt meine Runde und vermeide die Ränder.")

# === Starte Musik ===
music_process = subprocess.Popen(['mpg123', '-q', music_path])

# === Start der Fahrt ===
px.forward(speed)
start_time = time.time()

try:
    while True:
        if time.time() - start_time > max_drive_time:
            print("✅ Ziel erreicht – Stoppe Auto.")
            px.stop()
            music_process.terminate()
            speak("Das hat wunderbar funktioniert!")
            break

        frame = picam2.capture_array()
        direction = analyze_lane(frame)
        steer(direction)
        sleep(0.05)

except KeyboardInterrupt:
    print("⛔ Manuell gestoppt.")
    px.stop()
    music_process.terminate()
