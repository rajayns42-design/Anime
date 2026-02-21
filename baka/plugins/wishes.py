# Copyright (c) 2026 Telegram:- @WTF_Phantom <DevixOP>
# Special Wishes Plugin: Morning, Night, Festivals & Love

import re
import random
from telegram import Update
from telegram.ext import ContextTypes
from baka.config import BOT_NAME

# --- 📝 WISHES DATA ---
WISHES_DATA = {
    "morning": [
        "Good morning babu! ✨ Uth gaye? ❤️",
        "Suprabhat! Aapka din bahut accha jaye. 🌸",
        "Morning ji! Coffee peeli ya abhi bhi so rahe ho? 😂",
        "Utho utho, Angel ne yaad kiya hai! 🫧"
    ],
    "night": [
        "Good night! Sapno mein milte hain. 🌙❤️",
        "So jao ab, kal phir baatein karenge. ✨",
        "Shubh ratri! Mast neend aaye aapko. 💤",
        "Good night ji, thak gaye hoge na? Rest karlo. 🌸"
    ],
    "love": [
        "Aww, itna pyar? Nazar na lage! ❤️✨",
        "I love you too... as a friend! 😂 mazak tha re.",
        "Aap bahut sweet ho, sach mein! 🌸",
        "Pyar vayar toh hota rahega, pehle party do! 🥂"
    ],
    "festivals": [
        "Happy Holi! Rangon ki tarah aapki life bhi colorful ho. 🌈",
        "Diwali Mubarak! Khushiyon wala saal rahe aapka. ✨🪔",
        "Eid Mubarak! Allah aapko bohot khush rakhe. 🌙",
        "Happy Festival! Khoob enjoy karna. 💃"
    ],
    "marriage": [
        "Shaadi Mubarak ho! Khush raho humesha. 💍✨",
        "Arey wah! Party kab hai phir? Badhai ho! 🎉",
        "Best wishes for your new journey! ❤️",
        "Shaadi ki dher saari shubhkamnayein! 🌸"
    ]
}

# --- 🧠 LOGIC ENGINE ---
async def wishes_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.effective_message
    if not msg or not msg.text or msg.text.startswith("/"):
        return

    text = msg.text.lower()
    reply = None

    # Keyword Matching
    if any(word in text for word in ["gm", "morning", "good morning", "suprabhat"]):
        reply = random.choice(WISHES_DATA["morning"])
    elif any(word in text for word in ["gn", "night", "good night", "shubh ratri"]):
        reply = random.choice(WISHES_DATA["night"])
    elif any(word in text for word in ["love you", "i love you", "pyar"]):
        reply = random.choice(WISHES_DATA["love"])
    elif any(word in text for word in ["diwali", "holi", "eid", "mubarak", "festival"]):
        reply = random.choice(WISHES_DATA["festivals"])
    elif any(word in text for word in ["marriage", "shaadi", "wedding", "shadi"]):
        reply = random.choice(WISHES_DATA["marriage"])

    if reply:
        await msg.reply_text(reply)

