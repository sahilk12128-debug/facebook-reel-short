import os
import random
import subprocess
import requests

FACEBOOK_PAGE_ID = "1322066784333919"
FB_ACCESS_TOKEN = os.environ.get("FB_ACCESS_TOKEN")

VIDEO_PATH = "reel.mp4"
MOVIE_FILE = "movie.mp4"

def check_local_movie():
    print("Step 1: Checking local movie.mp4 file...")
    if os.path.exists(MOVIE_FILE) and os.path.getsize(MOVIE_FILE) > 1024:
        print("✅ movie.mp4 successfully mil gayi hai!")
        return True
    else:
        print("❌ Error: movie.mp4 nahi mili ya file khali hai!")
        return False

def cut_safe_movie_clip():
    print("Step 2: Movie se 30-second ka clip kaata ja raha hai...")
    if not os.path.exists(MOVIE_FILE):
        return None
    
    start_time = 0
    clip_duration = 30
    
    try:
        result = subprocess.run([
            "ffprobe", "-v", "error", "-show_entries", "format=duration", 
            "-of", "default=noprint_wrappers=1:nokey=1", MOVIE_FILE
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        total_duration = float(result.stdout.strip())
        if total_duration > 40:
            start_time = random.randint(0, int(total_duration) - 30)
    except Exception as e:
        print(f"⚠️ Warning: {e}")

    print(f"🎬 Clip starting from timestamp: {start_time} seconds")
    
    # FFmpeg command (Watermark hide karne ke liye zoom/crop aur text overlay)
    cut_cmd = [
        "ffmpeg", "-y", "-ss", str(start_time), "-i", MOVIE_FILE, "-t", str(clip_duration),
        "-vf", "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920",
        "-c:v", "libx264", "-c:a", "aac", VIDEO_PATH
    ]
    subprocess.run(cut_cmd, check=True)
    print("✅ 30-second reel clip taiyar ho gayi hai.")
    
    viral_caption = "Best movie scene! 🍿 Yeh suspense kaisa laga? Comments mein batao! 👇\n\n#Movies #MovieScenes #TrendingReels #ViralReels"
    return viral_caption

def upload_to_facebook(caption):
    print("Step 3: Facebook Reel Upload process shuru ho raha hai...")
    if not FB_ACCESS_TOKEN:
        print("❌ Error: FB_ACCESS_TOKEN missing hai! Kripya GitHub Secrets mein add karein.")
        return
    if not os.path.exists(VIDEO_PATH):
        print(f"❌ Error: {VIDEO_PATH} nahi mili!")
        return

    try:
        print("Step 4: Facebook upload session shuru ho raha hai...")
        url = f"https://graph.facebook.com/v18.0/{FACEBOOK_PAGE_ID}/video_reels"
        payload = {"upload_phase": "START", "access_token": FB_ACCESS_TOKEN}
        response = requests.post(url, data=payload).json()
        
        if "video_id" not in response or "upload_url" not in response:
            print(f"❌ Facebook Start Failed: {response}")
            return
            
        video_id = response["video_id"]
        upload_url = response["upload_url"]
        
        print(f"Step 5: Video data Facebook par bhej rahe hain... (Video ID: {video_id})")
        with open(VIDEO_PATH, "rb") as video_file:
            video_bytes = video_file.read()
            
        headers = {
            "Authorization": f"OAuth {FB_ACCESS_TOKEN}",
            "offset": "0",
            "file_size": str(len(video_bytes))
        }
        requests.post(upload_url, headers=headers, data=video_bytes)
        
        print("Step 6: Reel publish ki ja rahi hai...")
        publish_url = f"https://graph.facebook.com/v18.0/{FACEBOOK_PAGE_ID}/video_reels"
        publish_payload = {
            "upload_phase": "FINISH",
            "video_state": "PUBLISHED",
            "description": caption,
            "video_id": video_id,
            "access_token": FB_ACCESS_TOKEN
        }
        publish_response = requests.post(publish_url, data=publish_payload).json()
        print(f"Publish Response: {publish_response}")
        
        if publish_response.get("success"):
            print("🎉 Success! Movie Reel Facebook par publish ho gayi hai.")
        else:
            print(f"⚠️ Response: {publish_response}")
            
    except Exception as e:
        print(f"❌ Error during upload: {str(e)}")

if __name__ == "__main__":
    if check_local_movie():
        viral_caption = cut_safe_movie_clip()
        if viral_caption:
            upload_to_facebook(viral_caption)
