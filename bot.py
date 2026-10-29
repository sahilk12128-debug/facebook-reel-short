import json
import os
import random
import subprocess
import requests
from gtts import gTTS

FACEBOOK_PAGE_ID = "1322066784333919"
FB_ACCESS_TOKEN = os.environ.get("FB_ACCESS_TOKEN")
VIDEO_PATH = "reel.mp4"
RAW_VIDEO = "raw.mp4"
AUDIO_PATH = "voiceover.mp3"
BG_IMAGE_PATH = "bg_image.jpg"
POOL_FILE = "master_pool.json"
HISTORY_FILE = "used_stories.txt"


def get_non_repeating_content():
  print("Step 1: Loading unique content pool & checking history...")

  if os.path.exists(POOL_FILE):
    with open(POOL_FILE, "r", encoding="utf-8") as f:
      master_pool = json.load(f)
  else:
    master_pool = [{
        "text": (
            "Insan ka dil ek din mein\nlagbhag 1 lakh baar dhadakta hai!"
        ),
        "caption": "Amazing body facts! 👇 #Facts",
        "query": "science aesthetic background",
    }]

  # Load history of used texts
  used_texts = set()
  if os.path.exists(HISTORY_FILE):
    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
      used_texts = set(line.strip() for line in f.readlines())

  # Filter available unused items
  available_pool = [
      item for item in master_pool if item["text"] not in used_texts
  ]

  # Agar saari items use ho chuki hain, toh history reset kar do
  if not available_pool:
    print("🔄 All items used. Resetting history for fresh rotation...")
    if os.path.exists(HISTORY_FILE):
      os.remove(HISTORY_FILE)
    available_pool = master_pool

  chosen = random.choice(available_pool)

  # Save chosen text to history
  with open(HISTORY_FILE, "a", encoding="utf-8") as f:
    f.write(chosen["text"] + "\n")

  return chosen["text"], chosen["caption"], chosen["query"]


def download_background_image(query):
  print(f"Step 1.1: Generating background image for query: {query}")
  image_url = f"https://image.pollinations.ai/prompt/{query.replace(' ', '%20')}?width=1080&height=1920&nologo=true"

  try:
    response = requests.get(image_url, timeout=15)
    if response.status_code == 200:
      with open(BG_IMAGE_PATH, "wb") as f:
        f.write(response.content)
      print("✅ Background image downloaded successfully.")
      return True
  except Exception as e:
    print(f"⚠️ Error downloading image: {e}")

  return False


def generate_hindi_voice(text):
  print("Step 1.5: Generating Hindi Voiceover using gTTS...")
  clean_text = text.replace("\n", " ").replace("–", "")

  try:
    tts = gTTS(text=clean_text, lang="hi", slow=False)
    tts.save(AUDIO_PATH)
    print("✅ Hindi Voice generated successfully.")
    return True
  except Exception as e:
    print(f"⚠️ Error generating voice: {e}")

  return False


def download_and_process_video():
  story_text, viral_caption, query = get_non_repeating_content()
  print(f"Selected Content: {story_text}")

  has_image = download_background_image(query)
  generate_hindi_voice(story_text)

  print("Step 1.2: Compiling video with clean text (Shadow enabled)...")
  safe_text = (
      story_text.replace("'", "")
      .replace('"', "")
      .replace(":", " -")
      .replace("?", "")
      .replace("!", "")
  )

  if has_image and os.path.exists(BG_IMAGE_PATH):
    bg_cmd = [
        "ffmpeg",
        "-y",
        "-loop",
        "1",
        "-i",
        BG_IMAGE_PATH,
        "-vf",
        (
            "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,"
            "drawtext=text='VIRAL FACTS & STORIES':fontcolor=yellow:fontsize=52:x=(w-text_w)/2:y=250:shadowx=2:shadowy=2,"
            f"drawtext=text='{safe_text}':fontcolor=white:fontsize=44:line_spacing=28:x=(w-text_w)/2:y=(h-text_h)/2:shadowx=2:shadowy=2"
        ),
        "-c:v",
        "libx264",
        "-t",
        "30",
        "-pix_fmt",
        "yuv420p",
        RAW_VIDEO,
    ]
  else:
    bg_cmd = [
        "ffmpeg",
        "-y",
        "-f",
        "lavfi",
        "-i",
        (
            "color=c=0x0B0F19:s=1080x1920:rate=25:duration=30,"
            "drawtext=text='VIRAL FACTS & STORIES':fontcolor=yellow:fontsize=52:x=(w-text_w)/2:y=250:shadowx=2:shadowy=2,"
            f"drawtext=text='{safe_text}':fontcolor=white:fontsize=44:line_spacing=28:x=(w-text_w)/2:y=(h-text_h)/2:shadowx=2:shadowy=2"
        ),
        "-c:v",
        "libx264",
        "-pix_fmt",
        "yuv420p",
        RAW_VIDEO,
    ]

  subprocess.run(bg_cmd, check=True)
  print("✅ Video generated successfully.")

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
  print("✅ Video compiled successfully.")

  return viral_caption


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
  viral_caption = download_and_process_video()
  upload_to_facebook(viral_caption)
