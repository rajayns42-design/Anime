# Final Master Fusion: Fixed Chat Logic & Help Button
import requests
import re
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from baka.config import MISTRAL_API_KEY, BOT_NAME
from baka.database import chatbot_collection

# Life-Time Vocabulary Storage
LIFE_WORDS = {}

async def get_mistral_response(user_id, user_text):
    if not MISTRAL_API_KEY:
        return None [cite: 2026-02-22]
    
    url = "https://api.mistral.ai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {MISTRAL_API_KEY}", "Content-Type": "application/json"}
    
    # Vocabulary fetch karna [cite: 2026-02-22]
    past_vocab = ", ".join(list(LIFE_WORDS.get(user_id, set()))[-50:])

    system_prompt = (
        f"Tu {BOT_NAME} hai. Ek desi ladki. "
        "Rules: Hinglish bol. Max 4 words. "
        "No symbols like * or quotes. No emojis. "
        f"Ye words mat bolna: [{past_vocab}]."
    ) [cite: 2026-02-22]
    
    data = {
        "model": "open-mistral-7b",
        "messages": [{"role": "system", "content": system_prompt}, {"role": "user", "content": user_text}],
        "max_tokens": 20, # 20 Token Limit [cite: 2026-02-22]
        "temperature": 0.8,
        "repetition_penalty": 2.0 
    }
    
    try:
        response = requests.post(url, json=data, headers=headers, timeout=8)
        raw_text = response.json()['choices'][0]['message']['content'].strip()
        clean_text = re.sub(r'[*"\'#_`-]', '', raw_text) [cite: 2026-02-22]
        
        if user_id not in LIFE_WORDS:
            LIFE_WORDS[user_id] = set()
        for w in clean_text.lower().split():
            if len(w) > 3: LIFE_WORDS[user_id].add(w)
            
        return clean_text
    except:
        return None

# --- 🛠️ 1. Toggle Menu with Help Button ---
async def chatbot_toggle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    doc = chatbot_collection.find_one({"chat_id": f"settings_{chat_id}"})
    status = doc.get("enabled", True) if doc else True
    
    txt = "✅ Enabled" if status else "❌ Disabled"
    btn = "Turn Off ❌" if status else "Turn On ✅"
    
    keyboard = [
        [InlineKeyboardButton(btn, callback_data="cb_toggle")],
        [InlineKeyboardButton("❓ Help", callback_data="cb_help")] # Help button [cite: 2026-02-21]
    ]
    
    await update.message.reply_text(
        f"<b>🤖 {BOT_NAME} AI Settings</b>\nStatus: <code>{txt}</code>",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode=ParseMode.HTML
    )

# --- 🛠️ 2. Callback for Buttons ---
async def chatbot_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    chat_id = query.message.chat.id
    
    if query.data == "cb_toggle":
        doc = chatbot_collection.find_one({"chat_id": f"settings_{chat_id}"})
        new_val = not (doc.get("enabled", True) if doc else True)
        chatbot_collection.update_one({"chat_id": f"settings_{chat_id}"}, {"$set": {"enabled": new_val}}, upsert=True)
        await query.answer("Setting Updated!")
        return await chatbot_toggle(query, context)

    if query.data == "cb_help": # Help functionality [cite: 2026-02-21]
        await query.answer("Help Menu", show_alert=True)
        await query.message.edit_text("Bas group mein msg karo, AI auto reply degi. No commands needed!")

# --- 🛠️ 3. Ask AI (For manual query) ---
async def ask_ai(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args: return await update.message.reply_text("Kuch toh bolo!")
    res = await get_mistral_response(update.effective_user.id, " ".join(context.args))
    await update.message.reply_text(res or "Server error!")

# --- 💬 4. Auto Reply Handler ---
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

# Compatibility placeholders
async def add_chat(u, c): pass
async def bulk_add(u, c): pass
