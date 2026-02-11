from pymongo import MongoClient
import certifi
from datetime import datetime, timedelta
from baka.config import MONGO_URI

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
# CHATBOT FUNCTIONS
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

# ===============================================
# WORDSEEK DATABASE FUNCTIONS (Permanent Edition)
# ===============================================

# 🔹 Start New Group Game
def ws_start_game(chat_id, word):
    wordseek_collection.update_one(
        {"chat_id": chat_id},
        {
            "$set": {
                "chat_id": chat_id,
                "active": True,
                "word": word.upper(),
                "board": [],
                "revealed_indices": [], # Hint track karne ke liye
                "start_time": datetime.now()
            }
        },
        upsert=True
    )

# 🔹 Get Active Game
def ws_get_game(chat_id):
    return wordseek_collection.find_one(
        {"chat_id": chat_id, "active": True}
    )

# 🔹 Update Board
def ws_update_board(chat_id, board):
    wordseek_collection.update_one(
        {"chat_id": chat_id},
        {"$set": {"board": board}}
    )

# 🔹 End Game
def ws_end_game(chat_id):
    wordseek_collection.update_one(
        {"chat_id": chat_id},
        {"$set": {"active": False}}
    )

# 🔹 Update Hint Indices
def ws_update_hints(chat_id, revealed_indices):
    wordseek_collection.update_one(
        {"chat_id": chat_id},
        {"$set": {"revealed_indices": revealed_indices}}
    )

# 🔹 Add Win to Leaderboard (With Name Storage)
def ws_add_win(chat_id, user_id, first_name):
    wordseek_collection.update_one(
        {"chat_id": chat_id},
        {
            "$inc": {f"leaderboard.{user_id}.wins": 1},
            "$set": {f"leaderboard.{user_id}.name": first_name}
        },
        upsert=True
    )

# 🔹 Get Leaderboard Data
def ws_get_leaderboard(chat_id):
    data = wordseek_collection.find_one({"chat_id": chat_id})
    if data and "leaderboard" in data:
        return data["leaderboard"]
    return {}

# 🔹 Weekly Hint Limit Logic (2 per week)
def can_user_get_hint(chat_id, user_id):
    doc = wordseek_collection.find_one({"chat_id": chat_id})
    if not doc:
        return True, None
    
    # User ki hint history nikalo
    hint_users = doc.get("hint_users", {})
    history = hint_users.get(str(user_id), [])
    
    now = datetime.now()
    one_week_ago = now - timedelta(weeks=1)
    
    # Sirf pichle 7 din ke timestamps rakho
    active_hints = [h for h in history if h > one_week_ago]
    
    if len(active_hints) >= 2:
        # Agar 2 hints ho chuke hain, toh sabse purane hint ka time return karo
        return False, active_hints[0]
        
    # Naya hint time add karo
    active_hints.append(now)
    wordseek_collection.update_one(
        {"chat_id": chat_id},
        {"$set": {f"hint_users.{user_id}": active_hints}},
        upsert=True
    )
    return True, None
