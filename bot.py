import os
import random
import requests

# Aapke Facebook Page ki ID
FACEBOOK_PAGE_ID = "1322066784333919"
FB_ACCESS_TOKEN = os.environ.get("FB_ACCESS_TOKEN")

# 1. Mahabharat ke Vichar
MAHABHARAT_LINES = [
    "Mahabharat mein Shri Krishna ka sandesh hai ki manushya ka sabse bada dharm apna kartavya nibhana hai.",
    "Mahabharat ki seekh kehti hai ki krodh aur ahankar vyakti ke poore vivek ko nasht kar dete hain.",
    "Mahabharat ka gyan hamein yeh sikhata hai ki sachchai aur karm ki raah par chalne wale ki kabhi haar nahi hoti."
]

# 2. Ramayan ke Vichar
RAMAYAN_LINES = [
    "Ramayan kehti hai ki jeevan mein maryada, sanyam aur sanskar hi sabse badi poonji hain.",
    "Ramayan ka patra-parichay aur tyag hamein yeh sikhata hai ki parivar aur samaj ko jodkar rakhna hi satcha dharm hai.",
    "Ramayan ki pavitra seekh ke anusar, kathin se kathin samay mein bhi satya ka sath kabhi nahi chhodna chahiye."
]

# 3. Hindi Sahitya ke Vichar
SAHITYA_LINES = [
    "Hindi sahitya ke anusar, manushya apne vicharon se hi banta hai, jaisa woh sochta hai waisa hi ban jata hai.",
    "Sahitya aur anmol vachanon mein kaha gaya hai ki andhera kitna bhi ghana ho, ek chota sa deepak use roshan kar deta hai.",
    "Hindi sahitya ka saar yeh hai ki sachchi mehnat aur imandari ka rasta sabse kathin hota hai par sukoon wahi deta hai."
]

def generate_mixed_hindi_quote():
    # Mahabharat, Ramayan aur Sahitya teeno se ek-ek line uthakar ya mix karke ekdam naya vichar banayenge
    source_choice = random.choice(["Mahabharat", "Ramayan", "Sahitya"])
    
    if source_choice == "Mahabharat":
        line = random.choice(MAHABHARAT_LINES)
        tag = "#Mahabharat #ShriKrishna #Karma"
    elif source_choice == "Ramayan":
        line = random.choice(RAMAYAN_LINES)
        tag = "#Ramayan #LordRama #Dharma"
    else:
        line = random.choice(SAHITYA_LINES)
        tag = "#HindiSahitya #LifeLessons #DeepThoughts"
        
    return line, tag

def post_hindi_literature():
    print("Step 1: Mahabharat, Ramayan aur Hindi Sahitya se vichar taiyar kiya ja raha hai...")
    
    if not FB_ACCESS_TOKEN:
        print("❌ Error: FB_ACCESS_TOKEN missing hai! GitHub Secrets check karein.")
        return

    quote_text, source_tag = generate_mixed_hindi_quote()
    
    # Har post ko 100% unique banane ke liye random ID
    final_message = f"📜 '{quote_text}'\n\n#FilmClub #SanatanDharm {source_tag} #{random.randint(10000, 99999)}"
    print(f"📝 Generated Post:\n{final_message}")

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
    post_hindi_literature()
