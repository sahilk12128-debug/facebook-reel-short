import os
import random
import requests

FACEBOOK_PAGE_ID = "1322066784333919"
FB_ACCESS_TOKEN = os.environ.get("FB_ACCESS_TOKEN")

# Behtareen motivational lines ki list
MOTIVATIONAL_LINES = [
    "🔥 Safalta ek din mein nahi milti, lekin agar roz mehnat karo toh ek din zaroor milti hai! 💪 #Motivation #Success #Mindset",
    "⭐ Apne sapno ko sach karne ke liye, pehle unhe dekhna zaroori hai. 🚀 #Inspiration #Goals #Hustle",
    "🎯 Mushkilein dil ke iraade azmati hain, sapno ke parde hataati hain. Haar mat maano! ✨ #NeverGiveUp #MotivationDaily",
    "💡 Khud par vishwas rakho, adhi jeet toh wahin ho jati hai! 🦅 #SelfBelief #SuccessMindset #Positivity",
    "🚀 Raaste chahe kitne bhi kathin kyun na hon, agar manzil paane ki zid hai toh rasta mil hi jayega. 🔥 #KeepGoing #Quotes"
]

def post_motivation():
    print("Step 1: Motivational post process shuru ho raha hai...")
    
    if not FB_ACCESS_TOKEN:
        print("❌ Error: FB_ACCESS_TOKEN missing hai! GitHub Secrets check karein.")
        return

    # Random motivational line select karna
    selected_quote = random.choice(MOTIVATIONAL_LINES)
    print(f"📝 Selected Quote: {selected_quote}")

    try:
        print("Step 2: Facebook Page feed par post publish ki ja rahi hai...")
        # Yahan humne /feed endpoint use kiya hai jo text/status post ke liye hota hai
        url = f"https://graph.facebook.com/v18.0/{FACEBOOK_PAGE_ID}/feed"
        payload = {
            "message": selected_quote,
            "access_token": FB_ACCESS_TOKEN
        }
        
        response = requests.post(url, data=payload).json()
        print(f"Facebook Response: {response}")
        
        if "id" in response:
            print("🎉 Success! Motivational post successfully Facebook page par live ho gayi hai.")
        else:
            print(f"⚠️ Response warning: {response}")
            
    except Exception as e:
        print(f"❌ Error during posting: {str(e)}")

if __name__ == "__main__":
    post_motivation()
