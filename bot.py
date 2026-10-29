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
BG_IMAGE_PATH = "bg_image.jpg"


def get_fresh_anime_fact():
  """Har baar ek naya fact aur uske hisab se anime/cinematic background image chunega"""
  print("Step 1: Selecting a fresh unique fact...")

  # Facts aur unke sath matching cinematic/anime image search keywords
  anime_facts_pool = [
      {
          "text": (
              "Duniya mein jitne log hain,\nusse kahin zyada ped dharti par"
              " maujood hain!"
          ),
          "tag": "#nature #animeart #peace",
          "query": "anime forest landscape scenery aesthetic",
      },
      {
          "text": (
              "Insani dimaag ek din mein\nlagbhag 60,000 alag-alag vichaar\nsochta"
              " hai!"
          ),
          "tag": "#brain #deep #lofi",
          "query": "anime starry night sky aesthetic",
      },
      {
          "text": (
              "Pani ki bottle par jo expiry date\nhoti hai woh pani ki nahi,\nbalki"
              " bottle ki hoti hai!"
          ),
          "tag": "#facts #anime #mood",
          "query": "anime rain city aesthetic night",
      },
      {
          "text": "Duniya ka sabse purana chewing gum\n9,000 saal purana hai!",
          "tag": "#history #ancient #aesthetic",
          "query": "anime ancient village sunset",
      },
      {
          "text": "Titali apne pairon se kisi bhi\ncheez ka swaad chakhti hai!",
          "tag": "#nature #insects #anime",
          "query": "anime flower field butterfly",
      },
      {
          "text": (
              "Chamakdar taare asal mein\nbohot door hote hain aur\nunki roshni hazaron"
              " saal\npehle chali hoti hai!"
          ),
          "tag": "#space #universe #lofi",
          "query": "anime galaxy milky way night",
      },
      {
          "text": (
              "Octopuses ke paas teen dil\naur chaar tentacle hote hain!"
          ),
          "tag": "#ocean #deepsea #facts",
          "query": "anime underwater ocean blue aesthetic",
      },
      {
          "text": (
              "Duniya ka sabse tez daudne wala\njanwar cheetah hai, aur ghongha\n3"
              " saal tak so sakta hai!"
          ),
          "tag": "#wildlife #anime #forest",
          "query": "anime green forest peaceful morning",
      },
  ]

  chosen = random.choice(anime_facts_pool)
  return chosen["text"], chosen["tag"], chosen["query"]


def download_anime_background(query):
  """Fact ke topic par ek sundar Anime/Cinematic image download karega"""
  print(f"Step 1.1: Generating cinematic anime background for query: {query}")
  image_url = f"https://image.pollinations.ai/prompt/{query.replace(' ', '%20')}?width=1080&height=1920&nologo=true"
  
  try:
    response = requests.get(image_url, timeout=15)
    if response.status_code == 200:
      with open(BG_IMAGE_PATH, "wb") as f:
        f.write(response.content)
      print("✅ Cinematic Anime background image downloaded successfully.")
      return True
  except Exception as e:
    print(f"⚠️ Error downloading image: {e}")
  
  return False


def download_and_process_video():
  fact_text, hashtag_tag, query = get_fresh_anime_fact()
  print(f"Selected Fact: {fact_text}")

  has_image = download_anime_background(query)

  print("Step 1.2: Compiling video with anime background & line-by-line text...")
  safe_text = (
      fact_text.replace("'", "")
      .replace('"', "")
      .replace("?", "")
      .replace("!", "")
  )

  if has_image and os.path.exists(BG_IMAGE_PATH):
    # 🔥 Cinematic Anime Background Image + Line-by-Line Text Overlay
    bg_cmd = [
        "ffmpeg",
        "-y",
        "-loop", "1",
        "-i", BG_IMAGE_PATH,
        "-vf", (
            "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,"
            "drawtext=text='ROCHAK TATHYA':fontcolor=yellow:fontsize=64:x=(w-text_w)/2:y=280,"
            f"drawtext=text='{safe_text}':fontcolor=white:fontsize=46:line_spacing=25:x=(w-text_w)/2:y=(h-text_h)/2:box=1:boxcolor=black@0.75:boxborderw=45:shadowx=2:shadowy=2"
        ),
        "-c:v", "libx264",
        "-t", "30",
        "-pix_fmt", "yuv420p",
        RAW_VIDEO,
    ]
  else:
    # Fallback solid dark theme agar image download na ho
    bg_cmd = [
        "ffmpeg",
        "-y",
        "-f", "lavfi",
        "-i", (
            "color=c=0x0B0F19:s=1080x1920:rate=25:duration=30,"
            "drawtext=text='ROCHAK TATHYA':fontcolor=yellow:fontsize=64:x=(w-text_w)/2:y=280,"
            f"drawtext=text='{safe_text}':fontcolor=white:fontsize=46:line_spacing=25:x=(w-text_w)/2:y=(h-text_h)/2:box=1:boxcolor=black@0.85:boxborderw=45:shadowx=2:shadowy=2"
        ),
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        RAW_VIDEO,
    ]

  subprocess.run(bg_cmd, check=True)
  print("✅ Video background & text generated successfully.")

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
      "-i", RAW_VIDEO,
      "-i", AUDIO_PATH,
      "-c:v", "libx264",
      "-c:a", "aac",
      "-map", "0:v:0",
      "-map", "1:a:0",
      "-shortest",
      "-t", "30",
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
