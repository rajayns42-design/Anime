# Copyright (c) 2026 Telegram:- @WTF_Phantom <DevixOP>
import certifi
from pymongo import MongoClient
from baka.config import MONGO_URI
from datetime import datetime

# --- 🛰️ CONNECTION ---
client = MongoClient(MONGO_URI, tlsCAFile=certifi.where())
db = client["bakabot_db"]

# --- 📁 ALL COLLECTIONS ---
users_collection = db["users"]
groups_collection = db["groups"]
sudoers_collection = db["sudoers"]
chatbot_collection = db["chatbot"]
vocab_collection = db["vocabulary"]
couple_collection = db["couple_history"]
mafia_collection = db["mafia"]
wordseek_collection = db["wordseek"]
riddles_collection = db["riddles"]
ws_wins_collection = db["wordseek_wins"]

# ===============================================
# 🧠 CHATBOT CORE
# ===============================================

def get_banned_words(user_id):
    data = vocab_collection.find_one({"user_id": user_id})
    return data.get("banned_words", []) if data else []

def save_used_word(user_id, word):
    vocab_collection.update_one(
        {"user_id": user_id}, 
        {"$addToSet": {"banned_words": word.lower().strip()}}, 
        upsert=True
    )

def is_chatbot_enabled(chat_id):
    doc = chatbot_collection.find_one({"chat_id": f"settings_{chat_id}"})
    return doc.get("enabled", True) if doc else True

# ===============================================
# 🏆 GAME & LEADERBOARD HELPERS
# ===============================================

def ws_start_game(chat_id, word):
    wordseek_collection.update_one(
        {"chat_id": chat_id}, 
        {"$set": {"word": word.upper(), "active": True, "board": []}}, 
        upsert=True
    )

def ws_get_game(chat_id):
    return wordseek_collection.find_one({"chat_id": chat_id})

def ws_add_win(chat_id, user_id, name):
    ws_wins_collection.update_one(
        {"user_id": user_id},
        {"$inc": {"wins": 1}, "$set": {"name": name}},
        upsert=True
    )

def get_top_rich():
    return users_collection.find().sort("balance", -1).limit(10)

def get_mafia_leaderboard():
    return mafia_collection.find().sort("points", -1).limit(10)

# ===============================================
# 🛠️ GENERAL HELPERS
# ===============================================

def ensure_user_exists(user):
    users_collection.update_one(
        {"user_id": user.id}, 
        {
            "$set": {"username": user.username, "name": user.first_name}, 
            "$setOnInsert": {"battle_wins": 0, "balance": 5000}
        }, 
        upsert=True
    )

def save_daily_couple(chat_id, user1_id, user2_id):
    today = datetime.now().strftime("%Y-%m-%d")
    couple_collection.update_one(
        {"chat_id": chat_id}, 
        {"$set": {"u1": user1_id, "u2": user2_id, "date": today}}, 
        upsert=True
    )
