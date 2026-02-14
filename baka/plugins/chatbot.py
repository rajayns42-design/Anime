# Copyright (c) 2026 Telegram:- @WTF_Phantom <DevixOP>
# Fixed version for Private & Group functionality

import random
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode, ChatType
from baka.database import chatbot_collection, add_chat_to_db, get_chat_response

# =====================================
# ⚙️ 𝐂𝐎𝐍𝐅𝐈𝐆𝐔𝐑𝐀𝐓𝐈𝐎𝐍
# =====================================
OWNER_ID = 8321028072

async def is_admin_or_owner(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id == OWNER_ID: return True
    if update.effective_chat.type == ChatType.PRIVATE: return True
    try:
        member = await context.bot.get_chat_member(update.effective_chat.id, user_id)
        return member.status in ["creator", "administrator"]
    except:
        return False

# =====================================
# 🛠️ 𝐎𝐖𝐍𝐄𝐑 𝐂𝐎𝐌𝐌𝐀𝐍𝐃𝐒
# =====================================

async def add_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        return await update.message.reply_text("<b>❌ only owner baby 💀!</b>", parse_mode=ParseMode.HTML)
    try:
        # Args parse karne ka sahi tareeka
        args = update.message.text.split(None, 1)[1]
        if "|" not in args: raise ValueError
        word, response = args.split("|", 1)
        add_chat_to_db(word.strip().lower(), response.strip())
        await update.message.reply_text(f"<b>✅ 『 SUCCESS 』\n\n🔹 WORD:</b> <code>{word.strip()}</code>\n<b>🔸 REPLY:</b> <code>{response.strip()}</code>", parse_mode=ParseMode.HTML)
    except (ValueError, IndexError):
        await update.message.reply_text("<b>📌 USAGE:</b> <code>/addchat hi | hello {name}</code>", parse_mode=ParseMode.HTML)

# =====================================
# ⚙️ 𝐓𝐎𝐆𝐆𝐋𝐄 & 𝐌𝐄𝐒𝐒𝐀𝐆𝐄 𝐇𝐀𝐍𝐃𝐋𝐄𝐑
# =====================================

async def chatbot_toggle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin_or_owner(update, context):
        return await update.message.reply_text("<b>❌ Admins ya Owner only baby!</b>", parse_mode=ParseMode.HTML)
    
    if not context.args: 
        return await update.message.reply_text("<b>📌 USAGE:</b> <code>/chatbot on/off</code>", parse_mode=ParseMode.HTML)
    
    chat_id = update.effective_chat.id
    action = context.args[0].lower()
    
    if action == "on":
        chatbot_collection.update_one({"chat_id": f"settings_{chat_id}"}, {"$set": {"enabled": True}}, upsert=True)
        await update.message.reply_text("<b>✅ 『 CHATBOT ON 』\n\n🤖 Ab ayega maja baby 😉.</b>", parse_mode=ParseMode.HTML)
    elif action == "off":
        chatbot_collection.update_one({"chat_id": f"settings_{chat_id}"}, {"$set": {"enabled": False}}, upsert=True)
        await update.message.reply_text("<b>📴 『 CHATBOT OFF 』\n\n🔇 baby off kr diye mujhe 🥺.</b>", parse_mode=ParseMode.HTML)

async def ai_message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    # Basic Checks
    if not msg or not msg.text or msg.text.startswith("/"): 
        return

    chat = update.effective_chat
    text = msg.text.lower().strip()
    user_name = msg.from_user.first_name

    # 1. Chatbot Status Check (Groups ke liye)
    if chat.type != ChatType.PRIVATE:
        doc = chatbot_collection.find_one({"chat_id": f"settings_{chat.id}"})
        # Agar doc nahi hai toh default ON rakhein (True)
        is_enabled = doc.get("enabled", True) if doc else True
        if not is_enabled:
            return

    # 2. Database Response Fetching
    responses = get_chat_response(text)
    
    if responses:
        # Agar responses list hai toh random choice, warna direct string
        reply = random.choice(responses) if isinstance(responses, list) else responses
        
        # Name placeholder replace karein
        if "{name}" in reply:
            reply = reply.replace("{name}", f"<b>{user_name}</b>")
        
        await msg.reply_text(reply, parse_mode=ParseMode.HTML)
