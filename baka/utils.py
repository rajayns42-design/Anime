# Copyright (c) 2026 Telegram:- @WTF_Phantom <DevixOP>
# Full Fixed Utils for ZEXX - No more ImportErrors

import html
import re
from datetime import datetime, timedelta
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup
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
        "start": "🟢 𝐁𝐎𝐓 𝐃𝐄𝐏𝐋𝐎𝐘𝐄𝐃",
        "join": "🆕 𝐍𝐄𝐖 𝐆𝐑𝐎𝐔𝐏",
        "leave": "❌ 𝐋𝐄𝐅𝐓 𝐆𝐑𝐎𝐔𝐏",
        "command": "⚠️ 𝐀𝐃𝐌𝐈𝐍 𝐋𝐎𝐆",
        "transfer": "💸 𝐓𝐑𝐀𝐍𝐒𝐀𝐂𝐓𝐈𝐎𝐍"
    }
    header = headers.get(event_type, "🔔 𝐋𝐎𝐆")
    text = f"<b>{header}</b>\n\n📅 <b>𝐓𝐢𝐦𝐞:</b> <code>{now}</code>\n"
    if event_type == "start": text += f"🚀 <b>𝐒𝐭𝐚𝐭𝐮𝐬:</b> Online & Plugins Synced.\n"
    if 'user' in details: text += f"👤 <b>𝐓𝐫𝐢𝐠𝐠𝐞𝐫:</b> {details['user']}\n"
    if 'chat' in details: text += f"📍 <b>𝐂𝐡𝐚𝐭:</b> {html.escape(str(details['chat']))}\n"
    text += f"\n🤖 <i>{BOT_NAME} Systems</i>"
    try: await bot.send_message(chat_id=LOGGER_ID, text=text, parse_mode=ParseMode.HTML)
    except: pass

# --- 🛠️ CORE HELPERS (FIXED) ---

def format_money(amount): 
    return f"${amount:,}"

def format_time(timedelta_obj):
    total_seconds = int(timedelta_obj.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, _ = divmod(remainder, 60)
    return f"{hours}h {minutes}m"

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
            "balance": 0, "status": "alive", "protection_expiry": datetime.utcnow(),
            "registered_at": datetime.utcnow()
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

def get_active_protection(user_data):
    now = datetime.utcnow()
    self_expiry = user_data.get("protection_expiry")
    if self_expiry and self_expiry > now: return self_expiry
    return None

def track_group(chat, user):
    if chat.type in [ChatType.GROUP, ChatType.SUPERGROUP]:
        if not groups_collection.find_one({"chat_id": chat.id}):
            groups_collection.insert_one({"chat_id": chat.id, "title": chat.title})

def stylize_text(text):
    font_map = {'a': 'ᴀ', 'b': 'ʙ', 'c': 'ᴄ', 'd': 'ᴅ', 'e': 'ᴇ', 'f': 'ꜰ', 'g': 'ɢ', 'h': 'ʜ', 'i': 'ɪ', 'j': 'ᴊ', 'k': 'ᴋ', 'l': 'ʟ', 'm': 'ᴍ', 'n': 'ɴ', 'o': 'ᴏ', 'p': 'ᴩ', 'q': 'q', 'r': 'ʀ', 's': 'ꜱ', 't': 'ᴛ', 'u': 'ᴜ', 'v': 'ᴠ', 'w': 'ᴡ', 'x': 'x', 'y': 'ʏ', 'z': 'ᴢ'}
    return "".join(font_map.get(c.lower(), c) for c in text)

# --- 🆘 HELP MENU & BUTTONS ---

def get_help_menu_keyboard():
    # Adding HELP button as requested
    keyboard = [
        [InlineKeyboardButton("❍ BAL ❍", callback_data="cb_bal"), InlineKeyboardButton("❍ CHECK ❍", callback_data="cb_check"), InlineKeyboardButton("❍ GUESS ❍", callback_data="cb_guess")],
        [InlineKeyboardButton("❍ HAREM ❍", callback_data="cb_harem"), InlineKeyboardButton("❍ CHAT ❍", callback_data="cb_chat"), InlineKeyboardButton("❍ FAV ❍", callback_data="cb_fav")],
        [InlineKeyboardButton("❍ SHOP ❍", callback_data="cb_shop"), InlineKeyboardButton("❍ SPAWN ❍", callback_data="cb_spawn"), InlineKeyboardButton("❍ TAG ❍", callback_data="cb_tag")],
        [InlineKeyboardButton("❍ TRADE ❍", callback_data="cb_trade"), InlineKeyboardButton("❍ UPLOAD ❍", callback_data="cb_upload"), InlineKeyboardButton("❍ BROAD ❍", callback_data="cb_broad")],
        [InlineKeyboardButton("🆘 HELP", callback_data="cb_help_guide")],
        [InlineKeyboardButton("⬅️ Back", callback_data="start_return")]
    ]
    return InlineKeyboardMarkup(keyboard)
