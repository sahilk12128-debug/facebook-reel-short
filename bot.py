import os
import random
import requests
import textwrap
from PIL import Image, ImageDraw, ImageFont

# Aapke Facebook Page ki ID
FACEBOOK_PAGE_ID = "1322066784333919"
FB_ACCESS_TOKEN = os.environ.get("FB_ACCESS_TOKEN")

# Shuddh Hindi (Devanagari) ke dynamic parts (0% repetition)
PART_1 = [
    "महाभारत के पावन ज्ञान के अनुसार",
    "श्री भगवद्गीता का महान संदेश है कि",
    "रामायण की मर्यादा और पवित्र नीति कहती है कि",
    "सनातन साहित्य और ज्ञान के अनुसार",
    "प्राचीन ग्रंथों का अनमोल विचार है कि"
]

PART_2 = [
    "अपना कर्म बिना किसी फल की चिंता के पूरी निष्ठा से करना चाहिए।",
    "क्रोध और अहंकार का त्याग कर हमेशा सत्य के मार्ग पर चलना चाहिए।",
    "दूसरों की भलाई और सेवा को ही अपना सबसे बड़ा धर्म मानना चाहिए।",
    "अपनी सच्ची मेहनत और आत्मविश्वास से हर कठिनाई का सामना करना चाहिए।",
    "अपने मन और इंद्रियों पर संयम रखकर जीवन को सफल बनाना चाहिए।"
]

AUTHOR_LIST = [
    "— श्री कृष्ण (महाभारत)",
    "— रामायण सार",
    "— सनातन साहित्य",
    "— गीता ज्ञान",
    "— नीति वचन"
]

def generate_dynamic_hindi_quote():
    text = f"{random.choice(PART_1)}\n{random.choice(PART_2)}\n\n{random.choice(AUTHOR_LIST)}"
    return text

def create_designer_frame():
    print("Step 1: Shuddh Hindi designer frame image banayi ja rahi hai...")
    
    width, height = 1080, 1080
    
    # Aesthetic background paper color
    img = Image.new("RGB", (width, height), color="#FBF9F5")
    draw = ImageDraw.Draw(img)
    
    # Professional double border
    draw.rectangle([90, 90, width - 90, height - 90], outline="#1A1A1A", width=8)
    draw.rectangle([105, 105, width - 105, height - 105], outline="#9C7C38", width=3)
    
    # Dynamic Shuddh Hindi text
    raw_text = generate_dynamic_hindi_quote()
    
    # Text wrapping: Width ko chota rakha hai taaki Hindi text frame ke andar hi rahe
    wrapped_lines = []
    for paragraph in raw_text.split('\n'):
        if paragraph.strip() == "":
            wrapped_lines.append("")
        else:
            wrapped_lines.extend(textwrap.wrap(paragraph, width=28))
    
    formatted_text = "\n".join(wrapped_lines)
    
    # Font load karna (Linux system default font ya fallback)
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 34)
    except Exception:
        font = ImageFont.load_default()

    # Text ko frame ke bilkul center mein align karna
    bbox = draw.multiline_textbbox((0, 0), formatted_text, font=font, spacing=20)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    
    x = (width - text_w) / 2
    y = (height - text_h) / 2
    
    draw.multiline_text((x, y), formatted_text, fill="#2C2C2C", font=font, align="center", spacing=20)
    
    image_path = "hindi_designer_frame.jpg"
    img.save(image_path)
    print(f"✅ Shuddh Hindi frame image ready ho gayi: {image_path}")
    return image_path, raw_text

def post_frame_to_facebook():
    if not FB_ACCESS_TOKEN:
        print("❌ Error: FB_ACCESS_TOKEN missing hai!")
        return

    image_path, caption_text = create_designer_frame()

    try:
        print("Step 2: Facebook Page par upload kiya ja raha hai...")
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
                print("🎉 Success! Shuddh Hindi post Facebook par live ho gayi hai.")
            else:
                print(f"⚠️ Response warning: {response}")
                
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    post_frame_to_facebook()
