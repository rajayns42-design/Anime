from pymongo import MongoClient
import certifi
from baka.config import MONGO_URI

# Initialize Connection
RyanBaka = MongoClient(MONGO_URI, tlsCAFile=certifi.where())
db = RyanBaka["bakabot_db"]

# --- DEFINING COLLECTIONS ---
users_collection = db["users"]       # Stores balance, inventory, waifus, stats
groups_collection = db["groups"]     # Tracks group settings (welcome, claim status)
sudoers_collection = db["sudoers"]   # Stores admin IDs
chatbot_collection = db["chatbot"]   # Stores AI chat history per group/user
riddles_collection = db["riddles"]   # Stores active riddles and answers

# ===============================================
# --- CHATBOT FUNCTIONS (ZEXX Edition) ---
# ===============================================

def add_chat_to_db(word, response):
    """
    Naya word aur response database mein add karne ke liye.
    Bulk add aur single add dono isi se chalenge.
    $addToSet se duplicate responses nahi bante.
    """
    chatbot_collection.update_one(
        {"word": word.lower().strip()},
        {"$addToSet": {"responses": response.strip()}},
        upsert=True
    )

def get_chat_response(word):
    """
    User ke message ke liye database se responses ki list nikalta hai.
    """
    data = chatbot_collection.find_one({"word": word.lower().strip()})
    if data and "responses" in data:
        return data["responses"]
    return None

def remove_chat_word(word):
    """
    Database se kisi bhi word ka poora data saaf karne ke liye.
    """
    chatbot_collection.delete_one({"word": word.lower().strip()})

def toggle_chatbot_status(chat_id, status: bool):
    """
    Group mein chatbot on ya off karne ke liye settings save karta hai.
    """
    # Hum 'settings_' use kar rahe hain taaki words aur group IDs mix na hon
    chatbot_collection.update_one(
        {"chat_id": f"settings_{chat_id}"},
        {"$set": {"enabled": status}},
        upsert=True
    )

def is_chatbot_enabled(chat_id):
    """
    Check karta hai ki group mein bot ON hai ya OFF.
    """
    doc = chatbot_collection.find_one({"chat_id": f"settings_{chat_id}"})
    if doc:
        return doc.get("enabled", True)
    return True # By default ON rahega agar koi setting nahi milti

def get_chatbot_stats():
    """
    ZEXX ko batane ke liye ki database mein kitne words ho chuke hain.
    """
    # Sirf un documents ko count karega jinme 'word' key hai
    return chatbot_collection.count_documents({"word": {"$exists": True}})
