# Copyright (c) 2026 Telegram:- @WTF_Phantom <DevixOP>
# Edited for Malik: ZEXX (Full Smart Fixed Edition)

import random
import requests
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from baka.config import MISTRAL_API_KEY, BOT_NAME
from baka.database import chatbot_collection

# --- Smart Memory Storage ---
USER_MEMORY = {}

# =====================================
# 🧠 MISTRAL AI ENGINE (NO REPEAT)
# =====================================

async def get_mistral_response(user_id, user_text):
    """Mistral API logic for Angel Personality"""
    if not MISTRAL_API_KEY:
        return None
        
    url = "https://api.mistral.ai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {MISTRAL_API_KEY}", "Content-Type": "application/json"}
    
    # Character instruction for the AI
    system_prompt = (
        f"You are a friendly Indian girl named {BOT_NAME}. Talk in short, natural Hinglish. "
        "Use 1 emoji. Be sweet and casual. Ek bar jo bol diya dobara mat bolna."
    )

    # Repetition control logic
    previous_reply = USER_MEMORY.get(user_id, "")
    full_prompt = f"User: {user_text}\n(Note: Don't repeat your last reply: '{previous_reply}')"

    data = {
        "model": "mistral-tiny",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": full_prompt}
        ],
        "max_tokens": 40,
        "temperature": 0.8
    }

    try:
        response = requests.post(url, json=data, headers=headers, timeout=7)
        ai_reply = response.json()['choices'][0]['message']['content']
        # Update memory for next time
        USER_MEMORY[user_id] = ai_reply
        return ai_reply
    except Exception as e:
        print(f"AI ERROR: {e}")
        return None

# =====================================
# 🛠️ FIXED: chatbot_toggle (Fixes Image 1 Error)
# =====================================

async def chatbot_toggle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles /chatbot command to enable/disable AI"""
    chat_id = update.effective_chat.id
    user = update.effective_user

    # Admin check for groups
    if update.effective_chat.type != "private":
        try:
            member = await context.bot.get_chat_member(chat_id, user.id)
            if member.status not in ["creator", "administrator"]:
                return await update.message.reply_text("Babu, sirf admins hi chatbot control kar sakte hain! 🌸")
        except Exception:
            return

    # Database logic for status
    doc = chatbot_collection.find_one({"chat_id": f"settings_{chat_id}"})
    is_enabled = doc.get("enabled", True) if doc else True
    
    # Toggle status
    new_status = not is_enabled
    chatbot_collection.update_one(
        {"chat_id": f"settings_{chat_id}"},
        {"$set": {"enabled": new_status}},
        upsert=True
    )
    
    status_text = "On ✅" if new_status else "Off ❌"
    await update.message.reply_text(f"Chatbot ab {status_text} hai! ✨")

# =====================================
# 🛠️ FIXED: ask_ai (Fixes Image 2 Error)
# =====================================

async def ask_ai(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles /ask command specifically"""
    if not context.args:
        return await update.message.reply_text("Babu, kuch pucho toh sahi! Example: `/ask kaise ho?` 🌸")
    
    query = " ".join(context.args)
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    
    reply = await get_mistral_response(update.effective_user.id, query)
    if reply:
        await update.message.reply_text(reply)
    else:
        await update.message.reply_text("Uff.. dimag nahi chal raha abhi! 😅")

# =====================================
# 💬 AUTOMATIC CHAT HANDLER
# =====================================

async def ai_message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles general text messages for AI interaction"""
    msg = update.effective_message
    if not msg or not msg.text or msg.text.startswith("/"): 
        return
    
    chat_id = update.effective_chat.id
    
    # Check if chatbot is disabled in database
    doc = chatbot_collection.find_one({"chat_id": f"settings_{chat_id}"})
    if doc and not doc.get("enabled", True):
        return

    # Typing effect for realism
    await context.bot.send_chat_action(chat_id=chat_id, action="typing")
    
    reply = await get_mistral_response(update.effective_user.id, msg.text.strip())
    
    if reply:
        await msg.reply_text(reply)
