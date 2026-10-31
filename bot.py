import os
import random
import requests
from PIL import Image, ImageDraw, ImageFont

# Aapke Facebook Page ki ID
FACEBOOK_PAGE_ID = "1322066784333919"
FB_ACCESS_TOKEN = os.environ.get("FB_ACCESS_TOKEN")

# Yahan koi fix line nahi hai, ye alag-alag parts hain jo har baar nayi line banayenge (0% repetition)
PART_1 = [
    "Mahabharat ke paavan gyan anusar",
    "Shri Bhagavad Geeta ka mahan sandesh hai ki",
    "Ramayan ki maryada aur pavitra niti kehti hai ki",
    "Sanatan sahitya aur gyan ke anusar",
    "Prachin grantho ka anmol vichar hai ki"
]

PART_2 = [
    "apna karm bina kisi fal ki chinta ke poori nishtha se karna chahiye.",
    "krodh aur ahankaar ko tyag kar hamesha satya ke marg par chalna chahiye.",
    "dusron ki bhalai aur seva ko hi apna sabse bada dharm manna chahiye.",
    "apni sachchi mehnat aur aatm-vishwas se har kathinai ka samna karna chahiye.",
    "apne man aur indriyon par sanyam rakhkar jeevan ko safal banana chahiye."
]

AUTHOR_LIST = [
    "— Shri Krishna (Mahabharat)",
    "— Ramayan Saar",
    "— Sanatan Sahitya",
    "— Geeta Gyan",
    "— Niti Vachan"
]

def generate_dynamic_hindi_quote():
    # Har baar alag tukde judkar ekdam nayi line banayenge
    text = f"{random.choice(PART_1)} {random.choice(PART_2)}\n\n{random.choice(AUTHOR_LIST)}"
    return text

def create_designer_frame():
    print("Step 1: Sundar designer frame aur shuddh Hindi text wali image banayi ja rahi hai...")
    
    width, height = 1080, 1080
    
    # Aesthetic background paper color (Cream/Off-white)
    img = Image.new("RGB", (width, height), color="#FBF9F5")
    draw = ImageDraw.Draw(img)
    
    # Professional double border/frame (Dark and Gold theme)
    draw.rectangle([60, 60, width - 60, height - 60], outline="#1A1A1A", width=8)
    draw.rectangle([75, 75, width - 75, height - 75], outline="#9C7C38", width=3)
    
    # Dynamic unique Hindi text
    hindi_text = generate_dynamic_hindi_quote()
    
    # Font load karna
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 38)
    except Exception:
        font = ImageFont.load_default()

    # Text ko frame ke center mein align karna
    bbox = draw.multiline_textbbox((0, 0), hindi_text, font=font, spacing=25)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    
    x = (width - text_w) / 2
    y = (height - text_h) / 2
    
    draw.multiline_text((x, y), hindi_text, fill="#2C2C2C", font=font, align="center", spacing=25)
    
    image_path = "hindi_designer_frame.jpg"
    img.save(image_path)
    print(f"✅ Designer frame image successfully ready ho gayi: {image_path}")
    return image_path, hindi_text

def post_frame_to_facebook():
    if not FB_ACCESS_TOKEN:
        print("❌ Error: FB_ACCESS_TOKEN missing hai! GitHub Secrets check karein.")
        return

    image_path, caption_text = create_designer_frame()

    try:
        print("Step 2: Facebook Page par designer frame wali photo upload ki ja rahi hai...")
        url = f"https://graph.facebook.com/v18.0/{FACEBOOK_PAGE_ID}/photos"
        
        with open(image_path, "rb") as img_file:
            files = {"source": img_file}
            payload = {
                "caption": f"📜 {caption_text}\n\n#FilmClub #Mahabharat #Ramayan #HindiSahitya #SanatanDharm #{random.randint(10000, 99999)}",
                "access_token": FB_ACCESS_TOKEN
            }
            
            response = requests.post(url, data=payload, files=files).json()
            print(f"Facebook Response: {response}")
            
            if "id" in response:
                print("🎉 Success! Designer frame aur Hindi text wali post Facebook page par live ho gayi hai.")
            else:
                print(f"⚠️ Response warning: {response}")
                
    except Exception as e:
        print(f"❌ Error during posting image: {str(e)}")

if __name__ == "__main__":
    post_frame_to_facebook()
