import certifi
import random
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
# 🏆 WORDSEEK CORE (Fixes ImportError)
# ===============================================

def ws_start_game(chat_id, word):
    # active flag add kiya gaya hai taaki plugin check kar sake
    wordseek_collection.update_one(
        {"chat_id": chat_id}, 
        {"$set": {"word": word.upper(), "active": True, "board": []}}, 
        upsert=True
    )

def ws_get_game(chat_id):
    return wordseek_collection.find_one({"chat_id": chat_id})

def ws_update_board(chat_id, board):
    # Board state save karne ke liye
    wordseek_collection.update_one(
        {"chat_id": chat_id}, 
        {"$set": {"board": board}}
    )

def ws_end_game(chat_id):
    wordseek_collection.update_one(
        {"chat_id": chat_id}, 
        {"$set": {"active": False}}
    )

def ws_add_win(chat_id, user_id, name):
    # update_ws_win ko rename kiya gaya hai plugin ki demand par
    ws_wins_collection.update_one(
        {"user_id": user_id},
        {"$inc": {"wins": 1}, "$set": {"name": name}},
        upsert=True
    )

def ws_get_leaderboard(chat_id):
    # Dictionary format return karta hai jaisa wordseek.py ko chahiye
    winners = ws_wins_collection.find().sort("wins", -1).limit(10)
    return {str(w['user_id']): {"name": w['name'], "wins": w['wins']} for w in winners}

# ===============================================
# 🏆 OTHER LEADERBOARDS
# ===============================================

def update_mafia_stats(team_name, points):
    mafia_collection.update_one(
        {"team_name": team_name}, 
        {"$inc": {"points": points}}, 
        upsert=True
    )

def get_mafia_leaderboard():
    return mafia_collection.find().sort("points", -1).limit(10)

def update_battle_win(user_id):
    users_collection.update_one(
        {"user_id": user_id}, 
        {"$inc": {"battle_wins": 1}}, 
        upsert=True
    )

def get_battle_leaderboard():
    return users_collection.find({"battle_wins": {"$gt": 0}}).sort("battle_wins", -1).limit(10)

# ===============================================
# 🧠 CORE FUNCTIONS
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

def toggle_chatbot_status(chat_id, status: bool):
    chatbot_collection.update_one(
        {"chat_id": f"settings_{chat_id}"}, 
        {"$set": {"enabled": status}}, 
        upsert=True
    )

def is_chatbot_enabled(chat_id):
    doc = chatbot_collection.find_one({"chat_id": f"settings_{chat_id}"})
    return doc.get("enabled", True) if doc else True

def save_daily_couple(chat_id, user1_id, user2_id):
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
