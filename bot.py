import os
import random
import requests

# Aapke Facebook Page ki ID
FACEBOOK_PAGE_ID = "1322066784333919"
FB_ACCESS_TOKEN = os.environ.get("FB_ACCESS_TOKEN")

# Mahabharat, Ramayan aur Hindi Sahitya ke bade aur gehre vichar (Pure Hindi Paragraphs)
HINDI_PARAGRAPHS = [
    """🏹 Mahabharat ka saral aur satya sandesh yeh hai ki manushya ka jeevan uske karm par adharit hota hai. Jaise beej boyenge, waisa hi fal prapt hoga. Isiliye apne vartaman mein poori nishtha aur imandari ke sath apna kartavya karte raho, parinaam ki chinta karna Ishwar par chhod do. ✨ #Mahabharat #ShriKrishna #Karma #HindiSahitya""",
    
    """🌸 Ramayan humein yeh sikhati hai ki maryada, sanyam aur dharma ke marg par chalna chahe kitna bhi kathin kyun na ho, ant mein jeet hamesha satya ki hi hoti hai. Jeevan ke har sankat mein apne sanskar aur mulyon ko kabhi mat chhodo, yahi ek satcha manushya ki pehchan hai. 🌿 #Ramayan #LordRama #Dharma #Inspiration""",
    
    """🔥 Hindi sahitya aur sanatan gyan ke anusar, krodh aur ahankaar insaan ke sabse bade shatru hain jo uski sachi buddhi aur vivek ko nasht kar dete hain. Jo vyakti apne man aur indriyon par vijay prapt kar leta hai, vahin duniya ka sabse bada vijeta banta hai. Aapki mehnat aur sakaratmak vichar hi aapka sabse bada bal hain. 🎯 #HindiSahitya #ThoughtPower #Success""",
    
    """📚 Jeevan ek anmol yatra hai jisme kathinaiyan aur chunautiyan aana swabhavik hai. Lekin andhera kitna bhi ghana kyun na ho, ek chota sa deepak bhi us andhere ko cheer kar roshan karne ki taakat rakhta hai. Apne andar ke us vishwas aur mehnat ke diye ko kabhi bujhne mat do. 🌟 #Sahitya #Truth #LifeLessons #Motivation""",
    
    """⚔️ Maharshi Vyas dwara rchit Mahabharat humein yeh seekh deti hai ki darr aur aalasya manushya ki sabse badi kamzori hain. Jab aap apne lakshya ke prati samarpit ho jate hain aur mushkilon se ladne ka sahas rakhte hain, toh badi se badi badha bhi aapke samne jhukne par majboor ho jati hai. 🧘‍♂️ #Mahabharat #Geeta #Peace #SuccessMindset""",
    
    """🪷 Ramayan ka pratyek patra humein tyag, prem aur kartavya-nishtha ka paath padhata hai. Dusron ki bhalai ke liye jeena aur apne parivaron aur samaj ko jodkar rakhna hi satcha dharm hai. Bade vichar rakho, nek raste par chalo aur apni mehnat par poora bharosa rakho. 🙏 #Ramayan #Kindness #GoodVibes #DailyVichar"""
]

def post_hindi_paragraph():
    print("Step 1: Shuddh Hindi sahitya aur grantho se bada paragraph select kiya ja raha hai...")
    
    if not FB_ACCESS_TOKEN:
        print("❌ Error: FB_ACCESS_TOKEN missing hai! GitHub Secrets check karein.")
        return

    # List se ekdam random aur bada paragraph uthana
    selected_paragraph = random.choice(HINDI_PARAGRAPHS)
    
    # Har post ko 100% unique banane ke liye random ID jodna taaki Facebook duplicate error na de
    final_message = f"📜 {selected_paragraph}\n\n#FilmClub #Mahabharat #Ramayan #HindiSahitya #SanatanDharm #{random.randint(10000, 99999)}"
    print(f"📝 Generated Unique Paragraph:\n{final_message}")

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
            print("🎉 Success! Shuddh Hindi ka bada paragraph successfully Facebook page par live ho gaya hai.")
        else:
            print(f"⚠️ Response warning: {response}")
            
    except Exception as e:
        print(f"❌ Error during posting: {str(e)}")

if __name__ == "__main__":
    post_hindi_paragraph()
