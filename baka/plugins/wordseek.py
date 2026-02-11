import random
import asyncio
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
        return await update.message.reply_text("⚠️ Game already chal raha hai!")

    word = random.choice(WORDS)
    ws_start_game(chat.id, word, []) 
    
    await update.message.reply_text(
        f"🎯 **WordSeek Start!**\n📝 5 Letters ka word guess karo.\n"
        f"💡 `/hint` (Hafte mein sirf 2 baar milega!)\n⏳ 60 Seconds!",
        parse_mode=ParseMode.MARKDOWN
    )
    context.application.create_task(timer(chat.id, word, context))

# ================= HINT (Weekly Limit: 2) =================
async def get_hint(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    game = ws_get_game(chat.id)

    if not game or not game.get("active"):
        return await update.message.reply_text("❌ Abhi koi game active nahi hai.")

    # 🛑 Weekly Cooldown Check
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
        return await update.message.reply_text("Game ke saare hints khatam! 🛑")

    idx = random.choice([i for i in range(5) if i not in revealed])
    revealed.append(idx)
    ws_update_hints(chat.id, revealed)

    hint_view = " ".join([word[i] if i in revealed else "_" for i in range(5)])
    await update.message.reply_text(f"💡 **Hint:** `{hint_view}`", parse_mode=ParseMode.MARKDOWN)

# ================= GUESS LOGIC =================
async def guess(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    text = update.message.text.upper().strip()

    if len(text) != 5 or not text.isalpha() or text.startswith('/'):
        return

    game = ws_get_game(chat.id)
    if not game or not game.get("active"):
        return

    word = game["word"]
    board = game.get("board", [])

    # Row logic
    row = ""
    for i in range(5):
        if text[i] == word[i]: row += "🟩"
        elif text[i] in word: row += "🟨"
        else: row += "🟥"

    board.append(f"{row} `{text}`")
    ws_update_board(chat.id, board)
    board_text = "\n".join(board)

    if text == word:
        ws_end_game(chat.id)
        ws_add_win(chat.id, user.id, user.first_name)
        await update.message.reply_text(f"🎉 **{user.first_name} Won!**\n\n{board_text}", parse_mode=ParseMode.MARKDOWN)
    else:
        await update.message.reply_text(board_text, parse_mode=ParseMode.MARKDOWN)

# ================= TIMER & LB =================
async def timer(chat_id, target_word, context):
    await asyncio.sleep(60)
    game = ws_get_game(chat_id)
    if game and game.get("active") and game["word"] == target_word:
        ws_end_game(chat_id)
        await context.bot.send_message(chat_id, f"⏰ **Time Over!**\nWord tha: `{target_word}`")

async def leaderboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lb = ws_get_leaderboard(chat.id)
    if not lb: return await update.message.reply_text("Khali hai! 😅")
    
    # Sort and display
    sorted_lb = sorted(lb.items(), key=lambda x: x[1].get('wins', 0), reverse=True)
    text = "🏆 **Leaderboard**\n\n"
    for i, (uid, data) in enumerate(sorted_lb[:10], 1):
        text += f"{i}. {data.get('name')} — {data.get('wins')} wins\n"
    await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)

def setup(app):
    app.add_handler(CommandHandler("word", start_game))
    app.add_handler(CommandHandler("hint", get_hint))
    app.add_handler(CommandHandler("leaderboard", leaderboard))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, guess), group=2)
