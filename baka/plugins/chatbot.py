# Copyright (c) 2026 Telegram:- @WTF_Phantom <DevixOP>
import requests
import re
import asyncio
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode, ChatType
from baka.config import MISTRAL_API_KEY, BOT_NAME
from baka.database import chatbot_collection, save_used_word, get_banned_words

# --- ⚡ FAST AI ENGINE ---
async def get_mistral_response(user_id, user_text):
    if not MISTRAL_API_KEY:
        return None
    
    url = "https://api.mistral.ai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {MISTRAL_API_KEY}", "Content-Type": "application/json"}
    
    banned_list = get_banned_words(user_id) 
    banned_str = ", ".join(banned_list[-100:]) # Memory limit for speed

    system_prompt = (
        f"Tu {BOT_NAME} hai, ek cute desi ladki. "
        "Rule: Ek word life mein sirf ek baar bolna. "
        f"Ye words ban hain: [{banned_str}]. "
        "Short, cute aur fast Hinglish reply de. No symbols. No emojis."
    )
    
    data = {
        "model": "open-mistral-7b",
        "messages": [{"role": "system", "content": system_prompt}, {"role": "user", "content": user_text}],
        "max_tokens": 20, # Fast processing
        "temperature": 0.9,
    }
    
    try:
        response = requests.post(url, json=data, headers=headers, timeout=5)
        ans = response.json()['choices'][0]['message']['content'].strip()
        
        # Clean text
        clean_text = re.sub(r'[^a-zA-Z0-9\s]', '', ans)
        
        # Save words for lifetime unique rule
        for word in clean_text.lower().split():
            if len(word) > 1:
                save_used_word(user_id, word)
        
        return clean_text
    except:
        return None

# --- ⚙️ TOGGLE ---
async def chatbot_toggle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    doc = chatbot_collection.find_one({"chat_id": f"settings_{chat_id}"})
    status = doc.get("enabled", True) if doc else True
    new_val = not status
    chatbot_collection.update_one({"chat_id": f"settings_{chat_id}"}, {"$set": {"enabled": new_val}}, upsert=True)
    
    label = "✅ On" if new_val else "❌ Off"
    await update.message.reply_text(f"<b>{BOT_NAME} AI: {label}</b>", parse_mode=ParseMode.HTML)

# --- 💬 REAL-TIME REPLY ---
async def ai_message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.effective_message
    if not msg or not msg.text or msg.text.startswith("/") or msg.from_user.is_bot:
        return
        
    chat = update.effective_chat
    user = update.effective_user
    
    # Check if enabled
    doc = chatbot_collection.find_one({"chat_id": f"settings_{chat.id}"})
    if doc and not doc.get("enabled", True):
        return
        
    reply = await get_mistral_response(user.id, msg.text)
    
    if reply:
        # Fast typing feel
        await context.bot.send_chat_action(chat_id=chat.id, action="typing")
        
        if chat.type == ChatType.PRIVATE:
            await msg.reply_text(reply.lower(), disable_web_page_preview=True)
        else:
            # Sirf shuru mein ek baar naam, uske baad pure sentence mein kahin tag nahi
            mention = f"<a href='tg://user?id={user.id}'>{user.first_name}</a>"
            final_resp = f"{mention} {reply.lower()}"
            await msg.reply_text(final_resp, parse_mode=ParseMode.HTML, disable_web_page_preview=True)
