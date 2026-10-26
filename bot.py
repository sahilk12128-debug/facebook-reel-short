import os
import requests
import time

# Configurations from environment variables
FACEBOOK_PAGE_ID = os.getenv("FACEBOOK_PAGE_ID")
FACEBOOK_ACCESS_TOKEN = os.getenv("FACEBOOK_ACCESS_TOKEN")
VIDEO_PATH = "reel.mp4"  # Path to your video file

def upload_to_facebook():
    print("Starting Facebook Reel Upload process...")
    
    if not FACEBOOK_PAGE_ID or not FACEBOOK_ACCESS_TOKEN:
        print("❌ Error: FACEBOOK_PAGE_ID or FACEBOOK_ACCESS_TOKEN is missing in environment variables.")
        return

    if not os.path.exists(VIDEO_PATH):
        print(f"❌ Error: Video file '{VIDEO_PATH}' not found!")
        return

    try:
        # Step 1: Initialize the Reel Upload Session
        print("Step 1: Initializing video upload session with Facebook...")
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

        # Step 2: Upload the Video Binary
        print("Step 2: Uploading video binary data...")
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

        # Step 3: Finish/Publish the Reel
        print("Step 3: Publishing the Reel...")
        publish_url = f"https://graph.facebook.com/v18.0/{FACEBOOK_PAGE_ID}/video_reels"
        publish_payload = {
            'upload_phase': 'finish',
            'video_state': 'PUBLISHED',
            'description': 'Automated Daily Movie Short Reel #shorts',
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
    upload_to_facebook()
