import os
import subprocess
import requests
from gtts import gTTS

# आपकी Facebook Page ID और GitHub Secrets से Access Token
FACEBOOK_PAGE_ID = "1322066784333919"
FB_ACCESS_TOKEN = os.environ.get("FB_ACCESS_TOKEN")
VIDEO_PATH = "reel.mp4"
RAW_VIDEO = "raw.mp4"
AUDIO_PATH = "voiceover.mp3"


def download_and_process_video():
  print("Step 1: Downloading standard reliable video...")

  video_url = (
      "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/"
      "ForBiggerBlazes.mp4"
  )

  try:
    response = requests.get(video_url, stream=True)
    with open(RAW_VIDEO, "wb") as f:
      for chunk in response.iter_content(chunk_size=1024):
        if chunk:
          f.write(chunk)
    print("✅ Video downloaded successfully.")
  except Exception as e:
    print(f"❌ Error downloading video: {str(e)}")
    raise e

  print("Step 1.5: Generating Hindi AI Voiceover...")
  text_to_hindi = (
      "Duniya ke sabse gazab aur rochak tathya! Ishe sunkar aap bhi hairan"
      " reh jayenge. Aise aur bhi mazedaar videos ke liye page ko follow"
      " karein!"
  )
  tts = gTTS(text=text_to_hindi, lang="hi", slow=False)
  tts.save(AUDIO_PATH)
  print("✅ Hindi AI Voice generated successfully.")

  print("Step 2: Processing video and combining audio safely...")

  # 🔥 Foolproof FFmpeg Command (No strict stream mapping errors, perfectly combines audio + video)
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
      "-shortest",
      "-vf",
      "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,"
      "eq=brightness=0.03:saturation=1.1",
      "-t",
      "30",
      VIDEO_PATH,
  ]
  subprocess.run(ffmpeg_command, check=True)
  print("✅ Video processed and compiled successfully.")


def upload_to_facebook():
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
        "description": (
            "Gajab ke rochak tathya! Zaroor dekhein #shorts #viral #hindi"
        ),
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
  download_and_process_video()
  upload_to_facebook()
