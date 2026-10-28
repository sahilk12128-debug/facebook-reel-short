import os
import random
import subprocess
import requests
from gtts import gTTS

# आपकी Facebook Page आईडी और GitHub Secrets से Access Token
FACEBOOK_PAGE_ID = "1322066784333919"
FB_ACCESS_TOKEN = os.environ.get("FB_ACCESS_TOKEN")
VIDEO_PATH = "reel.mp4"
RAW_VIDEO = "raw.mp4"
AUDIO_PATH = "voiceover.mp3"
FACTS_FILE = "facts.txt"


def get_random_fact():
  """External facts.txt file se ek random fact aur hashtag uthayega"""
  if not os.path.exists(FACTS_FILE):
    # Agar file nahi mili toh backup fact
    return (
        "Octopuses ke paas teen dil aur chaar tentacle hote hain!",
        "#amazingfacts #science",
    )

  with open(FACTS_FILE, "r", encoding="utf-8") as f:
    lines = [line.strip() for line in f if line.strip()]

  if not lines:
    return (
        "Duniya ka sabse anmol ratan aapka waqt hai!",
        "#motivation #success",
    )

  selected_line = random.choice(lines)

  # Agar line mein hashtag hai toh usko alag karna
  if "#" in selected_line:
    parts = selected_line.rsplit("#", 1)
    fact_text = parts[0].strip()
    hashtag_tag = "#" + parts[1].strip()
  else:
    fact_text = selected_line
    hashtag_tag = "#facts #viral"

  return fact_text, hashtag_tag


def download_and_process_video():
  print("Step 1: Picking a fresh random fact from facts.txt...")
  fact_text, hashtag_tag = get_random_fact()

  print(f"Selected Fact: {fact_text}")

  print("Step 1.1: Generating animated background with line-by-line text...")
  safe_text = (
      fact_text.replace("'", "")
      .replace('"', "")
      .replace("?", "")
      .replace("!", "")
  )

  # 🔥 Animated Moving Gradient Background + Line-by-Line Text Overlay
  bg_cmd = [
      "ffmpeg",
      "-y",
      "-f",
      "lavfi",
      "-i",
      (
          "testsrc=size=1080x1920:rate=25:duration=30,"
          "geq=r='X/3+T*30':g='Y/3+T*30':b='150+sin(T)*100',"
          "drawtext=text='ROCHAK TATHYA':fontcolor=yellow:fontsize=64:x=(w-text_w)/2:y=250,"
          f"drawtext=text='{safe_text}':fontcolor=white:fontsize=46:line_spacing=20:x=(w-text_w)/2:y=(h-text_h)/2:box=1:boxcolor=black@0.8:boxborderw=40:shadowx=2:shadowy=2"
      ),
      "-c:v",
      "libx264",
      "-pix_fmt",
      "yuv420p",
      RAW_VIDEO,
  ]
  subprocess.run(bg_cmd, check=True)
  print("✅ Animated background & text generated successfully.")

  # Step 1.5: gTTS se clear voice generate karna
  normal_voice_text = fact_text.replace("\n", " ")
  print(f"Step 1.5: Generating Voiceover for: {normal_voice_text}")
  tts = gTTS(text=normal_voice_text, lang="hi", slow=False)
  tts.save(AUDIO_PATH)
  print("✅ Voice generated successfully.")

  print("Step 2: Mixing audio and compiling final video...")
  ffmpeg_command = [
      "ffmpeg",
      "-y",
      "-i",
      RAW_VIDEO,
      "-i",
      AUDIO_PATH,
      "-c:v",
      "libx264",
      "-c:a",
      "aac",
      "-map",
      "0:v:0",
      "-map",
      "1:a:0",
      "-shortest",
      "-t",
      "30",
      VIDEO_PATH,
  ]
  subprocess.run(ffmpeg_command, check=True)
  print("✅ Video processed and compiled successfully.")

  return normal_voice_text + " " + hashtag_tag


def upload_to_facebook(caption):
  print("Step 3: Starting Facebook Reel Upload process...")
  if not FB_ACCESS_TOKEN:
    print("❌ Error: FB_ACCESS_TOKEN is missing in GitHub Secrets!")
    return
  if not os.path.exists(VIDEO_PATH):
    print(f"❌ Error: Processed video file '{VIDEO_PATH}' not found!")
    return

  try:
    print("Step 4: Starting video upload session with Facebook...")
    url = f"https://graph.facebook.com/v18.0/{FACEBOOK_PAGE_ID}/video_reels"
    payload = {"upload_phase": "START", "access_token": FB_ACCESS_TOKEN}
    response_raw = requests.post(url, data=payload)
    response = response_raw.json()

    if "video_id" not in response or "upload_url" not in response:
      print(f"❌ Facebook Start Failed: {response}")
      return

    video_id = response["video_id"]
    upload_url = response["upload_url"]
    print(f"✅ Start successful! Video ID: {video_id}")

    print("Step 5: Uploading video binary data to Facebook...")
    with open(VIDEO_PATH, "rb") as video_file:
      video_bytes = video_file.read()

    headers = {
        "Authorization": f"OAuth {FB_ACCESS_TOKEN}",
        "offset": "0",
        "file_size": str(len(video_bytes)),
    }
    requests.post(upload_url, headers=headers, data=video_bytes)
    print("✅ Video binary uploaded successfully.")

    print("Step 6: Publishing the Reel on Facebook...")
    publish_url = f"https://graph.facebook.com/v18.0/{FACEBOOK_PAGE_ID}/video_reels"
    publish_payload = {
        "upload_phase": "FINISH",
        "video_state": "PUBLISHED",
        "description": caption,
        "video_id": video_id,
        "access_token": FB_ACCESS_TOKEN,
    }
    publish_response = requests.post(
        publish_url, data=publish_payload
    ).json()
    print(f"Publish Response: {publish_response}")

    if publish_response.get("success"):
      print("🎉 Success! Facebook Reel published successfully.")
    else:
      print(f"⚠️ Warning/Error during publish: {publish_response}")

  except Exception as e:
    print(f"❌ An exception occurred during upload: {str(e)}")


if __name__ == "__main__":
  dynamic_caption = download_and_process_video()
  upload_to_facebook(dynamic_caption)
