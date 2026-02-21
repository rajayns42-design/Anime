# Copyright (c) 2026 Telegram:- @WTF_Phantom <DevixOP>
# Edited for Malik: ZEXX (Full Smart Memory Edition)

import random
import requests
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler, MessageHandler, filters
from telegram.constants import ParseMode, ChatType
from baka.config import MISTRAL_API_KEY, BOT_NAME
from baka.database import chatbot_collection # Database connection for toggle

# --- Smart Memory Storage ---
# Isme pichle replies save honge taaki bot same cheez baar-baar na bole
USER_MEMORY = {}

# =====================================
# 🧠 MISTRAL AI ENGINE (NO REPEAT LOGIC)
# =====================================

async def get_mistral_response(user_id, user_text):
    if not MISTRAL_API_KEY:
        return None
        
    url = "https://api.mistral.ai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {MISTRAL_API_KEY}", "Content-Type": "application/json"}
    
    # Ladki jaisi personality + Strictly No Repetition
    system_prompt = (
        f"You are a friendly Indian girl named {BOT_NAME}. Talk in short, natural Hinglish. "
        "Use only 1 emoji. Strictly NO FORMAL words. "
        "Ek baar jo word ya sentence bol diya, use dobara mat bolna. "
        "Keep it sweet and casual, like a real girl friend. Max 15-20 words."
    )

    # Memory check: Pichla reply AI ko bhej rahe hain taaki wo repeat na kare
    previous_reply = USER_MEMORY.get(user_id, "")
    full_prompt = f"User said: {user_text}\n(Note: Don't repeat your last reply: '{previous_reply}')"

    data = {
        "model": "mistral-tiny",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": full_prompt}
        ],
        "max_tokens": 40,
        "temperature": 0.9 # High temperature = variety in replies
    }

    try:
        response = requests.post(url, json=data, headers=headers, timeout=7)
        ai_reply = response.json()['choices'][0]['message']['content']
        # Update memory for next time
        USER_MEMORY[user_id] = ai_reply
        return ai_reply
    except:
        return None

# =====================================
# ⚙️ CHATBOT TOGGLE (FIX FOR CRASH)
# =====================================

async def chatbot_toggle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Isse /chatbot command chalne lagegi aur bot crash nahi hoga"""
    chat_id = update.effective_chat.id
    user = update.effective_user

    # Only admins or owner can toggle
    if chat_id > 0: # Private Chat
        pass
    else: # Groups
        member = await context.bot.get_chat_member(chat_id, user.id)
        if member.status not in ["creator", "administrator"]:
            return await update.message.reply_text("Babu, sirf admins hi chatbot control kar sakte hain! 🌸")

    # DB Logic
    doc = chatbot_collection.find_one({"chat_id": f"settings_{chat_id}"})
    is_enabled = doc.get("enabled", True) if doc else True
    
    new_status = not is_enabled
    chatbot_collection.update_one(
        {"chat_id": f"settings_{chat_id}"},
        {"$set": {"enabled": new_status}},
        upsert=True
    )
    
    status_text = "On ✅" if new_status else "Off ❌"
    await update.message.reply_text(f"Chatbot ab {status_text} hai! ✨")

# =====================================
# 💬 MESSAGE HANDLER
# =====================================

async def ai_message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.effective_message
    if not msg or not msg.text or msg.text.startswith("/"): return
    
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    
    # Check if chatbot is disabled in this chat
    doc = chatbot_collection.find_one({"chat_id": f"settings_{chat_id}"})
    if doc and not doc.get("enabled", True):
        return

    # Typing action for realistic feel
    await context.bot.send_chat_action(chat_id=chat_id, action="typing")
    
    # Get Response
    reply = await get_mistral_response(user_id, msg.text.strip())
    
    if reply:
        await msg.reply_text(reply)
    else:
        # Fallback if API fails
        fallbacks = ["Hmm.. kya bola? 🌸", "Acha? 😂", "Sunna.. firse bolna", "Theek hai baba.. 🤔"]
        await msg.reply_text(random.choice(fallbacks))

# =====================================
# NOTE FOR RYAN.PY:
# app_bot.add_handler(CommandHandler("chatbot", chatbot_toggle))
# app_bot.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), ai_message_handler))
# =====================================
