import certifi
import random
from pymongo import MongoClient
from baka.config import MONGO_URI

# --- 🛰️ CONNECTION ---
RyanBaka = MongoClient(MONGO_URI, tlsCAFile=certifi.where())
db = RyanBaka["bakabot_db"]

# --- 📁 COLLECTIONS ---
users_collection = db["users"]
couple_collection = db["couple_history"]
battle_stats = db["battle_records"]
mafia_collection = db["mafia"]
chatbot_collection = db["chatbot"]
vocab_collection = db["vocabulary"]

# ===============================================
# 🔫 MAFIA LEADERBOARD
# ===============================================

def update_mafia_stats(team_name, points):
    """Mafia team ke points update karne ke liye"""
    mafia_collection.update_one(
        {"team_name": team_name},
        {"$inc": {"points": points}},
        upsert=True
    )

def get_mafia_leaderboard():
    """Top 10 Mafia Teams ki list"""
    return mafia_collection.find().sort("points", -1).limit(10)

# ===============================================
# 🏆 BATTLE LEADERBOARD SYSTEM
# ===============================================

def update_battle_win(user_id):
    """User ki battle win count badhane ke liye"""
    users_collection.update_one(
        {"user_id": user_id},
        {"$inc": {"battle_wins": 1}},
        upsert=True
    )

def get_battle_leaderboard():
    """Top 10 battle winners ki list"""
    return users_collection.find().sort("battle_wins", -1).limit(10)

# ===============================================
# ❤️ COUPLE TRACKER
# ===============================================

def save_daily_couple(chat_id, user1_id, user2_id):
    """Daily couple save karne ke liye"""
    couple_collection.update_one(
        {"chat_id": chat_id},
        {"$set": {"u1": user1_id, "u2": user2_id, "date": "2026-02-22"}},
        upsert=True
    )

# ===============================================
# 🧠 CHATBOT MEMORY (Life-Time Blocking)
# ===============================================

def save_used_word(user_id, word):
    """Jo word bot ne bola usse permanent block list mein daalne ke liye"""
    vocab_collection.update_one(
        {"user_id": user_id},
        {"$addToSet": {"banned_words": word.lower()}},
        upsert=True
    )

def get_banned_words(user_id):
    """Sare purane bole gaye words nikalne ke liye"""
    data = vocab_collection.find_one({"user_id": user_id})
    return data["banned_words"] if data else []

# ===============================================
# 🛠️ CORE USER DATA
# ===============================================

def ensure_user_exists(user):
    """User register karne ke liye"""
    users_collection.update_one(
        {"user_id": user.id},
        {
            "$set": {"username": user.username, "name": user.first_name},
            "$setOnInsert": {"battle_wins": 0, "balance": 5000}
        },
        upsert=True
    )
