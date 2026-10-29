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


def get_random_unique_content():
  """Har baar ek bilkul nayi aur alag funny ya fact video chunega taaki repeat na ho"""
  print("Step 1: Selecting fresh unique content (Funny & Facts mix)...")

  master_pool = [
      # --- Category 1: Funny Baby Stories ---
      {
          "text": (
              "Beta, 20 rupaye do,\nswarg mil jayega!\n\nAre Dada ji,\n20 rupaye"
              " mein toh ice cream aati hai!"
          ),
          "caption": (
              "Bachhe ki yeh baat sunkar hasi nahi ro paoge! 🤭 Cute baby"
              " moments ke liye follow karein! 👇\n\n#CuteBaby #Funny"
              " #BabySmile #TrendingReels #Comedy"
          ),
          "query": (
              "cute 3d animated baby talking to an old grandfather on a bench"
              " in a park, Pixar style"
          ),
      },
      {
          "text": (
              "Mummi ne bola ki:\nJaldi so jao warna\nBhoot aa jayega!\n\nMaine bola:"
              " Bulwao use, akela bore ho raha hu!"
          ),
          "caption": (
              "Aajkal ke bachhe kisi se nahi darte! 👻 Tag your fearless friends!"
              " 👇\n\n#FunnyBaby #CuteBaby #ViralReels #Trending #BabyComedy"
          ),
          "query": (
              "cute funny 3d animated baby smiling mischievously in a cozy"
              " bedroom, Pixar style"
          ),
      },
      {
          "text": (
              "Jab papa poochte hain:\nMobile kisne toda?\n\nAur main apni ankhon"
              " se\nmera bhai dikha deta hu!"
          ),
          "caption": (
              "Mastermind baby! 🧠 Kis-kis ne bachpan mein yeh kiya hai?"
              " Comments mein batao! 👇\n\n#SmartBaby #CuteBaby #ComedyReels"
              " #Trending #Viral"
          ),
          "query": (
              "cute smart 3d animated baby pointing finger innocently, Pixar"
              " animation style"
          ),
      },
      # --- Category 2: Amazing Facts & Knowledge ---
      {
          "text": (
              "Duniya mein jitne log hain,\nusse kahin zyada ped dharti par"
              " maujood hain!"
          ),
          "caption": (
              "Kya aapko yeh baat pata thi? 🌳 Nature hamari soch se kahin zyada"
              " khubsurat hai! Apne dost ko tag karo! 👇\n\n#NatureLovers #Facts"
              " #ViralReels #Trending #DidYouKnow"
          ),
          "query": "anime forest landscape scenery aesthetic, beautiful nature",
      },
      {
          "text": (
              "Insani dimaag ek din mein\nlagbhag 60,000 alag-alag vichaar\nsochta"
              " hai!"
          ),
          "caption": (
              "Aapke dimaag mein abhi kya chal raha hai? 🤯 Itne vicharon mein se"
              " aap kis baare mein sochte ho? Comments mein batao! 👇\n\n"
              "#HumanBrain #PsychologyFacts #Viral #MindBlown #Knowledge"
          ),
          "query": "anime starry night sky aesthetic lofi, galaxy stars",
      },
      {
          "text": (
              "Pani ki bottle par jo expiry date\nhoti hai woh pani ki nahi,\nbalki"
              " bottle ki hoti hai!"
          ),
          "caption": (
              "Yeh sach jaan kar aap bhi chaunk gaye na? 💧 Kitne logo ko yeh"
              " galatfahmi thi? Video ko share karo! 👇\n\n#Water"
              " #FactsThatBlowYourMind #ViralVideo #Trending"
          ),
          "query": "anime rain city aesthetic night, neon lights reflection",
      },
      {
          "text": "Titali apne pairon se kisi bhi\ncheez ka swaad chakhti hai!",
          "caption": (
              "Kudrat ke raaz hairan karne wale hain! 🦋 Aise hi aur rochak tathya"
              " roz dekhne ke liye follow karein! 👇\n\n#Insects #NatureFacts"
              " #Viral #Trending #FactsDaily"
          ),
          "query": "anime flower field butterfly sunny day aesthetic",
      },
  ]

  chosen = random.choice(master_pool)
  return chosen["text"], chosen["caption"], chosen["query"]


def download_background_image(query):
  """Topic ke hisab se cinematic background image download karega"""
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
  """gTTS se clear aur fast Hindi voice generate karega"""
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
  story_text, viral_caption, query = get_random_unique_content()
  print(f"Selected Content: {story_text}")

  has_image = download_background_image(query)
  generate_hindi_voice(story_text)

  print(
      "Step 1.2: Compiling video with clean text (No background box, shadow"
      " enabled)..."
  )
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
