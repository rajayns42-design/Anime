# Copyright (c) 2026 Telegram:- @WTF_Phantom <DevixOP>
# Edited for Malik: ZEXX (Fast Database Version)

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
    member = await context.bot.get_chat_member(update.effective_chat.id, user_id)
    return member.status in ["creator", "administrator"]

# =====================================
# 🛠️ 𝐎𝐖𝐍𝐄𝐑 𝐂𝐎𝐌𝐌𝐀𝐍𝐃𝐒
# =====================================

async def add_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        return await update.message.reply_text("<b>❌ only owner baby 💀!</b>", parse_mode=ParseMode.HTML)
    try:
        args = " ".join(context.args)
        if "|" not in args: raise ValueError
        word, response = args.split("|", 1)
        add_chat_to_db(word.strip().lower(), response.strip())
        await update.message.reply_text(f"<b>✅ 『 SUCCESS 』\n\n🔹 WORD:</b> <code>{word.strip()}</code>\n<b>🔸 REPLY:</b> <code>{response.strip()}</code>", parse_mode=ParseMode.HTML)
    except ValueError:
        await update.message.reply_text("<b>📌 USAGE:</b> <code>/addchat hi | hello {name}</code>", parse_mode=ParseMode.HTML)

async def bulk_add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        return await update.message.reply_text("<b>❌ NO ACCESS! Only owner can use this.</b>", parse_mode=ParseMode.HTML)
    raw_data = " ".join(context.args)
    if not raw_data: return await update.message.reply_text("<b>📌 USAGE:</b> <code>/bulkadd hi=hello,bye=tata</code>", parse_mode=ParseMode.HTML)
    pairs = raw_data.split(",")
    count = 0
    for pair in pairs:
        if "=" in pair:
            w, r = pair.split("=", 1)
            add_chat_to_db(w.strip().lower(), r.strip()); count += 1
    await update.message.reply_text(f"<b>✅ 『 BULK ADDED 』\n\n✨ Hari, <code>{count}</code> naye replies add ho gaye done baby 💗!</b>", parse_mode=ParseMode.HTML)

# =====================================
# 🚀 𝐇𝐄𝐑𝐎𝐊𝐔 𝐂𝐑𝐀𝐒𝐇 𝐅𝐈𝐗𝐄𝐒 (Missing Handlers)
# =====================================

async def chatbot_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Fixes AttributeError in Ryan.py line 170"""
    await update.message.reply_text("<b>🤖 Chatbot Settings:</b>\nUse <code>/chatbot on/off</code> to toggle.", parse_mode=ParseMode.HTML)

async def ask_ai(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Fixes AttributeError in Ryan.py line 171"""
    await update.message.reply_text("<b>❌ AI system disabled for speed!</b>\nAi baby.", parse_mode=ParseMode.HTML)

async def chatbot_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Fixes AttributeError in Ryan.py line 172"""
    query = update.callback_query
    await query.answer("AI features are currently restricted for performance.")

# =====================================
# ⚙️ 𝐓𝐎𝐆𝐆𝐋𝐄 & 𝐌𝐄𝐒𝐒𝐀𝐆𝐄 𝐇𝐀𝐍𝐃𝐋𝐄𝐑
# =====================================

async def chatbot_toggle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin_or_owner(update, context):
        return await update.message.reply_text("<b>❌ Admins ya Owner (ZEXX) only baby!</b>", parse_mode=ParseMode.HTML)
    if not context.args: return await update.message.reply_text("<b>📌 USAGE:</b> <code>/chatbot on/off</code>", parse_mode=ParseMode.HTML)
    chat, action = update.effective_chat, context.args[0].lower()
    if action == "on":
        chatbot_collection.update_one({"chat_id": f"settings_{chat.id}"}, {"$set": {"enabled": True}}, upsert=True)
        await update.message.reply_text("<b>✅ 『 CHATBOT ON 』\n\n🤖 Ab ayega maja baby 😉.</b>", parse_mode=ParseMode.HTML)
    elif action == "off":
        chatbot_collection.update_one({"chat_id": f"settings_{chat.id}"}, {"$set": {"enabled": False}}, upsert=True)
        await update.message.reply_text("<b>📴 『 CHATBOT OFF 』\n\n🔇 baby off kr diye mujhe 🥺.</b>", parse_mode=ParseMode.HTML)

async def ai_message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    if not msg or not msg.text or msg.text.startswith("/"): return
    text, user_name = msg.text.lower().strip(), msg.from_user.first_name

    # Identity Check
    if any(x in text for x in ["owner", "malik", "admin", "creator"]):
        return await msg.reply_text(f"『 𝐇ᴀʀɪ 』</b>", parse_mode=ParseMode.HTML)

    # Status Check
    if update.effective_chat.type != ChatType.PRIVATE:
        doc = chatbot_collection.find_one({"chat_id": f"settings_{update.effective_chat.id}"}, {"enabled": 1})
        if doc and not doc.get("enabled", True): return

    # Database Response
    responses = get_chat_response(text)
    if responses:
        reply = random.choice(responses)
        if "{name}" in reply: reply = reply.replace("{name}", f"<b>{user_name}</b>")
        await msg.reply_text(reply, parse_mode=ParseMode.HTML)
