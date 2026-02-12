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

WORDS = ["APPLE", "HEART", "SMILE", "TIGER", "QUEEN", "ANGEL", "DREAM", "LIGHT", "WORLD", "BRUSH"]

# ================= START =================
async def start_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    if chat.type == "private":
        return await update.message.reply_text("❌ Groups mein khelo!")

    if ws_get_game(chat.id):
        return await update.message.reply_text("⚠️ Ek game pehle se chal raha hai!")

    word = random.choice(WORDS)
    ws_start_game(chat.id, word) 

    await update.message.reply_text("WordSeek\nGame started! Guess the 5 letter word!")

# ================= GUESS LOGIC (Clean - No Mention) =================
async def guess(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    text = update.message.text.upper().strip()

    if len(text) != 5 or not text.isalpha() or update.message.text.startswith('/'):
        return

    game = ws_get_game(chat.id)
    if not game or not game.get("active"):
        return

    word = game["word"]
    board = game.get("board", [])

    row = ""
    for i in range(5):
        if text[i] == word[i]: row += "🟩"
        elif text[i] in word: row += "🟨"
        else: row += "🟥"

    # Board update (No mention here)
    board.append(f"{row} **{text}**")
    ws_update_board(chat.id, board)
    
    board_text = "WordSeek\n" + "\n".join(board)

    if text == word:
        ws_end_game(chat.id)
        ws_add_win(chat.id, user.id, user.first_name)
        # Winner ke waqt mention ya naam dikhayega
        await update.message.reply_text(
            f"{board_text}\n\n🎉 **{user.first_name} WON!**", 
            parse_mode=ParseMode.MARKDOWN
        )
    else:
        # Normal guess par sirf board dikhayega, bina mention ke
        await update.message.reply_text(board_text, parse_mode=ParseMode.MARKDOWN)

# ================= HINT & LEADERBOARD =================
async def get_hint(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    game = ws_get_game(chat.id)
    if not game or not game.get("active"): return

    can_get, oldest_hint = can_user_get_hint(chat.id, user.id)
    if not can_get:
        wait = (oldest_hint + timedelta(weeks=1)) - datetime.now()
        return await update.message.reply_text(f"🚫 Limit Reached! Wait {wait.days}d {wait.seconds//3600}h")

    word = game["word"]
    revealed = game.get("revealed_indices", [])
    if len(revealed) >= 3: return await update.message.reply_text("Hints khatam! 🛑")

    idx = random.choice([i for i in range(5) if i not in revealed])
    revealed.append(idx)
    ws_update_hints(chat.id, revealed)
    hint_view = " ".join([word[i] if i in revealed else "_" for i in range(5)])
    await update.message.reply_text(f"💡 Hint: `{hint_view}`", parse_mode=ParseMode.MARKDOWN)

async def leaderboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lb = ws_get_leaderboard(update.effective_chat.id)
    if not lb: return await update.message.reply_text("Khali hai! 😅")
    sorted_lb = sorted(lb.items(), key=lambda x: x[1].get('wins', 0), reverse=True)
    text = "🏆 **WordSeek Leaderboard**\n\n"
    for i, (uid, data) in enumerate(sorted_lb[:10], 1):
        text += f"{i}. {data.get('name')} — **{wins}** wins\n"
    await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)

def setup(app):
    app.add_handler(CommandHandler("word", start_game))
    app.add_handler(CommandHandler("hint", get_hint))
    app.add_handler(CommandHandler("leaderboard", leaderboard))
    app.add_handler(MessageHandler(filters.TEXT & filters.ChatType.GROUPS & ~filters.COMMAND, guess), group=0)
