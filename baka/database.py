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
# 🧠 CHATBOT CORE (Lifetime Memory)
# ===============================================

def get_banned_words(user_id):
    """Bole gaye saare purane words fetch karta hai [cite: 2026-02-24]"""
    data = vocab_collection.find_one({"user_id": user_id})
    return data.get("banned_words", []) if data else [] [cite: 2026-02-24]

def save_used_word(user_id, word):
    """Naye word ko lifetime ke liye ban (save) karta hai [cite: 2026-02-24]"""
    vocab_collection.update_one(
        {"user_id": user_id}, 
        {"$addToSet": {"banned_words": word.lower().strip()}}, 
        upsert=True
    ) [cite: 2026-02-24]

def is_chatbot_enabled(chat_id):
    """Check karta hai ki AI On hai ya Off [cite: 2026-02-24]"""
    doc = chatbot_collection.find_one({"chat_id": f"settings_{chat_id}"})
    return doc.get("enabled", True) if doc else True [cite: 2026-02-24]

# ===============================================
# 🏆 WORDSEEK CORE
# ===============================================

def ws_start_game(chat_id, word):
    """Naya wordseek game shuru karta hai [cite: 2026-02-24]"""
    wordseek_collection.update_one(
        {"chat_id": chat_id}, 
        {"$set": {"word": word.upper(), "active": True, "board": []}}, 
        upsert=True
    ) [cite: 2026-02-24]

def ws_get_game(chat_id):
    """Active game ka data nikalta hai [cite: 2026-02-24]"""
    return wordseek_collection.find_one({"chat_id": chat_id}) [cite: 2026-02-24]

def ws_add_win(chat_id, user_id, name):
    """Jeetne wale ka record save karta hai [cite: 2026-02-24]"""
    ws_wins_collection.update_one(
        {"user_id": user_id},
        {"$inc": {"wins": 1}, "$set": {"name": name}},
        upsert=True
    ) [cite: 2026-02-24]

# ===============================================
# 🛠️ GENERAL HELPERS
# ===============================================

def ensure_user_exists(user):
    """Naye user ko database mein register karta hai [cite: 2026-02-24]"""
    users_collection.update_one(
        {"user_id": user.id}, 
        {
            "$set": {"username": user.username, "name": user.first_name}, 
            "$setOnInsert": {"battle_wins": 0, "balance": 5000}
        }, 
        upsert=True
    ) [cite: 2026-02-24]

def save_daily_couple(chat_id, user1_id, user2_id):
    """Aaj ke din ka couple save karta hai [cite: 2026-02-24]"""
    today = datetime.now().strftime("%Y-%m-%d")
    couple_collection.update_one(
        {"chat_id": chat_id}, 
        {"$set": {"u1": user1_id, "u2": user2_id, "date": today}}, 
        upsert=True
    ) [cite: 2026-02-24]
