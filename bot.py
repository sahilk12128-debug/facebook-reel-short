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


def get_massive_mixed_content():
  """Unlimited Funny, Facts, Knowledge aur Stories ka Massive Master Pool"""
  print("Step 1: Selecting from massive non-repeating content pool...")

  master_pool = [
      # --- Category 1: Funny & Comedy ---
      {
          "text": (
              "Samosa khane se dimaag tez hota hai!\n\n- Arre nahi bhai, yeh toh"
              " sirf pet bharne ka bahana hai!"
          ),
          "caption": (
              "Samosa lovers kahan hain? 🥟 Tag your foodie friend! 👇\n\n"
              "#Samosa #Foodie #Comedy #ViralReels #Trending"
          ),
          "query": (
              "cute funny 3d animated character eating samosa happily, Pixar"
              " style"
          ),
      },
      {
          "text": (
              "Teacher ne poochha: 'Homer ki death kaise hui thi?'\n\nStudent"
              " bola: 'Sir, use geography ki padhai karte waqt heart attack aa"
              " gaya tha!'"
          ),
          "caption": (
              "Exam ke ajeeb jawab! 😂 Kis-kis ne paper mein aisi comedy ki hai?"
              " 👇\n\n#SchoolLife #ExamFunny #ComedyReels #Trending"
          ),
          "query": (
              "cute funny 3d animated student scratching head in classroom, Pixar"
              " style"
          ),
      },
      {
          "text": (
              "Mummi ne bola ki: Jaldi so jao warna Bhoot aa jayega!\n\nMaine"
              " bola: Bulwao use, akela bore ho raha hu!"
          ),
          "caption": (
              "Aajkal ke bachhe kisi se nahi darte! 👻 Tag your fearless friends!"
              " 👇\n\n#FunnyBaby #CuteBaby #ViralReels #Trending"
          ),
          "query": (
              "cute funny 3d animated baby smiling mischievously in a cozy"
              " bedroom, Pixar style"
          ),
      },
      {
          "text": (
              "Jab papa poochte hain: Mobile kisne toda?\n\nAur main apni ankhon"
              " se mera bhai dikha deta hu!"
          ),
          "caption": (
              "Mastermind baby! 🧠 Kis-kis ne bachpan mein yeh kiya hai?"
              " Comments mein batao! 👇\n\n#SmartBaby #CuteBaby #ComedyReels"
          ),
          "query": (
              "cute smart 3d animated baby pointing finger innocently, Pixar"
              " animation style"
          ),
      },
      # --- Category 2: Amazing Facts & Science ---
      {
          "text": (
              "Duniya ka sabse pehla camera itna slow tha ki\nphoto khinchane ke"
              " liye 8 ghante baithna padta tha!"
          ),
          "caption": (
              "Pehle ke zamane ka photography struggle! 📸 Kya aapko yeh ajeeb"
              " fact pata tha? 👇\n\n#HistoryFacts #Camera #DidYouKnow"
              " #ViralReels"
          ),
          "query": "vintage old camera retro style aesthetic photography",
      },
      {
          "text": (
              "Mars (Mangal Grah) par sunsets\nneele (blue) rang ke dikhai dete"
              " hain!"
          ),
          "caption": (
              "Space ke kitne saare raaz abhi baaki hain! 🪐 Space lovers video"
              " ko share karein! 👇\n\n#Space #Mars #AstronomyFacts #ViralVideo"
          ),
          "query": "anime space mars sunset blue landscape sci fi aesthetic",
      },
      {
          "text": (
              "Penguin ke paas namkeen paani peene ke liye\nek special gland hota"
              " hai jo namak ko bahar nikal deta hai!"
          ),
          "caption": (
              "Nature ke ajeeb aur khubsurat raaz! 🐧 Aise hi facts roz dekhne"
              " ke liye follow karein! 👇\n\n#Animals #Penguin #NatureFacts"
              " #Trending"
          ),
          "query": "cute penguins in snow ice aesthetic winter anime background",
      },
      {
          "text": (
              "Billiyaan (Cats) apni poori zindagi ka\n70 percent hissa sone"
              " mein hi bita deti hain!"
          ),
          "caption": (
              "Alsi billi! 🐱 Tag your sleeping buddy who loves to sleep all"
              " day! 👇\n\n#Cats #PetLovers #FunnyAnimals #ViralReels"
          ),
          "query": "cute sleeping cat cozy room aesthetic lofi anime style",
      },
      {
          "text": (
              "Agar aap chand par apna jhanda lagayein,\ntoh woh wahan hazaron"
              " saal tak waisa hi rahega kyunki wahan hawa hi nahi hai!"
          ),
          "caption": (
              "Space ki ek aur dilchasp baat! 🌙 Apne doston ko tag karo! 👇\n\n"
              "#Moon #SpaceFacts #Universe #TrendingReels"
          ),
          "query": (
              "anime moon night glowing aesthetic beautiful space background"
          ),
      },
      {
          "text": (
              "Duniya mein jitne log hain,\nusse kahin zyada ped dharti par"
              " maujood hain!"
          ),
          "caption": (
              "Kya aapko yeh baat pata thi? 🌳 Nature hamari soch se kahin zyada"
              " khubsurat hai! 👇\n\n#NatureLovers #Facts #ViralReels #Trending"
          ),
          "query": "anime forest landscape scenery aesthetic, beautiful nature",
      },
      {
          "text": (
              "Pani ki bottle par jo expiry date hoti hai\nwoh pani ki nahi,"
              " balki bottle ki hoti hai!"
          ),
          "caption": (
              "Yeh sach jaan kar aap bhi chaunk gaye na? 💧 Video ko share karo!"
              " 👇\n\n#Water #FactsThatBlowYourMind #ViralVideo"
          ),
          "query": "anime rain city aesthetic night, neon lights reflection",
      },
      {
          "text": (
              "Titali apne pairon se kisi bhi\ncheez ka swaad chakhti hai!"
          ),
          "caption": (
              "Kudrat ke raaz hairan karne wale hain! 🦋 Follow karein! 👇\n\n"
              "#Insects #NatureFacts #Viral #Trending"
          ),
          "query": "anime flower field butterfly sunny day aesthetic",
      },
      {
          "text": "Insan ki ankhon ka lens\n576 megapixels ka hota hai!",
          "caption": (
              "Kudrat ka sabse behtareen camera! 👁️ Is amazing fact ke liye"
              " like banta hai! 👇\n\n#HumanBody #ScienceFacts #Vision #Trending"
          ),
          "query": "anime futuristic glowing human eye cyber aesthetic",
      },
      {
          "text": (
              "Banana (Kela) aisi fruit hai\njo curve hoti hai kyunki woh suraj"
              " ki taraf ugti hai!"
          ),
          "caption": (
              "Physics aur nature ka kamaal! 🍌 Kya aapko yeh fact pata tha? 👇\n\n"
              "#Banana #ScienceFacts #DidYouKnow #Viral"
          ),
          "query": "anime tropical bright sunny banana tree aesthetic background",
      },
  ]

  chosen = random.choice(master_pool)
  print(f"✅ Selected Fresh Content: {chosen['text'][:30]}...")
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
  story_text, viral_caption, query = get_massive_mixed_content()

  has_image = download_background_image(query)
  generate_hindi_voice(story_text)

  print("Step 1.2: Compiling video with clean text...")
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
