import requests
import re
import random
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
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
    
    # Vocabulary fetch karna
    banned = get_banned_words(user_id)
    past_vocab = ", ".join(banned[-50:])

    system_prompt = (
        f"Tu {BOT_NAME} hai, ek cool desi ladki. "
        "Rules: Max 4 words. Hinglish bolna. "
        "Strictly NO symbols or emojis. "
        f"Ye words repeat mat karna: [{past_vocab}]. "
        "Fresh and unique words use kar."
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
        
        # Safai: Symbols hatane ke liye
        clean_text = re.sub(r'[*"\'#_`-]', '', ans)
        
        # Words save karna taaki repeat na ho
        for word in clean_text.lower().split():
            if len(word) > 2:
                save_used_word(user_id, word)
        
        return clean_text
    except:
        return None

# --- 🛠️ TOGGLE MENU & HELP ---
async def chatbot_toggle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    doc = chatbot_collection.find_one({"chat_id": f"settings_{chat_id}"})
    status = doc.get("enabled", True) if doc else True
    
    txt = "✅ Enabled" if status else "❌ Disabled"
    btn_txt = "Switch Off ❌" if status else "Switch On ✅"
    
    keyboard = [
        [InlineKeyboardButton(btn_txt, callback_data="cb_toggle")],
        [InlineKeyboardButton("❓ Help / Support", callback_data="cb_help")]
    ]
    
    await update.message.reply_text(
        f"<b>🤖 {BOT_NAME} Chat Settings</b>\n\n"
        f"Group Status: <code>{txt}</code>\n"
        "AI will reply to all messages automatically.",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode=ParseMode.HTML
    )

async def chatbot_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    chat_id = query.message.chat.id
    
    if query.data == "cb_toggle":
        doc = chatbot_collection.find_one({"chat_id": f"settings_{chat_id}"})
        new_val = not (doc.get("enabled", True) if doc else True)
        chatbot_collection.update_one({"chat_id": f"settings_{chat_id}"}, {"$set": {"enabled": new_val}}, upsert=True)
        await query.answer("Bot Settings Updated!")
        
        # UI Refresh
        txt = "✅ Enabled" if new_val else "❌ Disabled"
        btn_txt = "Switch Off ❌" if new_val else "Switch On ✅"
        kb = [[InlineKeyboardButton(btn_txt, callback_data="cb_toggle")], [InlineKeyboardButton("❓ Help", callback_data="cb_help")]]
        await query.edit_message_text(f"<b>🤖 {BOT_NAME} Chat Settings</b>\n\nStatus: <code>{txt}</code>", reply_markup=InlineKeyboardMarkup(kb), parse_mode=ParseMode.HTML)
        
    if query.data == "cb_help":
        await query.answer("Bas group me baatein karo, AI khud reply degi!", show_alert=True)

# --- 💬 MESSAGE HANDLERS ---
async def ask_ai(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args: return await update.message.reply_text("Kuch toh bolo baby!")
    
    user = update.effective_user
    res = await get_mistral_response(user.id, " ".join(context.args))
    
    if res:
        tag = f"<a href='tg://user?id={user.id}'>{user.first_name}</a>"
        await update.message.reply_text(f"{tag} {res}", parse_mode=ParseMode.HTML)

async def ai_message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.effective_message
    if not msg or not msg.text or msg.text.startswith("/") or msg.from_user.is_bot:
        return
        
    chat_id = update.effective_chat.id
    doc = chatbot_collection.find_one({"chat_id": f"settings_{chat_id}"})
    
    # Global default is Enabled
    if doc and not doc.get("enabled", True):
        return
        
    user = update.effective_user
    reply = await get_mistral_response(user.id, msg.text)
    
    if reply:
        tag = f"<a href='tg://user?id={user.id}'>{user.first_name}</a>"
        await msg.reply_text(f"{tag} {reply}", parse_mode=ParseMode.HTML)
