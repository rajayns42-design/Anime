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

# 🆕 MAFIA COLLECTION (ZEXX Edition - Isse data kabhi nahi udega)
mafia_collection = db["mafia"]       # Stores Team names, members, bank, and power

# ===============================================
# --- CHATBOT FUNCTIONS (ZEXX Edition) ---
# ===============================================

def add_chat_to_db(word, response):
    chatbot_collection.update_one(
        {"word": word.lower().strip()},
        {"$addToSet": {"responses": response.strip()}},
        upsert=True
    )

def get_chat_response(word):
    data = chatbot_collection.find_one({"word": word.lower().strip()})
    if data and "responses" in data:
        return data["responses"]
    return None

def remove_chat_word(word):
    chatbot_collection.delete_one({"word": word.lower().strip()})

def toggle_chatbot_status(chat_id, status: bool):
    chatbot_collection.update_one(
        {"chat_id": f"settings_{chat_id}"},
        {"$set": {"enabled": status}},
        upsert=True
    )

def is_chatbot_enabled(chat_id):
    doc = chatbot_collection.find_one({"chat_id": f"settings_{chat_id}"})
    if doc:
        return doc.get("enabled", True)
    return True

def get_chatbot_stats():
    return chatbot_collection.count_documents({"word": {"$exists": True}})
