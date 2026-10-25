# =====================================================================
# 🎬 100% डेली ऑटोमैटिक फेसबुक रील्स + यूट्यूब शॉर्ट्स डुअल सॉफ्टवेयर (फॉन्ट फिक्स)
# =====================================================================

import os
import requests
import json
import time
import subprocess

print("⏳ सॉफ्टवेयर के जरूरी टूल्स और फॉन्ट पैकेज लोड हो रहे हैं...")
# 🔥 यहाँ हमने fonts-freefont-ttf भी इंस्टॉल करवा दिया है ताकि अक्षर लिखने में एरर न आए
subprocess.run("sudo apt-get update && sudo apt-get install -y fonts-freefont-ttf", shell=True)
subprocess.run("pip install --upgrade requests yt-dlp google-api-python-client google-auth-oauthlib google-auth-httplib2", shell=True)
print("✅ सभी टूल्स और फोंट्स लोड हो गए हैं!\n")

from yt_dlp import YoutubeDL
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials

# ⚙️ गिटहब के सुरक्षित लॉकर से फेसबुक और यूट्यूब की चाबियां उठाना
FACEBOOK_PAGE_ID = os.environ.get("FB_PAGE_ID")
FACEBOOK_ACCESS_TOKEN = os.environ.get("FB_ACCESS_TOKEN")

YT_CLIENT_ID = os.environ.get("YT_CLIENT_ID")
YT_CLIENT_SECRET = os.environ.get("YT_CLIENT_SECRET")
YT_REFRESH_TOKEN = os.environ.get("YT_REFRESH_TOKEN")

# 🔗 100% सेफ डायरेक्ट पब्लिक लिंक
VIDEO_URL = "https://w3schools.com"

FUNNY_TEXT_ON_VIDEO = "End tak dekho, hansi nahi rukegi!"
VIDEO_CAPTION = "End tak dekho, hansi nahi rukegi! 🤣🔥 #shorts #funny #movies #viral #comedy"

INPUT_VIDEO = "original_movie_clip.mp4"
OUTPUT_REEL = "funny_facebook_reel.mp4"

# ---------------------------------------------------------------------
# 🎥 कार्य 1 & 2: सेफ डाउनलोड और सुपरफास्ट FFmpeg एडिटिंग
# ---------------------------------------------------------------------
def prepare_video():
    print("🔍 सेफ सोर्स से फनी मूवी क्लिप डाउनलोड की जा रही है...")
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        r = requests.get(VIDEO_URL, stream=True, headers=headers, verify=False)
        with open(INPUT_VIDEO, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024*1024):
                if chunk:
                    f.write(chunk)
        print("🎉 वीडियो सफलतापूर्वक डाउनलोड हो गया!\n")
        
        print("🎬 वीडियो एडिटिंग और फनी कंटेंट जोड़ने की प्रक्रिया शुरू...")
        # 🛠️ यहाँ हमने बिल्कुल सही फॉन्ट पाथ सेट कर दिया है ताकि एरर आने का रास्ता ही बंद हो जाए
        font_path = "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf"
        ffmpeg_cmd = (
            f'ffmpeg -i {INPUT_VIDEO} -vf "crop=ih*9/16:ih:(iw-ow)/2:0,setpts=PTS/1.03,eq=contrast=1.06:saturation=1.1,'
            f'drawtext=fontfile={font_path}:text=\'{FUNNY_TEXT_ON_VIDEO}\':x=(w-text_w)/2:y=80:fontsize=28:fontcolor=yellow:box=1:boxcolor=black@0.6:boxborderw=10" '
            f'-af "atempo=1.03" -c:v libx264 -preset ultrafast -crf 26 -c:a aac -b:a 128k {OUTPUT_REEL} -y'
        )
        subprocess.run(ffmpeg_cmd, shell=True, check=True)
        print("🎉 फनी शॉर्ट्स वीडियो तैयार हो गया है!\n")
        return True
    except Exception as e:
        print(f"❌ वीडियो बनाने में खराबी आई: {e}")
        return False

# ---------------------------------------------------------------------
# 👥 कार्य 3: फेसबुक पेज पर अपलोड करना
# ---------------------------------------------------------------------
def upload_to_facebook():
    if not FACEBOOK_PAGE_ID or not FACEBOOK_ACCESS_TOKEN:
        print("⚠️ फेसबुक की चाबियां गायब हैं, फेसबुक अपलोड स्किप किया गया।")
        return
    print("🚀 फेसबुक पेज पर रील अपलोड की जा रही है...")
    try:
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
        print("✅ वीडियो फाइल फेसबुक सर्वर पर ट्रांसफर हो गई!")
        
        publish_url = f"https://facebook.com{FACEBOOK_PAGE_ID}/video_reels"
        publish_payload = {
            'upload_phase': 'finish',
            'video_id': video_id,
            'video_state': 'PUBLISHED',
            'description': VIDEO_CAPTION,
            'access_token': FACEBOOK_ACCESS_TOKEN
        }
        time.sleep(5)
        publish_res = requests.post(publish_url, data=publish_payload).json()
        if publish_res.get('success') or 'fb_id' in publish_res:
            print("🔥 धमाका! फेसबुक पेज पर रील 100% लाइव हो चुकी है!")
        else:
            print(f"❌ फेसबुक पब्लिश एरर: {publish_res}")
    except Exception as e:
        print(f"❌ फेसबुक अपलोडिंग में तकनीकी खराबी: {e}")

# ---------------------------------------------------------------------
# 📺 कार्य 4: यूट्यूब शॉर्ट्स पर अपलोड करना
# ---------------------------------------------------------------------
def upload_to_youtube():
    if not YT_CLIENT_ID or not YT_CLIENT_SECRET or not YT_REFRESH_TOKEN:
        print("⚠️ यूट्यूब की चाबियां गायब हैं, यूट्यूब अपलोड स्किप किया गया।")
        return
    print("🚀 यूट्यूब चैनल पर शॉर्ट्स अपलोड की जा रही है...")
    try:
        creds = Credentials(
            token=None,
            refresh_token=YT_REFRESH_TOKEN,
            token_uri="https://googleapis.com",
            client_id=YT_CLIENT_ID,
            client_secret=YT_CLIENT_SECRET
        )
        youtube = build("youtube", "v3", credentials=creds)
        
        body = {
            "snippet": {
                "title": "Bollywood Comedy Scene #shorts",
                "description": VIDEO_CAPTION,
                "tags": ["shorts", "funny", "comedy", "movie"],
                "categoryId": "23" 
            },
            "status": {
                "privacyStatus": "public", 
                "selfDeclaredMadeForKids": False
            }
        }
        
        media = MediaFileUpload(OUTPUT_REEL, chunksize=-1, resumable=True, mimetype="video/mp4")
        request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)
        
        response = None
        while response is None:
            status, response = request.next_chunk()
            if status:
                print(f"⏳ अपलोड हो रहा है: {int(status.progress() * 100)}%")
        print(f"🎉 धमाका! यूट्यूब शॉर्ट्स पर वीडियो लाइव हो गया! वीडियो आईडी: {response['id']}")
    except Exception as e:
        print(f"❌ यूट्यूब अपलोडिंग में तकनीकी खराबी: {e}")

if __name__ == "__main__":
    print("🏁 --- डुअल ऑटोमेशन बॉट चालू हो रहा है --- 🏁\n")
    if prepare_video():
        upload_to_facebook()
        print("")
        upload_to_youtube()
    print("\n🏁 --- प्रक्रिया पूरी तरह समाप्त --- 🏁")
