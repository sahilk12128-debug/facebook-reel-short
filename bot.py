import os
import random
import requests

# Aapke Facebook Page ki ID
FACEBOOK_PAGE_ID = "1322066784333919"
FB_ACCESS_TOKEN = os.environ.get("FB_ACCESS_TOKEN")

def post_unique_quote_from_internet():
    print("Step 1: Internet se bilkul nayi aur unique line fetch ki ja rahi hai...")
    
    if not FB_ACCESS_TOKEN:
        print("❌ Error: FB_ACCESS_TOKEN missing hai! GitHub Secrets check karein.")
        return

    # Default fallback agar internet fail ho
    quote_text = "Karm karo, fal ki chinta mat karo."
    author = "Mahabharat"
    
    try:
        # Direct free public API se fresh quote lana (kisi list ki zaroorat nahi)
        response = requests.get("https://api.quotable.io/random", timeout=10, verify=False)
        if response.status_code == 200:
            data = response.json()
            quote_text = data.get("content", quote_text)
            author = data.get("author", "Unknown")
    except Exception as e:
        print(f"⚠️ API warning: {e}")

    # Facebook post ke liye message (saath mein random number taaki Facebook duplicate na roke)
    final_message = f"💡 {quote_text}\n\n— {author}\n\n#FilmClub #Mahabharat #Ramayan #HindiSahitya #DailyQuotes #{random.randint(10000, 99999)}"
    print(f"📝 Generated Unique Post: {final_message}")

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
            print("🎉 Success! Bilkul nayi unique post Facebook page par live ho gayi hai.")
        else:
            print(f"⚠️ Response warning: {response}")
            
    except Exception as e:
        print(f"❌ Error during posting: {str(e)}")

if __name__ == "__main__":
    post_unique_quote_from_internet()
