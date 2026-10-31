import os
import random
import requests
from PIL import Image, ImageDraw, ImageFont

# Aapke Facebook Page ki ID
FACEBOOK_PAGE_ID = "1322066784333919"
FB_ACCESS_TOKEN = os.environ.get("FB_ACCESS_TOKEN")

# Mahabharat, Ramayan aur Hindi Sahitya ke alag-alag gehre vichar (Romanized/Clean Hindi taaki frame par saaf dikhe)
HINDI_QUOTES = [
    "\"Karm karo, fal ki chinta mat karo.\"\n— Shri Krishna (Mahabharat)",
    "\"Dharm wahi hai jo satya aur maryada ke marg par chalna sikhaye.\"\n— Ramayan",
    "\"Manushya apne vicharon se hi banta hai, jaisa sochte hain waisa bante hain.\"\n— Hindi Sahitya",
    "\"Krodh manushya ka sabse bada shatru hai, jo vivek ko nasht kar deta hai.\"\n— Mahabharat",
    "\"Andhera kitna bhi ghana ho, ek chota sa diya use roshan kar deta hai.\"\n— Sahitya ki Seekh",
    "\"Sahi samay par kiya gaya prayas aur sachchi mehnat kabhi vyarth nahi jati.\"\n— Sanatan Vichar",
    "\"Jo dusron ki bhalai ke liye jeete hain, unka jeevan sarthak ho jata hai.\"\n— Ramayan ki Seekh"
]

def create_frame_image():
    print("Step 1: Sundar frame aur Hindi text wali image create ki ja rahi hai...")
    
    # 1080x1080 Square size ki high-quality image
    width, height = 1080, 1080
    
    # Elegant aesthetic paper background color
    img = Image.new("RGB", (width, height), color="#FDFBF7")
    draw = ImageDraw.Draw(img)
    
    # Image ke chaaron taraf ek professional border/frame banana
    margin = 70
    draw.rectangle(
        [margin, margin, width - margin, height - margin],
        outline="#1B1B1B", width=8
    )
    
    # Andar ek aur patli line ka double border
    inner_margin = 85
    draw.rectangle(
        [inner_margin, inner_margin, width - inner_margin, height - inner_margin],
        outline="#8C7853", width=2
    )
    
    # Har baar ekdam random aur nayi line select karna taaki repeat na ho
    selected_quote = random.choice(HINDI_QUOTES)
    
    # Font load karna (Linux system default)
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 46)
    except Exception:
        font = ImageFont.load_default()

    # Text ko frame ke bilkul beech mein align karna
    bbox = draw.multiline_textbbox((0, 0), selected_quote, font=font, spacing=25)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    
    x = (width - text_w) / 2
    y = (height - text_h) / 2
    
    # Frame ke andar text draw karna
    draw.multiline_text((x, y), selected_quote, fill="#2C2C2C", font=font, align="center", spacing=25)
    
    # Image save karna
    image_path = "hindi_frame_post.jpg"
    img.save(image_path)
    print(f"✅ Frame image successfully ready ho gayi: {image_path}")
    return image_path, selected_quote

def post_frame_to_facebook():
    if not FB_ACCESS_TOKEN:
        print("❌ Error: FB_ACCESS_TOKEN missing hai! GitHub Secrets check karein.")
        return

    # Image aur text generate karo
    image_path, quote_caption = create_frame_image()

    try:
        print("Step 2: Facebook Page par frame wali photo upload ki ja rahi hai...")
        url = f"https://graph.facebook.com/v18.0/{FACEBOOK_PAGE_ID}/photos"
        
        with open(image_path, "rb") as img_file:
            files = {"source": img_file}
            payload = {
                "caption": f"📜 {quote_caption}\n\n#FilmClub #Mahabharat #Ramayan #HindiSahitya #SanatanDharm #{random.randint(10000, 99999)}",
                "access_token": FB_ACCESS_TOKEN
            }
            
            response = requests.post(url, data=payload, files=files).json()
            print(f"Facebook Response: {response}")
            
            if "id" in response:
                print("🎉 Success! Designer frame wali post successfully Facebook page par live ho gayi hai.")
            else:
                print(f"⚠️ Response warning: {response}")
                
    except Exception as e:
        print(f"❌ Error during uploading image: {str(e)}")

if __name__ == "__main__":
    post_frame_to_facebook()
