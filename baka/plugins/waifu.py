# Copyright (c) 2025 Telegram:- @WTF_Phantom <DevixOP>
# Edited for Malik: ZEXX (Fast Social Version)

import httpx
import random
from datetime import datetime, timedelta
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from baka.utils import ensure_user_exists, resolve_target, get_mention, stylize_text, format_money
from baka.database import users_collection
from baka.config import WAIFU_PROPOSE_COST

API_URL = "https://api.waifu.pics"
SFW_ACTIONS = ["kick", "happy", "wink", "poke", "dance", "cringe", "kill", "waifu", "neko", "shinobu", "bully", "cuddle", "cry", "hug", "awoo", "kiss", "lick", "pat", "smug", "bonk", "yeet", "blush", "smile", "wave", "highfive", "handhold", "nom", "bite", "glomp", "slap"]

# --- SOCIAL ACTIONS (FAST) ---
async def waifu_action(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cmd = update.message.text.split()[0].replace("/", "")
    if cmd not in SFW_ACTIONS: return

    target, _ = await resolve_target(update, context)
    user = update.effective_user

    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{API_URL}/sfw/{cmd}")
            url = resp.json()['url']
    except: return

    s_link = get_mention(user)
    t_link = get_mention(target) if target else "the air"
    
    # Custom captions for specific actions
    caption = f"{s_link} {cmd}s {t_link}!"
    if cmd == "kill": caption = f"{s_link} murdered {t_link} 💀"
    if cmd == "kiss": caption = f"{s_link} kissed {t_link} 💋"

    await update.message.reply_animation(animation=url, caption=caption, parse_mode=ParseMode.HTML)

# --- PROPOSE (INSTANT ROAST - NO AI) ---
async def wpropose(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Propose to a Waifu (Uses Gold)."""
    user = ensure_user_exists(update.effective_user)

    if user['balance'] < WAIFU_PROPOSE_COST:
        return await update.message.reply_text(f"❌ <b>Poor!</b> Need {format_money(WAIFU_PROPOSE_COST)}.", parse_mode=ParseMode.HTML)

    users_collection.update_one({"user_id": user['user_id']}, {"$inc": {"balance": -WAIFU_PROPOSE_COST}})

    success = random.random() < 0.3

    if success:
        # Celestial Waifu Success Logic
        async with httpx.AsyncClient() as client:
            r = await client.get("https://api.waifu.im/search?tags=waifu")
            img_url = r.json()['images'][0]['url']

        waifu_data = {"name": "Celestial Queen", "rarity": "Celestial", "date": datetime.utcnow()}
        users_collection.update_one({"user_id": user['user_id']}, {"$push": {"waifus": waifu_data}})

        await update.message.reply_photo(img_url, caption=f"💍 <b>YES!</b>\n\nYou married a <b>CELESTIAL WAIFU</b>!", parse_mode=ParseMode.HTML)
    else:
        # AI Hata kar local fast Hinglish roasts add kiye hain
        local_roasts = [
            "Shakal dekhi hai apni? Wo anime girl hai, andhi nahi! 😂",
            "Waifu ne bola: 'Tujhse accha toh 2D pixel hi reh lungi'. 💀",
            "Itna rejection toh Google AdSense bhi nahi deta jitna tumhe mila. 🤡",
            "Bhagwan ne dimaag bata toh tum line mein piche the, ab Waifu ke liye bhi piche hi raho.",
            "Beta tumse na ho payega, jaao jaake POGO dekho! 📺"
        ]
        roast = random.choice(local_roasts)
        fail_gifs = ["https://media.giphy.com/media/pSpmPXdHQWZrcuJRq3/giphy.gif"]

        await update.message.reply_animation(
            random.choice(fail_gifs),
            caption=f"💔 <b>REJECTED!</b>\n\n🗣️ <i>{stylize_text(roast)}</i>",
            parse_mode=ParseMode.HTML
        )

# --- WMARRY (STAYS SAME) ---
async def wmarry(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = ensure_user_exists(update.effective_user)
    last = user.get("last_wmarry")
    
    if last and (datetime.utcnow() - last) < timedelta(hours=2):
        return await update.message.reply_text(f"⏳ <b>Cooldown!</b> 2 ghante wait karo.", parse_mode=ParseMode.HTML)

    try:
        async with httpx.AsyncClient() as client:
            r = await client.get("https://api.waifu.pics/sfw/waifu")
            url = r.json()['url']

        waifu_data = {"name": "Random Waifu", "rarity": "Rare", "date": datetime.utcnow()}
        users_collection.update_one({"user_id": user['user_id']}, {"$push": {"waifus": waifu_data}, "$set": {"last_wmarry": datetime.utcnow()}})

        await update.message.reply_photo(url, caption="💍 <b>Married!</b>\nAdded <b>Rare Waifu</b> to collection.", parse_mode=ParseMode.HTML)
    except:
        await update.message.reply_text("❌ API Error! Try again later.")
