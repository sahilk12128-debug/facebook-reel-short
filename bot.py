import os
import random
import subprocess
import requests

FACEBOOK_PAGE_ID = "1322066784333919"
FB_ACCESS_TOKEN = os.environ.get("FB_ACCESS_TOKEN")
VIDEO_PATH = "reel.mp4"
MOVIE_FILE = "movie.mp4"

# Google Drive ki direct download link
GOOGLE_DRIVE_DOWNLOAD_URL = (
    "https://drive.google.com/uc?export=download&id=1pHg_AkvY40iy_B9S4YD8teF1HzD1GhSf"
)


def download_movie_from_drive():
  print("Step 1: Downloading movie from your Google Drive...")
  if os.path.exists(MOVIE_FILE) and os.path.getsize(MOVIE_FILE) > 1024 * 1024:
    print("✅ Movie already exists locally.")
    return True

  try:
    print("Downloading... (This might take a few moments)")
    response = requests.get(GOOGLE_DRIVE_DOWNLOAD_URL, stream=True, timeout=120)

    if response.status_code == 200:
      with open(MOVIE_FILE, "wb") as f:
        for chunk in response.iter_content(chunk_size=1024 * 1024):
          if chunk:
            f.write(chunk)
      print("✅ Movie downloaded successfully from Google Drive.")
      return True
    else:
      print(
          "❌ Failed to download. Status code: "
          f"{response.status_code}"
      )
      return False
  except Exception as e:
    print(f"❌ Error downloading movie: {e}")
    return False


def cut_safe_movie_clip():
  print("Step 2: Cutting a random copyright-safe clip from the movie...")

  if not os.path.exists(MOVIE_FILE):
    print("❌ Error: movie.mp4 not found!")
    return None

  # Default fallback start time agar ffprobe fail ho jaye
  start_time = 300  # 5th minute se
  clip_duration = 30

  try:
    result = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            MOVIE_FILE,
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=True,
    )
    total_duration = float(result.stdout.strip())
    if total_duration > 120:
      start_time = random.randint(60, int(total_duration) - 60)
  except Exception as e:
    print(f"⚠️ Warning: Could not detect exact duration ({e}), using default start time.")

  print(f"🎬 Cutting clip starting at timestamp: {start_time} seconds")

  # Copyright Safe FFmpeg Command
  cut_cmd = [
      "ffmpeg",
      "-y",
      "-ss",
      str(start_time),
      "-i",
      MOVIE_FILE,
      "-t",
      str(clip_duration),
      "-vf",
      (
          "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,"
          "drawtext=text='BEST MOVIE SCENES':fontcolor=yellow:fontsize=50:x=(w-text_w)/2:y=150:shadowx=2:shadowy=2"
      ),
      "-af",
      "atempo=1.05",
      "-c:v",
      "libx264",
      "-c:a",
      "aac",
      VIDEO_PATH,
  ]

  subprocess.run(cut_cmd, check=True)
  print("✅ Copyright-safe movie clip processed successfully.")

  viral_caption = (
      "Best movie scene! 🍿 Yeh suspense kaisa laga? Comments mein batao! 👇\n\n"
      "#Movies #MovieScenes #Bollywood #TrendingReels #ViralReels #Cinema"
  )
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
      print("🎉 Success! Movie Reel published successfully.")
    else:
      print(f"⚠️ Warning/Error during publish: {publish_response}")

  except Exception as e:
    print(f"❌ An exception occurred during upload: {str(e)}")


if __name__ == "__main__":
  if download_movie_from_drive():
    viral_caption = cut_safe_movie_clip()
    if viral_caption:
      upload_to_facebook(viral_caption)
