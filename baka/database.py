import certifi
import random
from pymongo import MongoClient
from baka.config import MONGO_URI

# --- 🛰️ CONNECTION ---
client = MongoClient(MONGO_URI, tlsCAFile=certifi.where())
db = client["bakabot_db"]

# --- 📁 ALL COLLECTIONS (Sync with all plugins) ---
users_collection = db["users"]
groups_collection = db["groups"]
sudoers_collection = db["sudoers"]
chatbot_collection = db["chatbot"]
vocab_collection = db["vocabulary"]
couple_collection = db["couple_history"]
mafia_collection = db["mafia"]
wordseek_collection = db["wordseek"]
riddles_collection = db["riddles"]  # Fixed ImportError for riddle.py

# --- 🧠 LIFE-TIME MEMORY VARIABLE ---
LIFE_WORDS = {} 

def load_life_words():
    """Startup par database se words load karne ke liye"""
    global LIFE_WORDS
    try:
        cursor = vocab_collection.find()
        for doc in cursor:
            LIFE_WORDS[doc["user_id"]] = set(doc.get("banned_words", []))
    except Exception as e:
        print(f"Error loading memory: {e}")

def save_used_word(user_id, word):
    """Variable aur Database dono update karega"""
    word = word.lower().strip()
    if user_id not in LIFE_WORDS:
        LIFE_WORDS[user_id] = set()
    
    if word not in LIFE_WORDS[user_id]:
        LIFE_WORDS[user_id].add(word)
        vocab_collection.update_one(
            {"user_id": user_id},
            {"$addToSet": {"banned_words": word}},
            upsert=True
        )

# ===============================================
# 🏆 LEADERBOARD SYSTEMS
# ===============================================

def update_battle_win(user_id):
    users_collection.update_one(
        {"user_id": user_id},
        {"$inc": {"battle_wins": 1}},
        upsert=True
    )

def get_battle_leaderboard():
    return users_collection.find({"battle_wins": {"$gt": 0}}).sort("battle_wins", -1).limit(10)

def get_couple_leaderboard(chat_id):
    """Fixes the SyntaxError from logs"""
    return couple_collection.find({"chat_id": chat_id}).sort("date", -1).limit(10)

def get_mafia_leaderboard():
    return mafia_collection.find().sort("points", -1).limit(10)

# ===============================================
# ❤️ COUPLE & USER DATA
# ===============================================

def save_daily_couple(chat_id, user1_id, user2_id):
    from datetime import datetime
    today = datetime.now().strftime("%Y-%m-%d")
    couple_collection.update_one(
        {"chat_id": chat_id},
        {"$set": {"u1": user1_id, "u2": user2_id, "date": today}},
        upsert=True
    )

def ensure_user_exists(user):
    users_collection.update_one(
        {"user_id": user.id},
        {
            "$set": {"username": user.username, "name": user.first_name},
            "$setOnInsert": {"battle_wins": 0, "balance": 5000}
        },
        upsert=True
    )
