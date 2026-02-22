# Copyright (c) 2026 Telegram:- @WTF_Phantom <DevixOP>
# Updated Utils with Missing RPG & Economy Functions

import html
import re
import asyncio
from datetime import datetime, timedelta
from telegram import Bot
from telegram.constants import ParseMode, ChatType
from baka.database import users_collection, sudoers_collection, groups_collection
from baka.config import OWNER_ID, SUDO_IDS_STR, LOGGER_ID, BOT_NAME, AUTO_REVIVE_HOURS, AUTO_REVIVE_BONUS

SUDO_USERS = set()

def reload_sudoers():
    SUDO_USERS.clear()
    SUDO_USERS.add(OWNER_ID)
    if SUDO_IDS_STR:
        for x in SUDO_IDS_STR.split(","):
            if x.strip().isdigit(): SUDO_USERS.add(int(x.strip()))
    for doc in sudoers_collection.find({}):
        SUDO_USERS.add(doc["user_id"])

reload_sudoers()

# --- 🌟 ULTIMATE LOGGER ---
async def log_to_channel(bot: Bot, event_type: str, details: dict = None):
    if not LOGGER_ID or LOGGER_ID == 0: return
    if details is None: details = {}
    now = datetime.now().strftime("%I:%M %p | %d %b")
    
    headers = {
        "start": "🟢 <b>𝐁𝐎𝐓 𝐃𝐄𝐏𝐋𝐎𝐘𝐄𝐃</b>",
        "join": "🆕 <b>𝐍𝐄𝐖 𝐆𝐑𝐎𝐔𝐏</b>",
        "leave": "❌ <b>𝐋𝐄𝐅𝐓 𝐆𝐑𝐎𝐔𝐏</b>",
        "command": "⚠️ <b>𝐀𝐃𝐌𝐈𝐍 𝐋𝐎𝐆</b>",
        "transfer": "💸 <b>𝐓𝐑𝐀𝐍𝐒𝐀𝐂𝐓𝐈𝐎𝐍</b>"
    }
    header = headers.get(event_type, "🔔 <b>𝐋𝐎𝐆</b>")
    text = f"{header}\n\n📅 <b>𝐓𝐢𝐦𝐞:</b> <code>{now}</code>\n"
    if event_type == "start": text += f"🚀 <b>𝐒𝐭𝐚𝐭𝐮𝐬:</b> Online & All 21 Plugins Synced.\n"
    if 'user' in details: text += f"👤 <b>𝐓𝐫𝐢𝐠𝐠𝐞𝐫:</b> {details['user']}\n"
    if 'chat' in details: text += f"📍 <b>𝐂𝐡𝐚𝐭:</b> {html.escape(str(details['chat']))}\n"
    if 'action' in details: text += f"🎬 <b>𝐀𝐜𝐭𝐢𝐨𝐧:</b> {details['action']}\n"
    text += f"\n🤖 <i>{BOT_NAME} 𝐒𝐲𝐬𝐭𝐞𝐦𝐬</i>"
    try: await bot.send_message(chat_id=LOGGER_ID, text=text, parse_mode=ParseMode.HTML)
    except: pass

# --- 🛠️ ESSENTIAL HELPERS (CRITICAL FIX) ---

def format_money(amount): 
    """Fixes the ImportError in economy.py"""
    return f"${amount:,}"

def get_mention(user_data, custom_name=None):
    if hasattr(user_data, "id"): 
        name = custom_name or user_data.first_name
        return f"<a href='tg://user?id={user_data.id}'><b>{html.escape(name)}</b></a>"
    return "𝐔𝐧𝐤𝐧𝐨𝐰𝐧"

def ensure_user_exists(tg_user):
    user_doc = users_collection.find_one({"user_id": tg_user.id})
    if not user_doc:
        new_user = {
            "user_id": tg_user.id, "name": tg_user.first_name, 
            "balance": 0, "status": "alive", "registered_at": datetime.utcnow()
        }
        users_collection.insert_one(new_user)
        return new_user
    return user_doc

async def resolve_target(update, context, specific_arg=None):
    if update.message.reply_to_message:
        return ensure_user_exists(update.message.reply_to_message.from_user), None
    query = specific_arg or (context.args[0] if context.args else None)
    if query and query.isdigit():
        doc = users_collection.find_one({"user_id": int(query)})
        if doc: return doc, None
    return None, "No target found"

def track_group(chat, user):
    if chat.type in [ChatType.GROUP, ChatType.SUPERGROUP]:
        if not groups_collection.find_one({"chat_id": chat.id}):
            groups_collection.insert_one({"chat_id": chat.id, "title": chat.title})

def stylize_text(text):
    font_map = {'a': 'ᴀ', 'b': 'ʙ', 'c': 'ᴄ', 'd': 'ᴅ', 'e': 'ᴇ', 'f': 'ꜰ', 'g': 'ɢ', 'h': 'ʜ', 'i': 'ɪ', 'j': 'ᴊ', 'k': 'ᴋ', 'l': 'ʟ', 'm': 'ᴍ', 'n': 'ɴ', 'o': 'ᴏ', 'p': 'ᴩ', 'q': 'q', 'r': 'ʀ', 's': 'ꜱ', 't': 'ᴛ', 'u': 'ᴜ', 'v': 'ᴠ', 'w': 'ᴡ', 'x': 'x', 'y': 'ʏ', 'z': 'ᴢ'}
    return "".join(font_map.get(c.lower(), c) for c in text)
