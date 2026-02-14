# Copyright (c) 2026 Telegram:- @WTF_Phantom <DevixOP>
# Fixed version: Added missing functions (format_money, resolve_target, etc.)

import html
import re
import asyncio
from datetime import datetime, timedelta
from telegram import Bot
from telegram.constants import ParseMode, ChatType
from telegram.error import TelegramError

# Database imports
from baka.database import (
    users_collection, 
    sudoers_collection, 
    groups_collection, 
    chatbot_collection
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
        "join": "🆕 <b>𝐍𝐖𝐄 𝐆𝐑𝐎𝐔𝐏</b>",
        "leave": "❌ <b>𝐋𝐄𝐅𝐓 𝐆𝐑𝐎𝐔𝐏</b>",
        "command": "⚠️ <b>𝐀𝐃𝐌𝐈𝐍 𝐋𝐎𝐆</b>",
        "transfer": "💸 <b>𝐓𝐑𝐀𝐍𝐒𝐀𝐂𝐓𝐈𝐎𝐍</b>"
    }
    header = headers.get(event_type, "🔔 <b>LOG</b>")
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
            "user_id": tg_user.id, "name": tg_user.first_name, "username": username,
            "balance": 0, "status": "alive", "registered_at": datetime.utcnow(), "seen_groups": []
        }
        users_collection.insert_one(new_user)
        return new_user
    return user_doc

def track_group(chat, user):
    if chat.type in [ChatType.GROUP, ChatType.SUPERGROUP]:
        if not groups_collection.find_one({"chat_id": chat.id}):
            groups_collection.insert_one({"chat_id": chat.id, "title": chat.title, "claimed": False})
        if user:
            users_collection.update_one({"user_id": user.id}, {"$addToSet": {"seen_groups": chat.id}})

# --- MISSING FUNCTIONS (Added back for economy.py) ---

def format_money(amount):
    """Formats amount like $1,000"""
    return f"${amount:,}"

def format_time(timedelta_obj):
    """Formats time for display"""
    total_seconds = int(timedelta_obj.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, _ = divmod(remainder, 60)
    return f"{hours}h {minutes}m"

async def resolve_target(update, context, specific_arg=None):
    """Resolves user from reply or mention/ID"""
    if update.message.reply_to_message:
        return ensure_user_exists(update.message.reply_to_message.from_user), None
    query = specific_arg if specific_arg else (context.args[0] if context.args else None)
    if query:
        if query.isdigit():
            doc = users_collection.find_one({"user_id": int(query)})
            if doc: return doc, None
            return None, f"❌ ID <code>{query}</code> not found."
        if query.startswith("@"):
            clean = query.strip("@").lower()
            doc = users_collection.find_one({"username": clean})
            if doc: return doc, None
            return None, f"❌ <code>@{clean}</code> not found."
    return None, "No target"

def stylize_text(text):
    """Normal text style as requested"""
    return text
