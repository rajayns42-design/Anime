# Copyright (c) 2026 Telegram:- @WTF_Phantom <DevixOP>
# Fixed by Gemini: ZEXX Edition (Private + Group + Buttons Support)

import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from telegram.constants import ParseMode, ChatType
from baka.database import chatbot_collection, add_chat_to_db, get_chat_response

OWNER_ID = 8321028072

async def is_admin_or_owner(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id == OWNER_ID: return True
    if update.effective_chat.type == ChatType.PRIVATE: return True
    try:
        member = await context.bot.get_chat_member(update.effective_chat.id, user_id)
        return member.status in ["creator", "administrator"]
    except Exception: return False

# =====================================
# 🛠️ MISSING ATTRIBUTES (FIXED)
# =====================================

async def ask_ai(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Fixes AttributeError: 'ask_ai'"""
    if not update.effective_message or not context.args:
        return await update.effective_message.reply_text("<b>📌 USAGE:</b> <code>/ask hello</code>", parse_mode=ParseMode.HTML)
    query = " ".join(context.args).lower().strip()
    response = get_chat_response(query)
    if response:
        reply = random.choice(response) if isinstance(response, list) else response
        if "{name}" in reply: reply = reply.replace("{name}", f"<b>{update.effective_user.first_name}</b>")
        await update.effective_message.reply_text(reply, parse_mode=ParseMode.HTML)
    else:
        await update.effective_message.reply_text("<b>❌ No response found baby.</b>", parse_mode=ParseMode.HTML)

async def chatbot_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Fixes AttributeError: 'chatbot_callback'"""
    query = update.callback_query
    if not await is_admin_or_owner(update, context):
        return await query.answer("Admin only baby!", show_alert=True)
    
    data = query.data.replace("cb_", "")
    chat_id = update.effective_chat.id
    
    if data == "enable":
        chatbot_collection.update_one({"chat_id": f"settings_{chat_id}"}, {"$set": {"enabled": True}}, upsert=True)
        await query.edit_message_text("<b>✅ Chatbot Enabled!</b>", parse_mode=ParseMode.HTML)
    elif data == "disable":
        chatbot_collection.update_one({"chat_id": f"settings_{chat_id}"}, {"$set": {"enabled": False}}, upsert=True)
        await query.edit_message_text("<b>📴 Chatbot Disabled!</b>", parse_mode=ParseMode.HTML)
    await query.answer()

# =====================================
# 🚀 OTHER COMMANDS
# =====================================

async def add_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        return await update.message.reply_text("<b>❌ Owner only!</b>", parse_mode=ParseMode.HTML)
    try:
        args = update.message.text.split(None, 1)[1]
        word, response = args.split("|", 1)
        add_chat_to_db(word.strip().lower(), response.strip())
        await update.message.reply_text("<b>✅ Added!</b>", parse_mode=ParseMode.HTML)
    except:
        await update.message.reply_text("<b>📌 Format:</b> <code>/addchat hi | hello</code>", parse_mode=ParseMode.HTML)

async def chatbot_toggle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Shows buttons to turn chatbot on/off"""
    keyboard = [
        [InlineKeyboardButton("On ✅", callback_data="cb_enable"),
         InlineKeyboardButton("Off 📴", callback_data="cb_disable")]
    ]
    await update.message.reply_text("<b>🤖 Chatbot Settings:</b>", 
                                  reply_markup=InlineKeyboardMarkup(keyboard),
                                  parse_mode=ParseMode.HTML)

async def ai_message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.effective_message
    if not msg or not msg.text or msg.text.startswith("/"): return
    chat = update.effective_chat
    if chat.type in [ChatType.GROUP, ChatType.SUPERGROUP]:
        doc = chatbot_collection.find_one({"chat_id": f"settings_{chat.id}"})
        if doc and not doc.get("enabled", True): return
    
    responses = get_chat_response(msg.text.lower().strip())
    if responses:
        reply = random.choice(responses) if isinstance(responses, list) else responses
        if "{name}" in reply: reply = reply.replace("{name}", f"<b>{msg.from_user.first_name}</b>")
        await msg.reply_text(reply, parse_mode=ParseMode.HTML)
