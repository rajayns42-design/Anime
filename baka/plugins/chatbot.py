# Final Fusion: Ultra-Smart Life-Time Memory Chatbot
import requests
import re
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from baka.config import MISTRAL_API_KEY, BOT_NAME
from baka.database import chatbot_collection

# Life-Time Vocabulary: Jo ek baar bola, wo hamesha ke liye block
LIFE_WORDS = {}

async def get_mistral_response(user_id, user_text):
    if not MISTRAL_API_KEY:
        return None
    
    url = "https://api.mistral.ai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {MISTRAL_API_KEY}", "Content-Type": "application/json"}
    
    # Life-time memory se purane saare shabdon ki list banana
    past_vocab = ", ".join(list(LIFE_WORDS.get(user_id, set())))

    system_prompt = (
        f"You are {BOT_NAME}, a smart Indian girl. "
        "STRICT PROTOCOL:\n"
        "1. Max 4 words. Use Hinglish.\n"
        "2. Strictly NO symbols like * or quotes. No emojis.\n"
        f"3. NEVER use these words again in your life: [{past_vocab}].\n"
        "4. Every reply must use BRAND NEW words. Be creative."
    )
    
    data = {
        "model": "mistral-tiny",
        "messages": [
            {"role": "system", "content": system_prompt}, 
            {"role": "user", "content": user_text}
        ],
        "max_tokens": 10,
        "temperature": 1.0,
        "repetition_penalty": 2.0 # Maximum strictness for new content
    }
    
    try:
        response = requests.post(url, json=data, headers=headers, timeout=8)
        raw_text = response.json()['choices'][0]['message']['content'].strip()
        
        # Symbol cleaning (No * or quotes)
        clean_text = re.sub(r'[*"\'#_`-]', '', raw_text)
        
        # Update Life-Time Memory
        if user_id not in LIFE_WORDS:
            LIFE_WORDS[user_id] = set()
        
        for word in clean_text.lower().split():
            if len(word) > 2: # Chote words ignore, bade words block
                LIFE_WORDS[user_id].add(word)
        
        return clean_text
    except:
        return None

# --- 🛠️ 1. Settings: Toggle On/Off ---
async def chatbot_toggle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    doc = chatbot_collection.find_one({"chat_id": f"settings_{chat_id}"})
    is_on = doc.get("enabled", True) if doc else True
    
    status = "✅ Active" if is_on else "❌ Inactive"
    button = "Turn Off ❌" if is_on else "Turn On ✅"
    
    await update.message.reply_text(
        f"<b>🤖 {BOT_NAME} AI Settings</b>\nStatus: <code>{status}</code>",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(button, callback_data="cb_toggle")]]),
        parse_mode=ParseMode.HTML
    )

# --- 🛠️ 2. Callback: Button Logic ---
async def chatbot_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    chat_id = update.effective_chat.id
    
    doc = chatbot_collection.find_one({"chat_id": f"settings_{chat_id}"})
    new_status = not (doc.get("enabled", True) if doc else True)
    
    chatbot_collection.update_one({"chat_id": f"settings_{chat_id}"}, {"$set": {"enabled": new_status}}, upsert=True)
    
    msg = "Enabled ✅" if new_status else "Disabled ❌"
    btn = "Turn Off ❌" if new_status else "Turn On ✅"
    
    await query.answer(f"Chatbot {msg}")
    await query.edit_message_text(
        f"<b>🤖 Chatbot is now {msg}!</b>",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(btn, callback_data="cb_toggle")]]),
        parse_mode=ParseMode.HTML
    )

# --- 💬 3. Listener: Auto Response ---
async def ai_message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.effective_message
    if not msg or not msg.text or msg.text.startswith("/") or msg.from_user.is_bot:
        return
        
    chat_id = update.effective_chat.id
    doc = chatbot_collection.find_one({"chat_id": f"settings_{chat_id}"})
    if doc and not doc.get("enabled", True):
        return
        
    reply = await get_mistral_response(update.effective_user.id, msg.text)
    if reply:
        await msg.reply_text(reply)

# Admin Placeholders
async def add_chat(u, c): pass
async def bulk_add(u, c): pass
