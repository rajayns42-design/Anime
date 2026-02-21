# Copyright (c) 2026 Telegram:- @WTF_Phantom <DevixOP>
# Full Fixed Code for Ryan.py Integration

import random
import requests
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from baka.config import MISTRAL_API_KEY, BOT_NAME
from baka.database import chatbot_collection

# Memory to prevent repetition
USER_MEMORY = {}

# --- 🧠 AI ENGINE ---
async def get_mistral_response(user_id, user_text):
    if not MISTRAL_API_KEY:
        return None
    url = "https://api.mistral.ai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {MISTRAL_API_KEY}", "Content-Type": "application/json"}
    system_prompt = f"You are a friendly Indian girl named {BOT_NAME}. Talk in short Hinglish. Max 20 words."
    prev_reply = USER_MEMORY.get(user_id, "")
    data = {
        "model": "mistral-tiny",
        "messages": [{"role": "system", "content": system_prompt}, {"role": "user", "content": f"{user_text} (Don't repeat: {prev_reply})"}],
        "max_tokens": 20,
        "temperature": 0.8
    }
    try:
        response = requests.post(url, json=data, headers=headers, timeout=7)
        ai_reply = response.json()['choices'][0]['message']['content']
        USER_MEMORY[user_id] = ai_reply
        return ai_reply
    except:
        return None

# --- 🛠️ FIX 1: chatbot_toggle ---
async def chatbot_toggle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    doc = chatbot_collection.find_one({"chat_id": f"settings_{chat_id}"})
    is_enabled = doc.get("enabled", True) if doc else True
    
    status = "Enabled ✅" if is_enabled else "Disabled ❌"
    buttons = [[InlineKeyboardButton(f"Turn {'Off ❌' if is_enabled else 'On ✅'}", callback_data="cb_toggle")]]
    await update.message.reply_text(f"Chatbot Status: {status}", reply_markup=InlineKeyboardMarkup(buttons))

# --- 🛠️ FIX 2: ask_ai ---
async def ask_ai(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        return await update.message.reply_text("Babu, kuch pucho toh sahi! Example: /ask hi")
    query = " ".join(context.args)
    reply = await get_mistral_response(update.effective_user.id, query)
    await update.message.reply_text(reply or "Uff.. network issue! 🌸")

# --- 🛠️ FIX 3: chatbot_callback ---
async def chatbot_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    chat_id = update.effective_chat.id
    if query.data == "cb_toggle":
        doc = chatbot_collection.find_one({"chat_id": f"settings_{chat_id}"})
        new_status = not (doc.get("enabled", True) if doc else True)
        chatbot_collection.update_one({"chat_id": f"settings_{chat_id}"}, {"$set": {"enabled": new_status}}, upsert=True)
        status_text = "On ✅" if new_status else "Off ❌"
        await query.answer(f"Chatbot turned {status_text}")
        await query.edit_message_text(f"Chatbot status updated to: {status_text}")

# --- 💬 MESSAGE HANDLER ---
async def ai_message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.effective_message
    if not msg or not msg.text or msg.text.startswith("/"): return
    chat_id = update.effective_chat.id
    doc = chatbot_collection.find_one({"chat_id": f"settings_{chat_id}"})
    if doc and not doc.get("enabled", True): return
    reply = await get_mistral_response(update.effective_user.id, msg.text)
    if reply: await msg.reply_text(reply)
