# Copyright (c) 2025 Telegram:- @WTF_Phantom <DevixOP>
# Location: Supaul, Bihar 

import httpx
import random
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from telegram.constants import ParseMode, ChatAction, ChatType
from telegram.error import BadRequest
from baka.config import MISTRAL_API_KEY, BOT_NAME, OWNER_LINK
from baka.database import chatbot_collection

# Settings
MISTRAL_URL = "https://api.mistral.ai/v1/chat/completions"
MODEL = "mistral-small-latest" 
MAX_HISTORY = 12

STICKER_PACKS = [
    "https://t.me/addstickers/RandomByDarkzenitsu",
    "https://t.me/addstickers/animation_0_8_Cat",
    "https://t.me/addstickers/vhelw_by_CalsiBot"
]

FALLBACK_RESPONSES = [
    "Achha ji?",
    "Hmm... aur batao?",
    "Okk",
    "Sahi hai yaar",
    "babu or bato",
    "kkrh",
    "kuch nhi",
    "khana huaa",
    "kya khaya",
    "apne bare bato",
    "kuch bhi",
    "jo man me ho",
]

async def send_ai_sticker(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        raw_link = random.choice(STICKER_PACKS)
        pack_name = raw_link.split('/')[-1]
        sticker_set = await context.bot.get_sticker_set(pack_name)
        if sticker_set and sticker_set.stickers:
            sticker = random.choice(sticker_set.stickers)
            await update.message.reply_sticker(sticker.file_id)
            return True
    except:
        pass
    return False

# --- MENU HANDLERS ---

async def chatbot_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user

    if chat.type == ChatType.PRIVATE:
        return await update.message.reply_text("Haan baba, DM me active hu! 😉")

    member = await chat.get_member(user.id)
    if member.status not in ['administrator', 'creator']:
        return await update.message.reply_text("Tu Admin nahi hai, Baka!")

    doc = chatbot_collection.find_one({"chat_id": chat.id})
    is_enabled = doc.get("enabled", True) if doc else True
    status = "Enabled" if is_enabled else "Disabled"

    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("Enable", callback_data="ai_enable"), InlineKeyboardButton("Disable", callback_data="ai_disable")],
        [InlineKeyboardButton("Reset", callback_data="ai_reset"), InlineKeyboardButton("Help ❓", callback_data="ai_help")]
    ])
    await update.message.reply_text(f"AI Settings\nStatus: {status}", reply_markup=kb)

async def chatbot_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data
    chat_id = query.message.chat.id

    if data == "ai_help":
        return await query.answer("Baby bat kro n.", show_alert=True)

    member = await query.message.chat.get_member(query.from_user.id)
    if member.status not in ['administrator', 'creator']: 
        return await query.answer("only Admin ke liye hai.", show_alert=True)

    if data == "ai_enable":
        chatbot_collection.update_one({"chat_id": chat_id}, {"$set": {"enabled": True}}, upsert=True)
        await query.message.edit_text("chatbot on ab maja ayega 😚")
    elif data == "ai_disable":
        chatbot_collection.update_one({"chat_id": chat_id}, {"$set": {"enabled": False}}, upsert=True)
        await query.message.edit_text("chatbot off firr yad krna 🥹.")
    elif data == "ai_reset":
        chatbot_collection.update_one({"chat_id": chat_id}, {"$set": {"history": []}}, upsert=True)
        await query.answer("Sab bhool gayi!", show_alert=True)

# --- AI ENGINE ---

async def get_ai_response(chat_id: int, user_input: str, user_name: str):
    if not MISTRAL_API_KEY: return "API Key nahi mil rahi."

    doc = chatbot_collection.find_one({"chat_id": chat_id}) or {}
    history = doc.get("history", [])

    # First message check: Use name only if no history exists
    greeting = f"Oye {user_name}, " if not history else ""

    system_prompt = (
        f"Tum {BOT_NAME} ho. Ek cute Indian girl jo Hinglish me baat karti hai. "
        "Rules: Short replies do. Normal text use karo. Koi fancy font nahi or group or private jaise membar bat kre waishe tum bat krogi koi faltu bate nhi bologi or nhi faltu bate krogi or. "
        "Emoji kabhi kabhi  karo. Zyada sawal mat pucho kisi se bhi."
    )

    messages = [{"role": "system", "content": system_prompt}]
    for msg in history[-MAX_HISTORY:]: 
        messages.append({"role": msg["role"], "content": msg["content"]})
    messages.append({"role": "user", "content": user_input})

    headers = {"Authorization": f"Bearer {MISTRAL_API_KEY}", "Content-Type": "application/json"}
    payload = {"model": MODEL, "messages": messages, "temperature": 0.7, "max_tokens": 20}

    try:
        async with httpx.AsyncClient(timeout=15) as client:
            resp = await client.post(MISTRAL_URL, json=payload, headers=headers)
            if resp.status_code != 200: return "Mood kharab hai mera..."

            reply = resp.json()["choices"][0]["message"]["content"].strip()
            final_reply = f"{greeting}{reply}"

            # History Update
            new_hist = history + [
                {"role": "user", "content": user_input}, 
                {"role": "assistant", "content": reply}
            ]
            chatbot_collection.update_one({"chat_id": chat_id}, {"$set": {"history": new_hist[-20:]}}, upsert=True)
            
            return final_reply
    except:
        return "Network problem hai shayad."

# --- MESSAGE HANDLER ---

async def ai_message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    if not msg or not msg.text or msg.text.startswith("/"): return
    
    chat = update.effective_chat
    
    # Check if enabled in groups
    if chat.type != ChatType.PRIVATE:
        doc = chatbot_collection.find_one({"chat_id": chat.id})
        if doc and not doc.get("enabled", True): return

    await context.bot.send_chat_action(chat_id=chat.id, action=ChatAction.TYPING)
    res = await get_ai_response(chat.id, msg.text, msg.from_user.first_name)
    
    await msg.reply_text(res)

    if random.random() < 0.20:
        await send_ai_sticker(update, context)

async def ask_ai(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args: return
    res = await get_ai_response(update.effective_chat.id, " ".join(context.args), update.effective_user.first_name)
    await update.message.reply_text(res)
