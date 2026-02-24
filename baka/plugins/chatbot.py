# Copyright (c) 2026 Telegram:- @WTF_Phantom <DevixOP>
import requests
import re
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode, ChatType
from baka.config import MISTRAL_API_KEY, BOT_NAME
from baka.database import (
    chatbot_collection, 
    save_used_word, 
    get_banned_words
)

# --- 🧠 CORE AI ENGINE ---
async def get_mistral_response(user_id, user_text):
    if not MISTRAL_API_KEY:
        return None
    
    url = "https://api.mistral.ai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {MISTRAL_API_KEY}", "Content-Type": "application/json"}
    
    banned = get_banned_words(user_id)
    past_vocab = ", ".join(banned[-50:])

    system_prompt = (
        f"Tu {BOT_NAME} hai, ek mast desi ladki. "
        "Rules: Max 4 words. Hinglish bolna. "
        "Strictly NO symbols or emojis. "
        f"Ye words repeat mat karna: [{past_vocab}]. "
        "Fresh words use kar."
    )
    
    data = {
        "model": "open-mistral-7b",
        "messages": [{"role": "system", "content": system_prompt}, {"role": "user", "content": user_text}],
        "max_tokens": 25,
        "temperature": 1.0,
        "repetition_penalty": 2.0 
    }
    
    try:
        response = requests.post(url, json=data, headers=headers, timeout=8)
        ans = response.json()['choices'][0]['message']['content'].strip()
        clean_text = re.sub(r'[*"\'#_`-]', '', ans)
        
        for word in clean_text.lower().split():
            if len(word) > 2:
                save_used_word(user_id, word)
        
        return clean_text
    except:
        return None

# --- ⚙️ SETTINGS ---
async def chatbot_toggle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    doc = chatbot_collection.find_one({"chat_id": f"settings_{chat_id}"})
    status = doc.get("enabled", True) if doc else True
    
    new_val = not status
    chatbot_collection.update_one({"chat_id": f"settings_{chat_id}"}, {"$set": {"enabled": new_val}}, upsert=True)
    
    txt = "✅ Enabled" if new_val else "❌ Disabled"
    await update.message.reply_text(f"🤖 Chatbot Status Updated: <b>{txt}</b>", parse_mode=ParseMode.HTML)

# --- 💬 HANDLERS ---
async def ask_ai(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args: return
    
    user = update.effective_user
    res = await get_mistral_response(user.id, " ".join(context.args))
    
    if res:
        tag = f"<a href='tg://user?id={user.id}'>{user.first_name}</a>"
        await update.message.reply_text(f"{tag} {res}", parse_mode=ParseMode.HTML, disable_web_page_preview=True)

async def ai_message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.effective_message
    if not msg or not msg.text or msg.text.startswith("/") or msg.from_user.is_bot:
        return
        
    chat = update.effective_chat
    user = update.effective_user
    
    doc = chatbot_collection.find_one({"chat_id": f"settings_{chat.id}"})
    if doc and not doc.get("enabled", True):
        return
        
    reply = await get_mistral_response(user.id, msg.text)
    
    if reply:
        if chat.type == ChatType.PRIVATE:
            await msg.reply_text(reply, disable_web_page_preview=True)
        else:
            tag = f"<a href='tg://user?id={user.id}'>{user.first_name}</a>"
            await msg.reply_text(f"{tag} {reply}", parse_mode=ParseMode.HTML, disable_web_page_preview=True)
