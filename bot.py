# =====================================================================
# 🎬 100% डेली ऑटोमैटिक फेसबुक मूवी शॉर्ट्स सॉफ्टवेयर (GitHub मोड)
# =====================================================================

import os
import requests
import json
import time
import subprocess

print("⏳ सॉफ्टवेयर के जरूरी टूल्स लोड हो रहे हैं...")
subprocess.run("pip install --upgrade requests yt-dlp", shell=True)
print("✅ टूल्स लोड हो गए हैं!\n")

from yt_dlp import YoutubeDL

# ⚙️ गिटहब के सुरक्षित लॉकर से चाबियां उठाना
FACEBOOK_PAGE_ID = os.environ.get("FB_PAGE_ID")
FACEBOOK_ACCESS_TOKEN = os.environ.get("FB_ACCESS_TOKEN")

SEARCH_KEYWORD = "Bollywood comedy movie scene"
FUNNY_TEXT_ON_VIDEO = "End tak dekho, hansi nahi rukegi!"
REEL_CAPTION = "End tak dekho, hansi nahi rukegi! 🤣🔥 #shorts #funny #movies #viral #comedy"

INPUT_VIDEO = "original_movie_clip.mp4"
OUTPUT_REEL = "funny_facebook_reel.mp4"

def start_bot():
    print(f"🔍 इंटरनेट पर '{SEARCH_KEYWORD}' ढूंढा जा रहा है...")
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'default_search': 'ytsearch1:', 
        'outtmpl': INPUT_VIDEO,
        'noplaylist': True,
        'download_ranges': lambda info_dict, ydl: [{'start_time': 10, 'end_time': 70}],
        'force_keyframes_at_cuts': True,
    }
    
    try:
        # डाउनलोड
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([f"{SEARCH_KEYWORD} scene"])
        print("🎉 वीडियो सफलतापूर्वक डाउनलोड हो गया!\n")
        
        # FFmpeg एडिटिंग
        print("🎬 वीडियो एडिटिंग और फनी कंटेंट जोड़ने की प्रक्रिया शुरू...")
        ffmpeg_cmd = (
            f'ffmpeg -i {INPUT_VIDEO} -vf "crop=ih*9/16:ih:(iw-ow)/2:0,setpts=PTS/1.03,eq=contrast=1.06:saturation=1.1,'
            f'drawtext=text=\'{FUNNY_TEXT_ON_VIDEO}\':x=(w-text_w)/2:y=80:fontsize=28:fontcolor=yellow:box=1:boxcolor=black@0.6:boxborderw=10" '
            f'-af "atempo=1.03" -c:v libx264 -preset ultrafast -crf 26 -c:a aac -b:a 128k {OUTPUT_REEL} -y'
        )
        subprocess.run(ffmpeg_cmd, shell=True, check=True)
        print("🎉 फनी रील वीडियो तैयार हो गया है!\n")
        
        # फेसबुक पर अपलोड
        print("🚀 फेसबुक पेज पर रील अपलोड की जा रही है...")
        url = f"https://facebook.com{FACEBOOK_PAGE_ID}/video_reels"
        payload = {'upload_phase': 'initialize', 'access_token': FACEBOOK_ACCESS_TOKEN}
        
        response = requests.post(url, data=payload).json()
        video_id = response['video_id']
        upload_url = response['upload_url']
        
        with open(OUTPUT_REEL, 'rb') as f:
            video_data = f.read()
            
        headers = {
            'Authorization': f'OAuth {FACEBOOK_ACCESS_TOKEN}',
            'offset': '0',
            'file_size': str(len(video_data))
        }
        requests.post(upload_url, headers=headers, data=video_data)
        print("✅ video फाइल फेसबुक सर्वर पर ट्रांसफर हो गई!")
        
        # पब्लिश
        print("🎬 रील लाइव की जा रही है...")
        publish_url = f"https://facebook.com{FACEBOOK_PAGE_ID}/video_reels"
        publish_payload = {
            'upload_phase': 'finish',
            'video_id': video_id,
            'video_state': 'PUBLISHED',
            'description': REEL_CAPTION,
            'access_token': FACEBOOK_ACCESS_TOKEN
        }
        time.sleep(5)
        publish_res = requests.post(publish_url, data=publish_payload).json()
        
        if publish_res.get('success') or 'fb_id' in publish_res:
            print("\n🔥 धमाका! आपकी रील आज भी 100% ऑटोमैटिक लाइव हो चुकी है! 🔥\n")
        else:
            print(f"❌ पब्लिश करने में दिक्कत आई: {publish_res}")
            
    except Exception as e:
        print(f"❌ तकनीकी खराबी: {e}")

if __name__ == "__main__":
    start_bot()
