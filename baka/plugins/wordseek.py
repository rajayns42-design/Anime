import random
import random
from datetime import datetime, timedelta
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes, CommandHandler, MessageHandler, filters

from baka.database import (
    ws_start_game, ws_get_game, ws_update_board, 
    ws_end_game, ws_add_win, ws_get_leaderboard,
    ws_update_hints, can_user_get_hint
)

# Word List
WORDS = ["APPLE", "HEART", "SMILE", "TIGER", "QUEEN", "ANGEL", "DREAM", "LIGHT", "WORLD", "BRUSH"]

# ================= START =================
async def start_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    if chat.type == "private":
        return await update.message.reply_text("❌ Groups mein khelo!")

    # Check agar game already chal raha ho
    if ws_get_game(chat.id):
        return await update.message.reply_text("⚠️ Ek game pehle se chal raha hai!")

    word = random.choice(WORDS)
    ws_start_game(chat.id, word) # DB mein game set (Timer logic removed)

    # Screenshot jaisa header
    await update.message.reply_text("WordSeek\nGame started! Guess the 5 letter word!")


# ================= GUESS LOGIC (Fixed & Clean) =================
async def guess(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    
    # Message filter: Sirf 5 letters and no commands
    text = update.message.text.upper().strip()
    if len(text) != 5 or not text.isalpha() or update.message.text.startswith('/'):
        return

    # Database se active game check karo
    game = ws_get_game(chat.id)
    if not game or not game.get("active"):
        return

    word = game["word"]
    board = game.get("board", [])

    # Wordle matching logic (🟩, 🟨, 🟥)
    row = ""
    for i in range(5):
        if text[i] == word[i]:
            row += "🟩"
        elif text[i] in word:
            row += "🟨"
        else:
            row += "🟥"

    # UI Update: Screenshot jaisa format
    board.append(f"{row} **{text}**")
    ws_update_board(chat.id, board)
    
    board_text = "WordSeek\n" + "\n".join(board)

    # WIN CHECK
    if text == word:
        ws_end_game(chat.id) # Game khatam (Winner mil gaya)
        ws_add_win(chat.id, user.id, user.first_name) # Win count add
        
        await update.message.reply_text(
            f"{board_text}\n\n🎉 **{user.first_name} WON!**", 
            parse_mode=ParseMode.MARKDOWN
        )
    else:
        # Pura board dikhao har guess pe
        await update.message.reply_text(board_text, parse_mode=ParseMode.MARKDOWN)


# ================= HINT SYSTEM (1 Week - 2 Limit) =================
async def get_hint(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    game = ws_get_game(chat.id)

    if not game or not game.get("active"):
        return await update.message.reply_text("❌ Abhi koi game active nahi hai.")

    # Weekly Quota Check
    can_get, oldest_hint = can_user_get_hint(chat.id, user.id)
    if not can_get:
        available_at = oldest_hint + timedelta(weeks=1)
        wait = available_at - datetime.now()
        return await update.message.reply_text(
            f"🚫 **Limit Reached!**\nAgla hint `{wait.days}d {wait.seconds//3600}h` baad milega."
        )

    word = game["word"]
    revealed = game.get("revealed_indices", [])

    if len(revealed) >= 3:
        return await update.message.reply_text("Is game ke hints khatam! 🛑")

    idx = random.choice([i for i in range(5) if i not in revealed])
    revealed.append(idx)
    ws_update_hints(chat.id, revealed)

    hint_view = " ".join([word[i] if i in revealed else "_" for i in range(5)])
    await update.message.reply_text(f"💡 Hint: `{hint_view}`", parse_mode=ParseMode.MARKDOWN)


# ================= LEADERBOARD =================
async def leaderboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lb = ws_get_leaderboard(chat.id)
    if not lb:
        return await update.message.reply_text("😅 Abhi tak koi nahi jeeta.")

    sorted_lb = sorted(lb.items(), key=lambda x: x[1].get('wins', 0), reverse=True)
    text = "🏆 **WordSeek Leaderboard**\n\n"
    
    for i, (uid, data) in enumerate(sorted_lb[:10], 1):
        name = data.get('name', 'User')
        wins = data.get('wins', 0)
        text += f"{i}. {name} — **{wins}** wins\n"
    
    await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)


# ================= SETUP =================
def setup(app):
    app.add_handler(CommandHandler("word", start_game))
    app.add_handler(CommandHandler("hint", get_hint))
    app.add_handler(CommandHandler("leaderboard", leaderboard))
    # Guess logic group 0 mein rakha hai for high priority
    app.add_handler(MessageHandler(filters.TEXT & filters.ChatType.GROUPS & ~filters.COMMAND, guess), group=0)
