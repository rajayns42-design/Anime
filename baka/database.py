from pymongo import MongoClient
import certifi
from baka.config import MONGO_URI

# ===============================================
# DATABASE CONNECTION
# ===============================================

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

# 🆕 WORDSEEK COLLECTION (Permanent Game Storage)
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
                "word": word,
                "board": [],
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


# 🔹 Add Win to Leaderboard
def ws_add_win(chat_id, user_id):
    wordseek_collection.update_one(
        {"chat_id": chat_id},
        {"$inc": {f"leaderboard.{user_id}": 1}},
        upsert=True
    )


# 🔹 Get Leaderboard
def ws_get_leaderboard(chat_id):
    data = wordseek_collection.find_one({"chat_id": chat_id})
    if data and "leaderboard" in data:
        return data["leaderboard"]
    return {}