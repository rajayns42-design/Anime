# Copyright (c) 2026 Telegram:- @WTF_Phantom <DevixOP>
# Edited for Malik: ZEXX (Fast Database Version)

import random
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode, ChatType
from baka.database import chatbot_collection, add_chat_to_db, get_chat_response
from baka.config import OWNER_ID  # Ensure OWNER_ID is imported from config or set below

# =====================================
# ⚙️ 𝐂𝐎𝐍𝐅𝐈𝐆𝐔𝐑𝐀𝐓𝐈𝐎𝐍
# =====================================
# Malik: ZEXX
OWNER_ID = 8211189367  # <--- Apni ID yahan confirm kar lein

async def is_admin_or_owner(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id == OWNER_ID: return True
    if update.effective_chat.type == ChatType.PRIVATE: return True
    member = await context.bot.get_chat_member(update.effective_chat.id, user_id)
    return member.status in ["creator", "administrator"]

# =====================================
# 🛠️ 𝐎𝐖𝐍𝐄𝐑 𝐂𝐎𝐌𝐌𝐀𝐍𝐃𝐒 (𝐎𝐍𝐋𝐘 𝐙𝐄𝐗𝐗)
# =====================================

async def add_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        return await update.message.reply_text("<b>❌ ye only owner (ZEXX) ke liye hai baby 💀!</b>", parse_mode=ParseMode.HTML)

    try:
        args = " ".join(context.args)
        if "|" not in args:
            raise ValueError
        word, response = args.split("|", 1)
        add_chat_to_db(word.strip().lower(), response.strip())
        await update.message.reply_text(
            f"<b>✅ 『 𝐒𝐔𝐂𝐂𝐄𝐒𝐒 』\n\n🔹 𝐖𝐎𝐑𝐃:</b> <code>{word.strip()}</code>\n"
            f"<b>🔸 𝐑𝐄𝐏𝐋𝐘:</b> <code>{response.strip()}</code>", 
            parse_mode=ParseMode.HTML
        )
    except ValueError:
        await update.message.reply_text("<b>📌 𝐔𝐒𝐀𝐆𝐄:</b> <code>/addchat hi | hello {name}</code>", parse_mode=ParseMode.HTML)

async def bulk_add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        return await update.message.reply_text("<b>❌ 𝐍𝐎 𝐀𝐂𝐂𝐄𝐒𝐒! Only Malik ZEXX can use this.</b>", parse_mode=ParseMode.HTML)

    raw_data = " ".join(context.args)
    if not raw_data:
        return await update.message.reply_text("<b>📌 𝐔𝐒𝐀𝐆𝐄:</b> <code>/bulkadd hi=hello,bye=tata</code>", parse_mode=ParseMode.HTML)

    pairs = raw_data.split(",")
    count = 0
    for pair in pairs:
        if "=" in pair:
            w, r = pair.split("=", 1)
            add_chat_to_db(w.strip().lower(), r.strip())
            count += 1
    await update.message.reply_text(
        f"<b>✅ 『 𝐁𝐔𝐋𝐊 𝐀𝐃𝐃𝐄𝐃 』\n\n✨ Malik ZEXX, <code>{count}</code> naye replies add ho gaye done baby 💗!</b>", 
        parse_mode=ParseMode.HTML
    )

# --- Empty function to prevent menu errors ---
async def chatbot_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Placeholder to fix AttributeError in logs"""
    await update.message.reply_text("<b>🤖 Chatbot Settings:</b>\nUse <code>/chatbot on/off</code> to toggle.", parse_mode=ParseMode.HTML)

# =====================================
# ⚙️ 𝐓𝐎𝐆𝐆𝐋𝐄 (𝐎𝐍/𝐎𝐅𝐅) - 𝐀𝐃𝐌𝐈𝐍𝐒 & 𝐎𝐖𝐍𝐄𝐑
# =====================================

async def chatbot_toggle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin_or_owner(update, context):
        return await update.message.reply_text("<b>❌ Admins ya Owner (ZEXX) only baby!</b>", parse_mode=ParseMode.HTML)

    if not context.args: 
        return await update.message.reply_text("<b>📌 𝐔𝐒𝐀𝐆𝐄:</b> <code>/chatbot on/off</code>", parse_mode=ParseMode.HTML)

    chat = update.effective_chat
    action = context.args[0].lower()

    if action == "on":
        chatbot_collection.update_one({"chat_id": f"settings_{chat.id}"}, {"$set": {"enabled": True}}, upsert=True)
        await update.message.reply_text("<b>✅ 『 𝐂𝐇𝐀𝐓𝐁𝐎𝐓 𝐎𝐍 』\n\n🤖 Ab ayega maja baby 😉.</b>", parse_mode=ParseMode.HTML)
    elif action == "off":
        chatbot_collection.update_one({"chat_id": f"settings_{chat.id}"}, {"$set": {"enabled": False}}, upsert=True)
        await update.message.reply_text("<b>📴 『 𝐂𝐇𝐀𝐓𝐁𝐎𝐓 𝐎𝐅𝐅 』\n\n🔇 baby off kr diye mujhe 🥺.</b>", parse_mode=ParseMode.HTML)

# =====================================
# 🤖 𝐌𝐄𝐒𝐒𝐀𝐆𝐄 𝐇𝐀𝐍𝐃𝐋𝐄𝐑 (𝐃𝐀𝐓𝐀𝐁𝐀𝐒𝐄 𝐎𝐍𝐋𝐘)
# =====================================

async def ai_message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    if not msg or not msg.text or msg.text.startswith("/"): return

    chat = update.effective_chat
    text = msg.text.lower().strip()
    user_name = msg.from_user.first_name

    # --- 1. Identity Check (Branding for ZEXX) ---
    if any(x in text for x in ["owner", "malik", "admin", "creator"]):
        return await msg.reply_text(f"Mere Malik <b>『 𝐙𝐄𝐗𝐗 』</b> hain!", parse_mode=ParseMode.HTML)

    # --- 2. Group Status Check ---
    if chat.type != ChatType.PRIVATE:
        doc = chatbot_collection.find_one({"chat_id": f"settings_{chat.id}"}, {"enabled": 1})
        if doc and not doc.get("enabled", True): return

    # --- 3. Database Response (Instant) ---
    responses = get_chat_response(text)
    if responses:
        reply = random.choice(responses)
        if "{name}" in reply: 
            reply = reply.replace("{name}", f"<b>{user_name}</b>")
        await msg.reply_text(reply, parse_mode=ParseMode.HTML)
