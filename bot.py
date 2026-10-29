import os
import random
import subprocess
import requests
import pyttsx3  # 🔥 New Male Voice Library

# आपकी Facebook Page आईडी और GitHub Secrets से Access Token
FACEBOOK_PAGE_ID = "1322066784333919"
FB_ACCESS_TOKEN = os.environ.get("FB_ACCESS_TOKEN")
VIDEO_PATH = "reel.mp4"
RAW_VIDEO = "raw.mp4"
AUDIO_PATH = "voiceover.wav"  # pyttsx3 .wav format save karta hai
BG_IMAGE_PATH = "bg_image.jpg"


def generate_male_voiceover(text):
  """Pyttsx3 ka use karke Men (Male) jaisi heavy aur clear voice generate karega"""
  print("Step 1.5: Generating Male Voiceover using pyttsx3...")

  engine = pyttsx3.init()

  # Voice speed set karna (thoda slow aur clear taaki samajh aaye)
  engine.setProperty("rate", 155)

  # Linux (GitHub Actions) par available male voice select karna
  voices = engine.getProperty("voices")
  for voice in voices:
    # Male voice ya hindi/english standard voice dhoondna
    if "english" in voice.name.lower() or "hindi" in voice.name.lower():
      engine.setProperty("voice", voice.id)
      break

  # Audio file save karna
  engine.save_to_file(text, AUDIO_PATH)
  engine.runAndWait()
  print("✅ Male Voice generated successfully.")
