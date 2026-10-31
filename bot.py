import os
import random
import requests

# Aapke Facebook Page ki ID
FACEBOOK_PAGE_ID = "1322066784333919"
FB_ACCESS_TOKEN = os.environ.get("FB_ACCESS_TOKEN")

def post_motivational_quote():
    print("Step 1: Internet se fresh motivational quote fetch ki ja rahi hai...")
    
    if not FB_ACCESS_TOKEN:
        print("❌ Error: FB_ACCESS_TOKEN missing hai! GitHub Secrets check karein.")
        return

    # Free public API se random quote nikalna
    quote_text = "Safalta mehnat karne walon par fida hoti hai!"
    author = "Success"
    
    try:
        response = requests.get("https://api.quotable.io/random", timeout=10)
        if response.status_code == 200:
            data = response.json()
            quote_text = data.get("content", quote_text)
            author = data.get("author", "Unknown")
    except Exception as e:
        print(f"⚠️ API warning: {e}")

    # Unique message with random ID taaki Facebook duplicate na bataye
    final_message = f"💡 {quote_text}\n\n— {author}\n\n#Motivation #Success #FilmClub #DailyQuotes #{random.randint(1000, 9999)}"
    print(f"📝 Generated Post: {final_message}")

    try:
        print("Step 2: Facebook Page feed par post publish ki ja rahi hai...")
        url = f"https://graph.facebook.com/v18.0/{FACEBOOK_PAGE_ID}/feed"
        payload = {
            "message": final_message,
            "access_token": FB_ACCESS_TOKEN
        }
        
        response = requests.post(url, data=payload).json()
        print(f"Facebook Response: {response}")
        
        if "id" in response:
            print("🎉 Success! Post successfully Facebook page par live ho gayi hai.")
        else:
            print(f"⚠️ Response warning: {response}")
            
    except Exception as e:
        print(f"❌ Error during posting: {str(e)}")

if __name__ == "__main__":
    post_motivational_quote()
