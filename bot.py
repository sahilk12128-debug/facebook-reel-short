import os
import random
import subprocess
import requests

FACEBOOK_PAGE_ID = "1322066784333919"
FB_ACCESS_TOKEN = os.environ.get("FB_ACCESS_TOKEN")

INPUT_VIDEO = "movie.mp4"
OUTPUT_VIDEO = "final_reel.mp4"

FACT_CAPTIONS = [
    "🧠 Kya aapko pata hai? Yeh fact aapko hairan kar dega! 🤯 #Facts #Knowledge #DailyFacts #Trending",
    "😂 Jab logic chat par jaye aur funny moments shuru ho jayein! 🍿 #FunnyReels #Comedy #Laughs",
    "💡 Amazing fact jo 99% log nahi jaante! Check this out. 👇 #MindBlown #DidYouKnow #Viral",
    "🔥 Sabse funny aur unexpected moment! Last tak zaroor dekhna. 🤣 #Humor #ReelsIndia #Explore"
]

def prepare_reel_video():
    print("Step 1: Video ko Facebook Reels format (1080x1920) mein fix kiya ja raha hai...")
    if not os.path.exists(INPUT_VIDEO):
        print(f"❌ Error: {INPUT_VIDEO} nahi mili!")
        return False
        
    # FFmpeg command jo video ko Facebook Reels ke liye perfectly format karegi
    ffmpeg_cmd = [
        "ffmpeg", "-y", "-i", INPUT_VIDEO,
        "-vf", "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920",
        "-c:v", "libx264", "-preset", "fast", "-crf", "23",
        "-c:a", "aac", "-b:a", "128k", "-ar", "48000",
        OUTPUT_VIDEO
    ]
    
    result = subprocess.run(ffmpeg_cmd)
    if result.returncode == 0 and os.path.exists(OUTPUT_VIDEO):
        print("✅ Video successfully Facebook format mein convert ho gayi hai!")
        return True
    else:
        print("❌ Video conversion fail ho gayi!")
        return False

def upload_daily_video():
    print("Step 2: Facebook upload process shuru ho raha hai...")
    
    if not FB_ACCESS_TOKEN:
        print("❌ Error: FB_ACCESS_TOKEN missing hai!")
        return
        
    if not os.path.exists(OUTPUT_VIDEO):
        print(f"❌ Error: {OUTPUT_VIDEO} file nahi mili!")
        return

    selected_caption = random.choice(FACT_CAPTIONS)
    print(f"📝 Selected Caption: {selected_caption}")

    try:
        print("Step 3: Facebook upload session create ho raha hai...")
        url = f"https://graph.facebook.com/v18.0/{FACEBOOK_PAGE_ID}/video_reels"
        payload = {"upload_phase": "START", "access_token": FB_ACCESS_TOKEN}
        response = requests.post(url, data=payload).json()
        
        if "video_id" not in response or "upload_url" not in response:
            print(f"❌ Facebook Start Failed: {response}")
            return
            
        video_id = response["video_id"]
        upload_url = response["upload_url"]
        
        print(f"Step 4: Formatted video bytes Facebook par upload ki ja rahi hain... (ID: {video_id})")
        with open(OUTPUT_VIDEO, "rb") as video_file:
            video_bytes = video_file.read()
            
        headers = {
            "Authorization": f"OAuth {FB_ACCESS_TOKEN}",
            "offset": "0",
            "file_size": str(len(video_bytes))
        }
        requests.post(upload_url, headers=headers, data=video_bytes)
        
        print("Step 5: Reel publish ki ja rahi hai...")
        publish_url = f"https://graph.facebook.com/v18.0/{FACEBOOK_PAGE_ID}/video_reels"
        publish_payload = {
            "upload_phase": "FINISH",
            "video_state": "PUBLISHED",
            "description": selected_caption,
            "video_id": video_id,
            "access_token": FB_ACCESS_TOKEN
        }
        publish_response = requests.post(publish_url, data=publish_payload).json()
        print(f"Publish Response: {publish_response}")
        
        if publish_response.get("success"):
            print("🎉 Success! Formatted Reel successfully Facebook par publish ho gayi hai.")
        else:
            print(f"⚠️ Response warning: {publish_response}")
            
    except Exception as e:
        print(f"❌ Error during upload: {str(e)}")

if __name__ == "__main__":
    if prepare_reel_video():
        upload_daily_video()
