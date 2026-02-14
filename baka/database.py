import random
import certifi
from pymongo import MongoClient
from datetime import datetime, timedelta
from baka.config import MONGO_URI # Ensure your config has MONGO_URI

# ===============================================
# DATABASE CONNECTION
# ===============================================

# SSL certificate verify karne ke liye certifi use kiya hai
RyanBaka = MongoClient(MONGO_URI, tlsCAFile=certifi.where())
db = RyanBaka["bakabot_db"]

# ===============================================
# COLLECTIONS
# ===============================================

users_collection = db["users"]
groups_collection = db["groups"]
sudoers_collection = db["sudoers"]
chatbot_collection = db["chatbot"]
riddles_collection = db["riddles"]
mafia_collection = db["mafia"]
wordseek_collection = db["wordseek"]

# ===============================================
# CHATBOT FUNCTIONS (Private & Group Support)
# ===============================================

def add_chat_to_db(word, response):
    """Database mein naya word aur reply add karne ke liye"""
    chatbot_collection.update_one(
        {"word": word.lower().strip()},
        {"$addToSet": {"responses": response.strip()}},
        upsert=True
    )

def get_chat_response(word):
    """Database se random response nikalne ke liye"""
    data = chatbot_collection.find_one({"word": word.lower().strip()})
    if data and "responses" in data:
        res = data["responses"]
        return random.choice(res) if isinstance(res, list) else res
    return None

def toggle_chatbot_status(chat_id, status: bool):
    """Group mein chatbot on ya off karne ke liye"""
    chatbot_collection.update_one(
        {"chat_id": f"settings_{chat_id}"},
        {"$set": {"enabled": status}},
        upsert=True
    )

def is_chatbot_enabled(chat_id):
    """Check karega ki chatbot enabled hai ya nahi"""
    doc = chatbot_collection.find_one({"chat_id": f"settings_{chat_id}"})
    if doc:
        return doc.get("enabled", True)
    return True

# ===============================================
# WORDSEEK FUNCTIONS
# ===============================================

def ws_start_game(chat_id, word):
    """Naya Wordseek game start karne ke liye"""
    wordseek_collection.update_one(
        {"chat_id": chat_id},
        {
            "$set": {
                "chat_id": chat_id,
                "active": True,
                "word": word.upper(),
                "board": [],
                "revealed_indices": [],
                "start_time": datetime.now()
            }
        },
        upsert=True
    )

def ws_get_game(chat_id):
    """Active game ka data nikalne ke liye"""
    return wordseek_collection.find_one({"chat_id": chat_id, "active": True})

def ws_update_board(chat_id, board, revealed_indices):
    """Board aur revealed indices ko update karne ke liye (Error Fix)"""
    wordseek_collection.update_one(
        {"chat_id": chat_id, "active": True},
        {
            "$set": {
                "board": board,
                "revealed_indices": revealed_indices
            }
        }
    )

def ws_end_game(chat_id):
    """Game khatam karne ke liye"""
    wordseek_collection.update_one({"chat_id": chat_id}, {"$set": {"active": False}})
