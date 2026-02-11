import random
import httpx
from datetime import datetime
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from baka.database import groups_collection, users_collection
from baka.utils import ensure_user_exists, get_mention

# In-Memory Drop Storage
active_drops = {}
DROP_MESSAGE_COUNT = 100

WAIFU_NAMES = [
    ("Rem", "rem"), ("Ram", "ram"), ("Emilia", "emilia"), ("Asuna", "asuna"), 
    ("Zero Two", "zero two"), ("Makima", "makima"), ("Nezuko", "nezuko"),
    ("Hinata", "hinata"), ("Sakura", "sakura"), ("Mikasa", "mikasa"), 
    ("Yor", "yor"), ("Anya", "anya"), ("Power", "power")
]

async def check_drops(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Fast check: Agar message valid nahi hai toh turant bahar nikal jao
    if not update.message or not update.effective_chat or update.effective_chat.type == "private":
        return
    
    chat_id = update.effective_chat.id

    # Database update aur message count track karna
    group = groups_collection.find_one_and_update(
        {"chat_id": chat_id}, {"$inc": {"msg_count": 1}}, upsert=True, return_document=True
    )

    # Check agar drop ka time ho gaya hai
    if group.get("msg_count", 0) % DROP_MESSAGE_COUNT == 0:
        name, slug = random.choice(WAIFU_NAMES)

        async with httpx.AsyncClient() as client:
            try:
                r = await client.get(f"https://api.waifu.im/search?included_tags={slug}", timeout=5.0)
                url = r.json()['images'][0]['url'] if r.status_code == 200 else "https://telegra.ph/file/5e5480760e412bd402e88.jpg"
            except:
                url = "https://telegra.ph/file/5e5480760e412bd402e88.jpg"

        active_drops[chat_id] = name.lower()

        await update.message.reply_photo(
            photo=url,
            caption=f"👧 <b>A Waifu Appeared!</b>\n\nGuess her name to collect her!\n<i>Reply to this image.</i>",
            parse_mode=ParseMode.HTML
        )

async def collect_waifu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Fast Validation: Ek hi line mein saare checks
    if not update.message or not update.message.text or update.effective_chat.id not in active_drops:
        return

    msg = update.message
    chat_id = update.effective_chat.id
    
    # Input clean karein (Yahan error fix ho gayi hai)
    guess = msg.text.lower().strip()
    correct = active_drops[chat_id]

    if guess == correct:
        # User exist karta hai check karein
        user = ensure_user_exists(msg.from_user)
        del active_drops[chat_id] # Drop clear karein taaki dusra guess na ho sake

        rarity = random.choice(["Common", "Rare", "Epic", "Legendary"])
        waifu = {"name": correct.title(), "rarity": rarity, "date": datetime.utcnow()}
        
        # Database mein save karein
        users_collection.update_one(
            {"user_id": user['user_id']}, 
            {"$push": {"waifus": waifu}}
        )

        await msg.reply_text(
            f"🎉 <b>Collected!</b>\n\n👤 {get_mention(user)} caught <b>{correct.title()}</b>!\n🌟 <b>Rarity:</b> {rarity}",
            parse_mode=ParseMode.HTML
        )
