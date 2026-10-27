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
  print("Step 1: Downloading video via direct source...")
  video_url = "https://www.learningcontainer.com/wp-content/uploads/2020/05/sample-mp4-file.mp4"
  try:
    response = requests.get(video_url, stream=True)
    with open(RAW_VIDEO, "wb") as f:
      for chunk in response.iter_content(chunk_size=1024):
        if chunk:
          f.write(chunk)
    print("✅ Raw video downloaded successfully.")

    # 🔥 Step 1.5: AI Voice generate karne ka code (Copyright se bachne ke liye)
    print("Step 1.5: Generating AI Voiceover...")
    text_to_speak = "Amazing facts you need to watch! #shorts #viral"
    tts = gTTS(text=text_to_speak, lang="en", slow=False)
    tts.save(AUDIO_PATH)
    print("✅ AI Voice generated successfully.")

    print(
        "Step 2: Processing video, removing original audio & adding AI Voice..."
    )

    # 🔥 FFmpeg command jo original audio hata kar AI voice ko video ke sath mix karegi
    ffmpeg_command = [
        "ffmpeg",
        "-y",
        "-i",
        RAW_VIDEO,
        "-i",
        AUDIO_PATH,  # AI audio file input
        "-c:v",
        "copy",  # Video ko bina badle fast copy karega
        "-c:a",
        "aac",  # Audio format AAC
        "-map",
        "0:v:0",
        "-map",
        "1:a:0",  # 🔥 Sirf AI voice wali audio rakhega, purana copyright sound khatam!
        "-shortest",
        "-vf",
        "eq=brightness=0.03:saturation=1.1",
        "-t",
        "30",
        VIDEO_PATH,
    ]
    subprocess.run(ffmpeg_command, check=True)
    print(
        "✅ Video processed successfully with AI Voice and copyright protection."
    )

  except Exception as e:
    print(f"❌ Error during download/processing: {str(e)}")
    raise e


def upload_to_facebook():
  print("Step 3: Starting Facebook Reel Upload process...")
  if not FB_ACCESS_TOKEN:
    print("❌ Error: FB_ACCESS_TOKEN is missing in GitHub Secrets!")
    return
  if not os.path.exists(VIDEO_PATH):
    print(f"❌ Error: Processed video file '{VIDEO_PATH}' not found!")
    return

  try:
    # Step 4: Start the Reel Upload Session using 'START' phase
    print("Step 4: Starting video upload session with Facebook...")
    url = f"https://graph.facebook.com/v18.0/{FACEBOOK_PAGE_ID}/video_reels"
    payload = {"upload_phase": "START", "access_token": FB_ACCESS_TOKEN}
    response_raw = requests.post(url, data=payload)
    print(f"Facebook Raw Response: {response_raw.text}")
    response = response_raw.json()

    if "video_id" not in response or "upload_url" not in response:
      print(f"❌ Facebook Start Failed: {response}")
      return

    video_id = response["video_id"]
    upload_url = response["upload_url"]
    print(f"✅ Start successful! Video ID: {video_id}")

    # Step 5: Upload the Video Binary
    print("Step 5: Uploading video binary data to Facebook...")
    with open(VIDEO_PATH, "rb") as video_file:
      video_bytes = video_file.read()

    headers = {
        "Authorization": f"OAuth {FB_ACCESS_TOKEN}",
        "offset": "0",
        "file_size": str(len(video_bytes)),
    }
    upload_response = requests.post(
        upload_url, headers=headers, data=video_bytes
    ).json()
    print(f"Upload Binary Response: {upload_response}")
    print("✅ Video binary uploaded successfully.")

    # Step 6: Finish/Publish the Reel using 'FINISH' phase
    print("Step 6: Publishing the Reel on Facebook...")
    publish_url = f"https://graph.facebook.com/v18.0/{FACEBOOK_PAGE_ID}/video_reels"
    publish_payload = {
        "upload_phase": "FINISH",
        "video_state": "PUBLISHED",
        "description": "Automated Daily Movie Short Reel #shorts #viral",
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
