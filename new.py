import json
import time
import os
import queue
import sounddevice as sd
from vosk import Model, KaldiRecognizer
import pyautogui
import winsound   # for sound notification

# ---------------- SETTINGS ---------------- #
SAVE_FOLDER = "screenshots"
TRIGGER_PHRASES = ("computer", "capture", "screenshot")
COOLDOWN_SECONDS = 1.2
# ------------------------------------------- #

# Create screenshot directory
os.makedirs(SAVE_FOLDER, exist_ok=True)

# Play beep sound when screenshot is taken
def notify_sound():
    winsound.Beep(1200, 200)  # frequency, duration(ms)

# Save screenshot
def save_screenshot():
    ts = time.strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(SAVE_FOLDER, f"screenshot_{ts}.png")
    
    img = pyautogui.screenshot()
    img.save(filename)

    print(f"[{time.strftime('%H:%M:%S')}] Screenshot saved: {filename}")

    # play notification
    notify_sound()

# Queue for audio stream
q = queue.Queue()

# Called whenever audio is received
def audio_callback(indata, frames, time_info, status):
    q.put(bytes(indata))

# Main voice recognition loop
def voice_listen():

    # Load model
    if not os.path.exists("model"):
        print("ERROR: VOSK model not found!")
        print("Download from: https://alphacephei.com/vosk/models")
        return

    print("Loading VOSK model... (please wait)")
    model = Model("model")

    samplerate = 16000
    rec = KaldiRecognizer(model, samplerate)

    print("\n🎤 Voice Screenshot Activated")
    print("Say: 'take screenshot' or 'capture'")
    print("Say: 'quit program' to exit.\n")

    last_shot = 0.0

    # Start listening to microphone
    with sd.RawInputStream(
        samplerate=samplerate,
        blocksize=8000,
        dtype='int16',
        channels=1,
        callback=audio_callback
    ):
        while True:
            data = q.get()

            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                text = result.get("text", "").lower()

                if not text:
                    continue

                print("Heard:", text)

                # Quit command
                if "exit" in text or "exit program" in text:
                    print("Exiting program...")
                    break

                # Screenshot command
                now = time.time()
                for phrase in TRIGGER_PHRASES:
                    if phrase in text:
                        if now - last_shot > COOLDOWN_SECONDS:
                            save_screenshot()
                            last_shot = now
                        break

# Run Program
if __name__ == "__main__":
    voice_listen()
