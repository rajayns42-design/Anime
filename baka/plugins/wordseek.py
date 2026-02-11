import random
import asyncio
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode

# Words list (5 letters only)
WORDS = ["APPLE", "HEART", "SMILE", "TIGER", "QUEEN", "ANGEL", "DREAM", "LIGHT", "WORLD", "BRUSH"]

# Temporary memory for active games
group_games = {}

async def start_wordle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    if chat.type == "private":
        return await update.message.reply_text("❌ Ye game sirf groups mein chalta hai!")

    if chat.id in group_games:
        return await update.message.reply_text("⚠️ Game pehle se hi chal raha hai!")

    await send_new_wordle(chat.id, context)

async def send_new_wordle(chat_id, context):
    word = random.choice(WORDS).upper()
    group_games[chat_id] = {
        "word": word,
        "board": [],
        "active": True
    }
    
    await context.bot.send_message(
        chat_id, 
        "🎯 **Wordle Shuru!**\n5 letters ka sahi word dhoondo.\nUnlimited mode ON hai!",
        parse_mode=ParseMode.MARKDOWN
    )

async def wordle_guess(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    text = update.message.text.upper()

    if chat.id not in group_games or len(text) != 5 or not text.isalpha():
        return

    game = group_games[chat.id]
    word = game["word"]
    row = ""

    # Logic: 🟩 Sahi jagah, 🟨 Galat jagah par hai, 🟥 Word mein nahi hai
    for i in range(5):
        if text[i] == word[i]:
            row += "🟩"
        elif text[i] in word:
            row += "🟨"
        else:
            row += "🟥"

    game["board"].append(f"{row} `{text}`")
    board_status = "\n".join(game["board"])

    # --- WIN LOGIC ---
    if text == word:
        # Reward Logic (Baka style database)
        ensure_user_exists(user) # User check
        reward = 1000
        users_collection.update_one({"user_id": user.id}, {"$inc": {"balance": reward, "wordle_wins": 1}})
        
        await update.message.reply_text(
            f"{board_status}\n\n"
            f"🎉 **{user.first_name} ne Jeet liya!**\n"
            f"💰 Inaam: {format_money(reward)}\n"
            f"Agla word aa raha hai..."
        )
        
        # Game reset for unlimited loop
        del group_games[chat.id]
        await asyncio.sleep(2)
        await send_new_wordle(chat.id, context)
    else:
        # Status update (Only if not won)
        await update.message.reply_text(board_status, parse_mode=ParseMode.MARKDOWN)

async def stop_wordle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if chat_id in group_games:
        del group_games[chat_id]
        await update.message.reply_text("🛑 Game rok diya gaya.")
