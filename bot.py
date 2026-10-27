import os
import random
import subprocess
import requests
from gtts import gTTS

# आपकी Facebook Page ID और GitHub Secrets से Access Token
FACEBOOK_PAGE_ID = "1322066784333919"
FB_ACCESS_TOKEN = os.environ.get("FB_ACCESS_TOKEN")
VIDEO_PATH = "reel.mp4"
RAW_VIDEO = "raw.mp4"
AUDIO_PATH = "voiceover.mp3"

# Facts aur Motivation ki Unique Scripts
FACTS_AND_MOTIVATION = [
    {
        "text": (
            "Duniya ka sabse bada sach yeh hai ki mehnat kabhi vyarth nahi hoti."
            " Apne sapno par vishwas rakho aur aage badhte raho!"
        ),
        "tag": "#motivation #success #hindi",
    },
    {
        "text": (
            "Kya aapko pata hai? Insaan ka dimaag itni urja paida karta hai jisse"
            " ek chota bulb jal sakta hai. Aise hi amazing facts ke liye follow"
            " karein!"
        ),
        "tag": "#facts #amazing #knowledge",
    },
    {
        "text": (
            "Zindagi mein agar aage badhna hai toh darna chhod do, kyunki jo"
            " dar gaya, samajho woh haar gaya. Mehnat karo aur jeet kar dikhao!"
        ),
        "tag": "#motivationalquotes #hindi #viral",
    },
    {
        "text": (
            "Kya aap jaante hain? Paani ke baad duniya mein sabse zyada piya"
            " jaane wala drink Chai hai! Is rochak tathya ke liye page ko follow"
            " karein."
        ),
        "tag": "#interestingfacts #tea #facts",
    },
    {
        "text": (
            "Muskil waqt wahi log paas karte hain jo khud par bharosa rakhte"
            " hain. Aapki aaj ki mehnat hi aapka kal banayegi!"
        ),
        "tag": "#selfbelief #motivation #shorts",
    },
]


def download_and_process_video():
  print("Step 1: Generating dynamic animated visual background...")

  # 🔥 Moving Gradient Background (Jisme continuous visual motion / graphics effect dikhega)
  motion_bg_cmd = [
      "ffmpeg",
      "-y",
      "-f",
      "lavfi",
      "-i",
      (
          "testsrc=size=1080x1920:rate=25:duration=30,"
          "geq=r='X/2+T*25':g='Y/2+T*25':b='128+sin(T)*128'"
      ),
      "-c:v",
      "libx264",
      "-pix_fmt",
      "yuv420p",
      RAW_VIDEO,
  ]
  subprocess.run(motion_bg_cmd, check=True)
  print("✅ Animated motion background generated successfully.")

  # Step 1.5: Random Unique Hindi Script & Voiceover
  selected_content = random.choice(FACTS_AND_MOTIVATION)
  hindi_script = selected_content["text"]
  hashtag_tag = selected_content["tag"]

  print(f"Step 1.5: Generating voiceover for: {hindi_script}")
  tts = gTTS(text=hindi_script, lang="hi", slow=False)
  tts.save(AUDIO_PATH)
  print("✅ Voice generated successfully.")

  print("Step 2: Processing video and mixing audio...")

  # FFmpeg command jo animated background aur voice ko mix karegi
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

  return hindi_script + " " + hashtag_tag


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
