import os
import random
import requests
from PIL import Image, ImageDraw, ImageFont

# Aapke Facebook Page ki ID
FACEBOOK_PAGE_ID = "1322066784333919"
FB_ACCESS_TOKEN = os.environ.get("FB_ACCESS_TOKEN")

# Mahabharat, Ramayan aur Hindi Sahitya ke unique aur badhe vichar pool (Bina repeat hue random selection ke liye)
HINDI_POOL = [
    ("Karm karo, fal ki chinta mat karo.", "— Shri Krishna (Mahabharat)"),
    ("Dharm wahi hai jo satya aur maryada ke marg par chalna sikhaye.", "— Ramayan"),
    ("Manushya apne vicharon se hi banta hai, jaisa sochte hain waisa bante hain.", "— Hindi Sahitya"),
    ("Krodh manushya ka sabse bada shatru hai, jo vivek ko nasht kar deta hai.", "— Mahabharat"),
    ("Andhera kitna bhi ghana ho, ek chota sa diya use roshan kar deta hai.", "— Sahitya ki Seekh"),
    ("Sahi samay par kiya gaya prayas aur sachchi mehnat kabhi vyarth nahi jati.", "— Sanatan Vichar"),
    ("Jo dusron ki bhalai ke liye jeete hain, unka jeevan sarthak ho jata hai.", "— Ramayan ki Seekh"),
    ("Dharya aur sanyam hi manushya ki sabse badi taakat hain.", "— Mahabharat Saar")
]

def create_designer_frame():
    print("Step 1: Designer frame aur shuddh Hindi text ki image banayi ja rahi hai...")
    
    width, height = 1080, 1080
    
    # Aesthetic background paper color
    img = Image.new("RGB", (width, height), color="#F9F6F0")
    draw = ImageDraw.Draw(img)
    
    # Professional double border/frame
    draw.rectangle([60, 60, width - 60, height - 60], outline="#1A1A1A", width=8)
    draw.rectangle([75, 75, width - 75, height - 75], outline="#8C7853", width=2)
    
    # Har baar ekdam random line select hogi taaki repeat na ho
    quote, author = random.choice(HINDI_POOL)
    formatted_text = f"\"{quote}\"\n\n{author}"
    
    # Font load karna (Linux runner ke liye)
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 44)
    except Exception:
        font = ImageFont.load_default()

    # Text ko center align karna
    bbox = draw.multiline_textbbox((0, 0), formatted_text, font=font, spacing=25)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    
    x = (width - text_w) / 2
    y = (height - text_h) / 2
    
    draw.multiline_text((x, y), formatted_text, fill="#222222", font=font, align="center", spacing=25)
    
    # Image save karna
    image_path = "hindi_frame_post.jpg"
    img.save(image_path)
    print(f"✅ Frame image successfully ready ho gayi: {image_path}")
    return image_path, quote

def post_frame_to_facebook():
    if not FB_ACCESS_TOKEN:
        print("❌ Error: FB_ACCESS_TOKEN missing hai! GitHub Secrets check karein.")
        return

    image_path, quote_text = create_designer_frame()

    try:
        print("Step 2: Facebook Page par frame wali photo upload ki ja rahi hai...")
        url = f"https://graph.facebook.com/v18.0/{FACEBOOK_PAGE_ID}/photos"
        
        with open(image_path, "rb") as img_file:
            files = {"source": img_file}
            payload = {
                "caption": f"📜 {quote_text}\n\n#FilmClub #Mahabharat #Ramayan #HindiSahitya #SanatanDharm #{random.randint(10000, 99999)}",
                "access_token": FB_ACCESS_TOKEN
            }
            
            response = requests.post(url, data=payload, files=files).json()
            print(f"Facebook Response: {response}")
            
            if "id" in response:
                print("🎉 Success! Designer frame wali Hindi post Facebook par live ho gayi hai.")
            else:
                print(f"⚠️ Response warning: {response}")
                
    except Exception as e:
        print(f"❌ Error during posting image: {str(e)}")

if __name__ == "__main__":
    post_frame_to_background = post_frame_to_facebook()
