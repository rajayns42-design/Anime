# Copyright (c) 2026 Telegram:- @WTF_Phantom <DevixOP>
# Full Fixed Code for Chatbot Plugin

import random
import requests
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from baka.config import MISTRAL_API_KEY, BOT_NAME
from baka.database import chatbot_collection

# Memory to prevent AI from repeating its last line
USER_MEMORY = {}

# --- 🧠 AI ENGINE (Mistral API) ---
async def get_mistral_response(user_id, user_text):
    if not MISTRAL_API_KEY:
        return None
    
    url = "https://api.mistral.ai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {MISTRAL_API_KEY}", 
        "Content-Type": "application/json"
    }
    
    # System prompt to give the AI a personality
    system_prompt = f"You are a friendly Indian girl named {BOT_NAME}. Talk in short Hinglish. Use emojis. Max 20 words."
    prev_reply = USER_MEMORY.get(user_id, "")
    
    data = {
        "model": "mistral-tiny",
        "messages": [
            {"role": "system", "content": system_prompt}, 
            {"role": "user", "content": f"{user_text} (Context: Don't repeat: {prev_reply})"}
        ],
        "max_tokens": 30,
        "temperature": 0.8
    }
    
    try:
        response = requests.post(url, json=data, headers=headers, timeout=7)
        ai_reply = response.json()['choices'][0]['message']['content']
        USER_MEMORY[user_id] = ai_reply
        return ai_reply
    except:
        return None

# --- 🛠️ 1. Chatbot Toggle (Settings) ---
async def chatbot_toggle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    # Database se setting uthao
    doc = chatbot_collection.find_one({"chat_id": f"settings_{chat_id}"})
    # Default Enabled (True) agar database mein record na ho
    is_enabled = doc.get("enabled", True) if doc else True
    
    status_icon = "✅ Enabled" if is_enabled else "❌ Disabled"
    button_text = "Turn Off ❌" if is_enabled else "Turn On ✅"
    
    keyboard = [[InlineKeyboardButton(button_text, callback_data="cb_toggle")]]
    
    await update.message.reply_text(
        f"<b>🤖 Chatbot Settings for this Chat:</b>\n\n"
        f"Current Status: <code>{status_icon}</code>\n"
        f"Description: AI will reply to messages automatically.",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode=ParseMode.HTML
    )

# --- 🛠️ 2. Ask AI (Direct Command) ---
async def ask_ai(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        return await update.message.reply_text("Babu, kuch pucho toh sahi! Example: <code>/ask tum kaisi ho?</code>", parse_mode=ParseMode.HTML)
    
    query = " ".join(context.args)
    sent_msg = await update.message.reply_text("Thinking... 💭")
    
    reply = await get_mistral_response(update.effective_user.id, query)
    await sent_msg.edit_text(reply or "Uff.. network issue! Thodi der baad try karo. 🌸")

# --- 🛠️ 3. Callback Handler (Button Click) ---
async def chatbot_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    chat_id = update.effective_chat.id
    
    if query.data == "cb_toggle":
        doc = chatbot_collection.find_one({"chat_id": f"settings_{chat_id}"})
        current_status = doc.get("enabled", True) if doc else True
        new_status = not current_status
        
        # Update Database
        chatbot_collection.update_one(
            {"chat_id": f"settings_{chat_id}"}, 
            {"$set": {"enabled": new_status}}, 
            upsert=True
        )
        
        status_text = "Enabled ✅" if new_status else "Disabled ❌"
        await query.answer(f"Chatbot is now {status_text}")
        
        # Edit message to show new status
        button_text = "Turn Off ❌" if new_status else "Turn On ✅"
        keyboard = [[InlineKeyboardButton(button_text, callback_data="cb_toggle")]]
        
        await query.edit_message_text(
            f"<b>🤖 Chatbot Settings updated!</b>\n\nStatus: <code>{status_text}</code>",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode=ParseMode.HTML
        )

# --- 🛠️ 4. Placeholder Functions (For Ryan.py) ---
async def add_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("This feature is currently under maintenance. 🛠")

async def bulk_add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Admin only feature. 👮‍♂️")

# --- 💬 5. AI Message Listener ---
async def ai_message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.effective_message
    
    # Check if message exists and is not a command
    if not msg or not msg.text or msg.text.startswith("/"):
        return
        
    chat_id = update.effective_chat.id
    
    # Check if AI is enabled for this chat
    doc = chatbot_collection.find_one({"chat_id": f"settings_{chat_id}"})
    if doc and not doc.get("enabled", True):
        return
        
    # Get AI reply
    reply = await get_mistral_response(update.effective_user.id, msg.text)
    if reply:
        await msg.reply_text(reply)
