import certifi
import random
from pymongo import MongoClient
from baka.config import MONGO_URI

# --- 🛰️ CONNECTION ---
client = MongoClient(MONGO_URI, tlsCAFile=certifi.where())
db = client["bakabot_db"]

# --- 📁 COLLECTIONS ---
users_collection = db["users"]
groups_collection = db["groups"]
sudoers_collection = db["sudoers"]
chatbot_collection = db["chatbot"]
vocab_collection = db["vocabulary"]
couple_collection = db["couple_history"]
mafia_collection = db["mafia"]
wordseek_collection = db["wordseek"]

# ===============================================
# 🏆 LEADERBOARD SYSTEMS
# ===============================================

def update_battle_win(user_id):
    """User ki battle win count badhane ke liye"""
    users_collection.update_one(
        {"user_id": user_id},
        {"$inc": {"battle_wins": 1}},
        upsert=True
    )

def get_battle_leaderboard():
    """Global Top 10 Battle Winners"""
    return users_collection.find({"battle_wins": {"$gt": 0}}).sort("battle_wins", -1).limit(10)

def get_couple_leaderboard(chat_id):
    """Group ke top couples ki list (New Add Kiya)"""
    return couple_collection.find({"chat_id": chat_id}).sort("date", -1).limit(10) [cite: 2026-02-22]

def get_mafia_leaderboard():
    """Top Mafia Teams ki ranking"""
    return mafia_collection.find().sort("points", -1).limit(10)

# ===============================================
# ❤️ COUPLE & USER DATA
# ===============================================

def save_daily_couple(chat_id, user1_id, user2_id):
    """Daily couple save karne ke liye"""
    from datetime import datetime
    today = datetime.now().strftime("%Y-%m-%d")
    couple_collection.update_one(
        {"chat_id": chat_id},
        {"$set": {"u1": user1_id, "u2": user2_id, "date": today}},
        upsert=True
    )

def ensure_user_exists(user):
    """User profile setup"""
    users_collection.update_one(
        {"user_id": user.id},
        {
            "$set": {"username": user.username, "name": user.first_name},
            "$setOnInsert": {"battle_wins": 0, "balance": 5000}
        },
        upsert=True
    )

# ===============================================
# 🧠 CHATBOT MEMORY (Life-Time Blocking)
# ===============================================

def save_used_word(user_id, word):
    vocab_collection.update_one(
        {"user_id": user_id},
        {"$addToSet": {"banned_words": word.lower()}},
        upsert=True
    )

def get_banned_words(user_id):
    data = vocab_collection.find_one({"user_id": user_id})
    return data["banned_words"] if data else []
