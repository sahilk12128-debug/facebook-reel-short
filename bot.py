import os
import random
import requests

FACEBOOK_PAGE_ID = "1322066784333919"
FB_ACCESS_TOKEN = os.environ.get("FB_ACCESS_TOKEN")

VIDEO_PATH = "movie.mp4"

# Daily funny facts aur knowledge captions ki list
FACT_CAPTIONS = [
    "🧠 Kya aapko pata hai? Yeh fact aapko hairan kar dega! 🤯 #Facts #Knowledge #DailyFacts #Trending",
    "😂 Jab logic chat par jaye aur funny moments shuru ho jayein! 🍿 #FunnyReels #Comedy #Laughs",
    "💡 Amazing fact jo 99% log nahi jaante! Check this out. 👇 #MindBlown #DidYouKnow #Viral",
    "🔥 Sabse funny aur unexpected moment! Last tak zaroor dekhna. 🤣 #Humor #ReelsIndia #Explore"
]

def upload_daily_video():
    print("Step 1: Daily video upload process shuru ho raha hai...")
    
    if not FB_ACCESS_TOKEN:
        print("❌ Error: FB_ACCESS_TOKEN missing hai! GitHub Secrets check karein.")
        return
        
    if not os.path.exists(VIDEO_PATH):
        print(f"❌ Error: {VIDEO_PATH} file nahi mili repository mein!")
        return

    selected_caption = random.choice(FACT_CAPTIONS)
    print(f"📝 Selected Caption: {selected_caption}")

    try:
        print("Step 2: Facebook upload session create ho raha hai...")
        url = f"https://graph.facebook.com/v18.0/{FACEBOOK_PAGE_ID}/video_reels"
        payload = {"upload_phase": "START", "access_token": FB_ACCESS_TOKEN}
        response = requests.post(url, data=payload).json()
        
        if "video_id" not in response or "upload_url" not in response:
            print(f"❌ Facebook Start Failed: {response}")
            return
            
        video_id = response["video_id"]
        upload_url = response["upload_url"]
        
        print(f"Step 3: Video bytes Facebook par upload ki ja rahi hain... (ID: {video_id})")
        with open(VIDEO_PATH, "rb") as video_file:
            video_bytes = video_file.read()
            
        headers = {
            "Authorization": f"OAuth {FB_ACCESS_TOKEN}",
            "offset": "0",
            "file_size": str(len(video_bytes))
        }
        requests.post(upload_url, headers=headers, data=video_bytes)
        
        print("Step 4: Reel publish ki ja rahi hai...")
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
            print("🎉 Success! Daily Fact/Funny Reel successfully publish ho gayi hai.")
        else:
            print(f"⚠️ Response: {publish_response}")
            
    except Exception as e:
        print(f"❌ Error during upload: {str(e)}")

if __name__ == "__main__":
    upload_daily_video()
