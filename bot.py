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


def get_smart_themed_fact():
  """Fact ke topic ke hisab se uska matching background theme aur text select karega"""
  print("Step 1: Selecting a fact with matching topic background theme...")

  # 🔥 Har fact ke sath uska topic-matching background color set hai
  themed_facts_pool = [
      {
          "text": (
              "Duniya mein jitne log hain,\nusse kahin zyada ped dharti par"
              " maujood hain!"
          ),
          "tag": "#nature #facts #earth",
          "bg": "0x0B2215",
      },  # Dark Forest Green (Nature theme)
      {
          "text": (
              "Insani dimaag ek din mein\nlagbhag 60,000 alag-alag vichaar\nsochta"
              " hai!"
          ),
          "tag": "#brain #psychology #knowledge",
          "bg": "0x1A1145",
      },  # Deep Purple (Mind & Psychology theme)
      {
          "text": (
              "Pani ki bottle par jo expiry date\nhoti hai woh pani ki nahi,\nbalki"
              " bottle ki hoti hai!"
          ),
          "tag": "#didyouknow #facts #water",
          "bg": "0x0B1D3A",
      },  # Ocean Blue (Water theme)
      {
          "text": "Duniya ka sabse purana chewing gum\n9,000 saal purana hai!",
          "tag": "#history #ancient #facts",
          "bg": "0x3A1F0B",
      },  # Ancient Bronze / Brown theme
      {
          "text": "Titali apne pairon se kisi bhi\ncheez ka swaad chakhti hai!",
          "tag": "#animals #insects #sciencefacts",
          "bg": "0x330B3A",
      },  # Vibrant Magenta (Wildlife theme)
      {
          "text": (
              "Aapki naak 1 kharab se bhi\nzyada alag-alag khusboo ko\npehchaan sakti"
              " hai!"
          ),
          "tag": "#humanbody #science #facts",
          "bg": "0x2D150B",
      },  # Warm Earthy theme
      {
          "text": (
              "Chamakdar taare asal mein\nbohot door hote hain aur\nunki roshni hazaron"
              " saal\npehle chali hoti hai!"
          ),
          "tag": "#space #astronomy #universe",
          "bg": "0x050814",
      },  # Deep Space Midnight Blue theme
      {
          "text": (
              "Japan mein train late hone par\ncompany yatriyon ko official\nmaafinama"
              " deti hai!"
          ),
          "tag": "#japan #trains #worldfacts",
          "bg": "0x3A0B0B",
      },  # Crimson Red theme
      {
          "text": (
              "Octopuses ke paas teen dil\naur chaar tentacle hote hain!"
          ),
          "tag": "#amazingfacts #science #viralshorts",
          "bg": "0x0B2A3A",
      },  # Deep Sea Teal theme
      {
          "text": (
              "Duniya ka sabse tez daudne wala\njanwar cheetah hai, aur ghongha\n3"
              " saal tak so sakta hai!"
          ),
          "tag": "#wildlifefacts #interestingfacts #hindi",
          "bg": "0x2E2A0B",
      },  # Safari Gold / Wildlife theme
      {
          "text": (
              "Space mein gravity na hone ki wajah\nse astronauts ki lambaai 2 inch"
              " badh jaati hai!"
          ),
          "tag": "#spacefacts #nasa #trending",
          "bg": "0x0F051D",
      },  # Cosmic Space theme
      {
          "text": (
              "Shahad hazaron saalon tak kharab\nnahi hota, yeh hamesha safe\nrehta"
              " hai!"
          ),
          "tag": "#historyfacts #honey #facts",
          "bg": "0x3A2E0B",
      },  # Golden Honey theme
  ]

  chosen = random.choice(themed_facts_pool)
  return chosen["text"], chosen["tag"], chosen["bg"]


def download_and_process_video():
  fact_text, hashtag_tag, bg_color = get_smart_themed_fact()
  print(f"Selected Fact: {fact_text} | Theme Background: {bg_color}")

  print("Step 1.1: Generating topic-matched themed background & text...")
  safe_text = (
      fact_text.replace("'", "")
      .replace('"', "")
      .replace("?", "")
      .replace("!", "")
  )

  # 🔥 Smart Themed Background (Fact ke hisab se color badlega) + Line-by-Line Text Layout
  bg_cmd = [
      "ffmpeg",
      "-y",
      "-f",
      "lavfi",
      "-i",
      (
          f"color=c={bg_color}:s=1080x1920:rate=25:duration=30,"
          "drawtext=text='ROCHAK TATHYA':fontcolor=yellow:fontsize=64:x=(w-text_w)/2:y=280,"
          f"drawtext=text='{safe_text}':fontcolor=white:fontsize=46:line_spacing=25:x=(w-text_w)/2:y=(h-text_h)/2:box=1:boxcolor=black@0.85:boxborderw=45:shadowx=2:shadowy=2"
      ),
      "-c:v",
      "libx264",
      "-pix_fmt",
      "yuv420p",
      RAW_VIDEO,
  ]
  subprocess.run(bg_cmd, check=True)
  print("✅ Themed background & text generated successfully.")

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
