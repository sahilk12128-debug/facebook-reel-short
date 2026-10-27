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

# 🔥 Bilkul Naye aur Viral Facts ki List (Har baar alag fact aayega)
VIRAL_FACTS = [
    {
        "text": (
            "Kya aap jaante hain? Octopuses ke paas teen dil aur chaar tentacle"
            " hote hain!"
        ),
        "tag": "#amazingfacts #science #viralshorts",
    },
    {
        "text": (
            "Duniya ka sabse tez daudne wala janwar cheetah hai, aur ek ghongha"
            " lagataar 3 saal tak so sakta hai!"
        ),
        "tag": "#wildlifefacts #interestingfacts #hindi",
    },
    {
        "text": (
            "Aapki ankhon ki putli andhere mein badi ho jaati hai aur roshni mein"
            " choti ho jaati hai!"
        ),
        "tag": "#humanbody #facts #knowledge",
    },
    {
        "text": (
            "Space mein gravity na hone ki wajah se astronauts ki lambaai 2 inch"
            " tak badh jaati hai!"
        ),
        "tag": "#spacefacts #nasa #trending",
    },
    {
        "text": (
            "Shahad ek aisi cheez hai jo hazaron saalon tak kharab nahi hoti,"
            " yeh hamesha safe rehta hai!"
        ),
        "tag": "#historyfacts #honey #facts",
    },
    {
        "text": (
            "Suraj ki roshni ko zameen tak pahunchne mein lagbhag 8 minute aur 20"
            " second ka samay lagta hai!"
        ),
        "tag": "#universe #sun #sciencefacts",
    },
    {
        "text": (
            "Insaan ki haddiyan cement se bhi zyada mazboot hoti hain!"
        ),
        "tag": "#amazing #healthfacts #knowledge",
    },
    {
        "text": (
            "Kela jhuka hua isliye hota hai kyunki yeh sooraj ki taraf badhne ki"
            " koshish karta hai!"
        ),
        "tag": "#banana #naturefacts #shorts",
    },
]


def download_and_process_video():
  print("Step 1: Selecting random unique fact...")
  selected_item = random.choice(VIRAL_FACTS)
  fact_text = selected_item["text"]
  hashtag_tag = selected_item["tag"]

  print("Step 1.1: Generating video background with text overlay...")
  safe_text = (
      fact_text.replace("'", "")
      .replace('"', "")
      .replace("?", "")
      .replace("!", "")
  )

  # FFmpeg ke zariye background aur screen par text likhne ka code
  bg_cmd = [
      "ffmpeg",
      "-y",
      "-f",
      "lavfi",
      "-i",
      (
          "color=c=0x0F172A:s=1080x1920:rate=25:duration=30,"
          "drawtext=text='ROCHAK TATHYA':fontcolor=orange:fontsize=64:x=(w-text_w)/2:y=300,"
          f"drawtext=text='{safe_text}':fontcolor=white:fontsize=48:x=(w-text_w)/2:y=(h-text_h)/2:box=1:boxcolor=black@0.6:boxborderw=20:shadowx=2:shadowy=2"
      ),
      "-c:v",
      "libx264",
      "-pix_fmt",
      "yuv420p",
      RAW_VIDEO,
  ]
  subprocess.run(bg_cmd, check=True)
  print("✅ Video background with text generated successfully.")

  # Step 1.5: gTTS se clear voice generate karna
  print(f"Step 1.5: Generating Voiceover for: {fact_text}")
  tts = gTTS(text=fact_text, lang="hi", slow=False)
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

  return fact_text + " " + hashtag_tag


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
