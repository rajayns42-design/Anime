# Copyright (c) 2025 Telegram:- @WTF_Phantom <DevixOP>
# Edited for Malik: ZEXX (Fixed Imports & Chatbot Integration)

import html
import re
import asyncio
import random
from datetime import datetime, timedelta
from telegram import Bot
from telegram.constants import ParseMode, ChatType
from telegram.error import TelegramError

# Database se zaroori collections import karna (Fixes ImportError)
from baka.database import (
    users_collection, 
    sudoers_collection, 
    groups_collection, 
    chatbot_collection,
    get_chat_response,
    is_chatbot_enabled
)
from baka.config import OWNER_ID, SUDO_IDS_STR, LOGGER_ID, BOT_NAME, AUTO_REVIVE_HOURS, AUTO_REVIVE_BONUS

SUDO_USERS = set()

def reload_sudoers():
    """Loads Sudo users from Env and DB."""
    SUDO_USERS.clear()
    SUDO_USERS.add(OWNER_ID)
    if SUDO_IDS_STR:
        for x in SUDO_IDS_STR.split(","):
            if x.strip().isdigit(): SUDO_USERS.add(int(x.strip()))
    for doc in sudoers_collection.find({}):
        SUDO_USERS.add(doc["user_id"])

reload_sudoers()

# --- 🌟 ULTIMATE LOGGER ---
async def log_to_channel(bot: Bot, event_type: str, details: dict):
    if LOGGER_ID == 0: return
    now = datetime.now().strftime("%I:%M %p | %d %b")
    
    headers = {
        "start": "🟢 <b>𝐁𝐎𝐓 𝐃𝐄𝐏𝐋𝐎𝐘𝐄𝐃</b>",
        "join": "🆕 <b>𝐍𝐄𝐖 𝐆𝐑𝐎𝐔𝐏</b>",
        "leave": "❌ <b>𝐋𝐄𝐅𝐓 𝐆𝐑𝐎𝐔𝐏</b>",
        "command": "⚠️ <b>𝐀𝐃𝐌𝐈𝐍 𝐋𝐎𝐆</b>",
        "transfer": "💸 <b>𝐓𝐑𝐀𝐍𝐒𝐀𝐂𝐓𝐈𝐎𝐍</b>"
    }
    header = headers.get(event_type, "🔔 <b>𝐋𝐎𝐆</b>")

    text = f"{header}\n\n📅 <b>Time:</b> <code>{now}</code>\n"
    if 'user' in details: text += f"👤 <b>Trigger:</b> {details['user']}\n"
    if 'chat' in details: text += f"📍 <b>Chat:</b> {html.escape(details['chat'])}\n"
    if 'action' in details: text += f"🎬 <b>Action:</b> {details['action']}\n"
    if 'link' in details and details['link'] != "No Link": text += f"🔗 <b>Link:</b> <a href='{details['link']}'>Click Here</a>\n"
    text += f"\n🤖 <i>{BOT_NAME} Systems</i>"

    try: await bot.send_message(chat_id=LOGGER_ID, text=text, parse_mode=ParseMode.HTML, disable_web_page_preview=True)
    except: pass

# --- HELPERS ---

def get_mention(user_data, custom_name=None):
    if hasattr(user_data, "id"): 
        name = custom_name or user_data.first_name
        return f"<a href='tg://user?id={user_data.id}'><b>{html.escape(name)}</b></a>"
    elif isinstance(user_data, dict):
        name = custom_name or user_data.get("name", "User")
        uid = user_data.get("user_id")
        return f"<a href='tg://user?id={uid}'><b>{html.escape(name)}</b></a>"
    return "Unknown"

def ensure_user_exists(tg_user):
    user_doc = users_collection.find_one({"user_id": tg_user.id})
    username = tg_user.username.lower() if tg_user.username else None
    
    if not user_doc:
        new_user = {
            "user_id": tg_user.id, 
            "name": tg_user.first_name, 
            "username": username, 
            "balance": 0,
            "status": "alive", 
            "registered_at": datetime.utcnow(), 
            "seen_groups": []
        }
        users_collection.insert_one(new_user)
        return new_user
    return user_doc

def track_group(chat, user):
    """Saves group and user interaction to DB."""
    if chat.type in [ChatType.GROUP, ChatType.SUPERGROUP]:
        if not groups_collection.find_one({"chat_id": chat.id}):
            groups_collection.insert_one({"chat_id": chat.id, "title": chat.title, "claimed": False})
        if user:
            users_collection.update_one(
                {"user_id": user.id}, 
                {"$addToSet": {"seen_groups": chat.id}}
            )

# --- SMART FONT STYLER ---
def stylize_text(text):
    font_map = {
        'A': '𝐀', 'B': '𝐁', 'C': '𝐂', 'D': '𝐃', 'E': '𝐄', 'F': '𝐅', 'G': '𝐆', 'H': '𝐇', 'I': '𝐈', 'J': '𝐉', 'K': '𝐊', 'L': '𝐋', 'M': '𝐌', 'N': '𝐍', 'O': '𝐎', 'P': '𝐏', 'Q': '𝐐', 'R': '𝐑', 'S': '𝐒', 'T': '𝐓', 'U': '𝐔', 'V': '𝐕', 'W': '𝐖', 'X': '𝐗', 'Y': '𝐘', 'Z': '𝐙',
        'a': 'ᴀ', 'b': 'ʙ', 'c': 'ᴄ', 'd': 'ᴅ', 'e': 'ᴇ', 'f': 'ꜰ', 'g': 'ɢ', 'h': 'ʜ', 'i': 'ɪ', 'j': 'ᴊ', 'k': 'ᴋ', 'l': 'ʟ', 'm': 'ᴍ', 'n': 'ɴ', 'o': 'ᴏ', 'p': 'ᴩ', 'q': 'q', 'r': 'ʀ', 's': 'ꜱ', 't': 'ᴛ', 'u': 'ᴜ', 'v': 'ᴠ', 'w': 'ᴡ', 'x': 'x', 'y': 'ʏ', 'z': 'ᴢ',
        '0': '𝟎', '1': '𝟏', '2': '𝟐', '3': '𝟑', '4': '𝟒', '5': '𝟓', '6': '𝟔', '7': '𝟕', '8': '𝟖', '9': '𝟗'
    }
    
    def apply_style(t):
        return "".join(font_map.get(c, c) for c in t)

    pattern = r"(@\w+|https?://\S+|`[^`]+`|/[a-zA-Z0-9_]+)"
    parts = re.split(pattern, text)
    
    result = []
    for part in parts:
        if re.match(pattern, part):
            result.append(part) 
        else:
            result.append(apply_style(part))
            
    return "".join(result)
