import os
import subprocess
import requests
import yt_dlp

# आपकी Facebook Page ID और Access Token यहाँ सेट हैं
FACEBOOK_PAGE_ID = "1322066784333919"
FACEBOOK_ACCESS_TOKEN = "EAAQcE9ZBE5XcBS0eXCOzM59mbl7hh6EuEnTYvb9dmscZCuVPwTNPcZA48htXvkYAa1zmdthG8prPf9PMTsl09CrZCBHX4T5jHVdqJAqdGE13yTnoO0L4Mur1MiDiP0ADVksyqzF5dlhmtlsYgNIJj10WaFAkVtcobHwcYpygCyGPT6vDAZCWYs00Wb6ZAuRjfhZAxPVg4S5ZAqL9hZBFYH33NkQaxwZCO3oOZAt"
VIDEO_PATH = "reel.mp4"
RAW_VIDEO = "raw.mp4"

def download_and_process_video():
    print("Step 1: Searching and downloading a viral/short video...")
    
    # आप यहाँ अपनी पसंद का कोई भी शॉर्ट वीडियो का सर्च टर्म या डायरेक्ट लिंक दे सकते हैं
    search_query = "ytsearch1:movie short viral reels shorts"
    
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': RAW_VIDEO,
        'noplaylist': True,
        'max_downloads': 1,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([search_query])
        print("✅ Video downloaded successfully.")
        
        # Step 2: Anti-Copyright Processing (FFmpeg के ज़रिए वीडियो को थोड़ा मॉडिफाई करना)
        print("Step 2: Processing video to prevent copyright issues (Editing metadata, slight speed/filter adjustment)...")
        # यह कमांड वीडियो का थोड़ा सा फ़्रेम और ऑडियो बदलकर उसे यूनिक बना देती है ताकि कॉपीराइट क्लेम न आए
        ffmpeg_command = [
            'ffmpeg', '-y', '-i', RAW_VIDEO,
            '-vf', "eq=brightness=0.03:saturation=1.1", # हल्का सा रंग और ब्राइटनेस बदलना
            '-af', 'asetrate=44100*1.02', # ऑडियो की पिच हल्की सी बदलना ताकि ऑटोमैटिक कॉपीराइट मैच न हो
            '-t', '55', # रील्स के लिए वीडियो को 55 सेकंड के अंदर रखना
            VIDEO_PATH
        ]
        
        subprocess.run(ffmpeg_command, check=True)
        print("✅ Video processed and edited successfully as 'reel.mp4'.")
        
    except Exception as e:
        print(f"❌ Error during download/processing: {str(e)}")
        raise e

def upload_to_facebook():
    print("Step 3: Starting Facebook Reel Upload process...")

    if not os.path.exists(VIDEO_PATH):
        print(f"❌ Error: Processed video file '{VIDEO_PATH}' not found!")
        return

    try:
        # Step 4: Initialize the Reel Upload Session with Facebook
        print("Step 4: Initializing video upload session with Facebook...")
        url = f"https://graph.facebook.com/v18.0/{FACEBOOK_PAGE_ID}/video_reels"
        payload = {
            'upload_phase': 'initialize',
            'access_token': FACEBOOK_ACCESS_TOKEN
        }
        
        response_raw = requests.post(url, data=payload)
        print(f"Facebook Raw Response: {response_raw.text}")
        
        response = response_raw.json()
        
        if 'video_id' not in response or 'upload_url' not in response:
            print(f"❌ Facebook Initialization Failed: {response}")
            return
            
        video_id = response['video_id']
        upload_url = response['upload_url']
        print(f"✅ Initialization successful! Video ID: {video_id}")

        # Step 5: Upload the Video Binary
        print("Step 5: Uploading video binary data to Facebook...")
        with open(VIDEO_PATH, 'rb') as video_file:
            video_bytes = video_file.read()
            
        headers = {
            'Authorization': f'OAuth {FACEBOOK_ACCESS_TOKEN}',
            'offset': '0',
            'file_size': str(len(video_bytes))
        }
        
        upload_response = requests.post(upload_url, headers=headers, data=video_bytes).json()
        print(f"Upload Binary Response: {upload_response}")
        print("✅ Video binary uploaded successfully.")

        # Step 6: Finish/Publish the Reel
        print("Step 6: Publishing the Reel on Facebook...")
        publish_url = f"https://graph.facebook.com/v18.0/{FACEBOOK_PAGE_ID}/video_reels"
        publish_payload = {
            'upload_phase': 'finish',
            'video_state': 'PUBLISHED',
            'description': 'Automated Daily Movie Short Reel #shorts #viral',
            'video_id': video_id,
            'access_token': FACEBOOK_ACCESS_TOKEN
        }
        
        publish_response = requests.post(publish_url, data=publish_payload).json()
        print(f"Publish Response: {publish_response}")
        
        if publish_response.get('success'):
            print("🎉 Success! Facebook Reel published successfully.")
        else:
            print(f"⚠️ Warning/Error during publish: {publish_response}")

    except Exception as e:
        print(f"❌ An exception occurred during upload: {str(e)}")

if __name__ == "__main__":
    download_and_process_video()
    upload_to_facebook()
