# Updated by Gemini: Girl Personality + Smart Memory Edition

import random
import requests
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode

# Mistral Config
MISTRAL_API_KEY = "TERI_MISTRAL_API_KEY_YAHAN_DALO"

# Duplicate rokne ke liye simple memory (Temporary)
USER_MEMORY = {}

async def get_mistral_response(user_id, user_text):
    url = "https://api.mistral.ai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {MISTRAL_API_KEY}", "Content-Type": "application/json"}
    
    # Ladki jaisa behavior set karne ke liye prompt
    system_prompt = (
        "You are a friendly Indian girl. Talk in short, natural Hinglish. "
        "Use 1 emojis. Don't be formal. Don't repeat your ak bar jo bol do dobara mat bolna wo word. "
        "Keep it sweet and casual, like a friend. No long paragraphs."
    )

    # Memory check to avoid repetition
    previous_reply = USER_MEMORY.get(user_id, "")
    full_prompt = f"{user_text} (Note: Don't say anything like '{previous_reply}')"

    data = {
        "model": "mistral-tiny",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": full_prompt}
        ],
        "max_tokens": 20,
        "temperature": 0.8 # Thoda creative banane ke liye
    }

    try:
        response = requests.post(url, json=data, headers=headers, timeout=7)
        ai_reply = response.json()['choices'][0]['message']['content']
        # Update memory
        USER_MEMORY[user_id] = ai_reply
        return ai_reply
    except:
        return None

async def ai_message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.effective_message
    if not msg or not msg.text or msg.text.startswith("/"): return
    
    user_id = update.effective_user.id
    user_query = msg.text.strip()

    # Bot ko thoda delay dena natural lagta hai
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    
    # AI Response
    reply = await get_mistral_response(user_id, user_query)
    
    if reply:
        # Extra filter for variety
        await msg.reply_text(reply)
    else:
        fallback_replies = ["Hmm.. kya bola?", "Kuch bhi? 😂", "Sunna.. firse bolna", "Acha? 🤔"]
        await msg.reply_text(random.choice(fallback_replies))

# ... (Baaki commands purane hi rahenge)
