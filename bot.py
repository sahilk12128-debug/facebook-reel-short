# =====================================================================
# 🎬 100% डेली ऑटोमैटिक फेसबुक रील्स अपलोड बॉट
# =====================================================================
import os
import requests
import json
import time
import subprocess

print("⏳ सॉफ्टवेयर के जरूरी टूल्स लोड हो रहे हैं...")
subprocess.run("pip install --upgrade requests yt-dlp", shell=True)
print("✅ सभी जरूरी टूल्स लोड हो गए हैं!\n")

# ⚙️ गिटहब के सुरक्षित लॉकर से फेसबुक की चाबियां उठाना
FACEBOOK_PAGE_ID = os.environ.get("FB_PAGE_ID")
FACEBOOK_ACCESS_TOKEN = os.environ.get("FB_ACCESS_TOKEN")

# 🔗 वीडियो लिंक और कैप्शन
VIDEO_URL = "https://w3schools.com"
VIDEO_CAPTION = "End tak dekho, hansi nahi rukegi! 🤣🔥 #shorts #funny #viral"
INPUT_VIDEO = "downloaded_clip.mp4"
OUTPUT_REEL = "funny_facebook_reel.mp4"

# ---------------------------------------------------------------------
# 🎥 कार्य 1: डाउनलोड और डिजिटल एंटी-कॉपीराइट बदलाव
# ---------------------------------------------------------------------
def prepare_video():
    print("🔍 वीडियो डाउनलोड की जा रही है...")
    try:
        if os.path.exists(INPUT_VIDEO):
            os.remove(INPUT_VIDEO)
        if os.path.exists(OUTPUT_REEL):
            os.remove(OUTPUT_REEL)
            
        headers = {'User-Agent': 'Mozilla/5.0'}
        r = requests.get(VIDEO_URL, stream=True, headers=headers, verify=False)
        
        with open(INPUT_VIDEO, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024*1024):
                if chunk:
                    f.write(chunk)
                    
        print("🎉 वीडियो सफलतापूर्वक डाउनलोड हो गया!\n")
        print("🎬 एंटी-कॉपीराइट कोडिंग बदलाव शुरू...")
        
        with open(INPUT_VIDEO, 'rb') as f_in:
            video_data = f_in.read()
            
        # 🔥 एंटी-कॉपीराइट बाइट्स जोड़ना
        extra_bytes = b"\x00\x01\x02\x03\x04" 
        
        with open(OUTPUT_REEL, 'wb') as f_out:
            f_out.write(video_data + extra_bytes)
            
        print("🎉 एंटी-कॉपीराइट वीडियो पूरी तरह तैयार है!\n")
        return True
        
    except Exception as e:
        print(f"❌ वीडियो बनाने में खराबी आई: {e}")
        return False

# ---------------------------------------------------------------------
# 👥 कार्य 2: फेसबुक पेज पर अपलोड करना
# ---------------------------------------------------------------------
def upload_to_facebook():
    if not FACEBOOK_PAGE_ID or not FACEBOOK_ACCESS_TOKEN:
        print("⚠️ फेसबुक की चाबियां गायब हैं!")
        return

    print("🚀 फेसबुक पेज पर रील अपलोड की जा रही है...")
    try:
        url = f"https://graph.facebook.com/v18.0/{FACEBOOK_PAGE_ID}/video_reels"
        payload = {
            'upload_phase': 'initialize',
            'access_token': FACEBOOK_ACCESS_TOKEN
        }
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

        print("🎬 रील लाइव की जा रही है...")
        publish_url = f"https://graph.facebook.com/v18.0/{FACEBOOK_PAGE_ID}/video_reels"
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
            print("\n🔥 धमाका! फेसबुक पेज पर रील 100% लाइव हो चुकी है! 🔥")
        else:
            print(f"❌ फेसबुक पब्लिश एरर: {publish_res}")

    except Exception as e:
        print(f"❌ फेसबुक अपलोडिंग में तकनीकी खराबी: {e}")

if __name__ == "__main__":
    print("🏁 --- फेसबुक ऑटोमेशन बॉट चालू हो रहा है --- 🏁\n")
    if prepare_video():
        upload_to_facebook()
    print("\n🏁 --- प्रक्रिया पूरी तरह समाप्त --- 🏁")
