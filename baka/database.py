import random
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode, ChatType
# Telethon wala import delete kar diya hai taaki crash na ho

# ===============================================
# ⚙️ DATABASE FUNCTIONS
# ===============================================

def is_chatbot_enabled(chat_id):
    # Har chat ka apna status check karega
    doc = chatbot_collection.find_one({"chat_id": f"settings_{chat_id}"})
    if doc:
        return doc.get("enabled", True)
    return True

def get_chat_response(word):
    # Database se word match karke random reply uthayega
    data = chatbot_collection.find_one({"word": word.lower().strip()})
    if data and "responses" in data:
        res = data["responses"]
        return random.choice(res) if isinstance(res, list) else res
    return None

# ===============================================
# 🚀 MAIN HANDLER (Private + Group Logic)
# ===============================================

async def ai_message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.effective_message
    
    # Check 1: Agar message text nahi hai ya command hai, toh ignore karo
    if not msg or not msg.text or msg.text.startswith("/"):
        return

    chat = update.effective_chat
    text = msg.text.lower().strip()
    user_name = msg.from_user.first_name

    # Check 2: Group Logic
    if chat.type in [ChatType.GROUP, ChatType.SUPERGROUP]:
        # Agar group mein chatbot OFF hai, toh reply nahi karega
        if not is_chatbot_enabled(chat.id):
            return

    # Check 3: Private Logic
    # Private chat mein bot hamesha reply karega agar word DB mein hai

    # 4. Reply dhoondo
    reply = get_chat_response(text)
    
    if reply:
        # User ka naam add karne ke liye {name} replace karega
        if "{name}" in reply:
            reply = reply.replace("{name}", f"<b>{user_name}</b>")
        
        await msg.reply_text(reply, parse_mode=ParseMode.HTML)
