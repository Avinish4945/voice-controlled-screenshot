# 🎙️ Voice-Controlled Screenshot System

A Python-based voice-controlled application that captures screenshots using offline speech recognition.

## 🚀 Features
- Offline voice recognition using VOSK
- Hands-free screenshot capture
- Trigger-based commands
- Screenshot saved with timestamp
- Audio beep notification after capture
- Cooldown system to avoid accidental multiple screenshots

## 🛠️ Tech Stack
- Python
- VOSK Speech Recognition
- SoundDevice
- PyAutoGUI
- OS & Queue modules

## 🎤 Trigger Words
The screenshot is captured when any of the following words are detected:
- computer
- capture
- screenshot

## 📁 Output
- Screenshots are saved automatically inside the `screenshots/` folder
- File format: PNG
- Filename format: screenshot_YYYYMMDD_HHMMSS.png

## ▶️ How to Run

### 1️⃣ Install dependencies
```bash
pip install sounddevice vosk pyautogui
