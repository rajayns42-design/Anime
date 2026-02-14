# Copyright (c) 2026 Telegram:- @WTF_Phantom <DevixOP>
# Edited for Malik: ZEXX (Invisible 1m Timer)

import random
from datetime import datetime, timedelta
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes, filters

from baka.database import (
    ws_start_game, ws_get_game, ws_update_board, 
    ws_end_game, ws_add_win, ws_get_leaderboard,
    ws_update_hints, can_user_get_hint
)

WORDS = ["APPLE", "HEART", "SMILE", "TIGER", "QUEEN", "ANGEL", "DREAM", "LIGHT", "WORLD", "BRUSH", "CANDY", "GHOST", "PIZZA", "STORM", "WATER"]

# --- ⏰ BACKGROUND AUTO-END (KISI KO DIKHEGA NAHI) ---
async def auto_end_game(context: ContextTypes.DEFAULT_TYPE):
    job = context.job
    chat_id = job.chat_id
    game = ws_get_game(chat_id)
    
    if game and game.get("active"):
        word = game["word"]
        ws_end_game(chat_id)
        # Time khatam hone par hi message aayega
        await context.bot.send_message(
            chat_id=chat_id,
            text=f"⌛ <b>Time's Up!</b>\n\nKoi bhi 1 minute mein guess nahi kar paya.\n🔑 Sahi word tha: <b>{word}</b>\n\nAb naya game shuru karne ke liye <b>/word</b> likhein!",
            parse_mode=ParseMode.HTML
        )

# ================= START =================
async def start_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    if chat.type == "private":
        return await update.message.reply_text("❌ Groups mein khelo!")

    if ws_get_game(chat.id):
        return await update.message.reply_text("⚠️ Ek game pehle se chal raha hai!")

    word = random.choice(WORDS)
    ws_start_game(chat.id, word) 

    # Background mein 60 seconds ka timer set (Display nahi hoga)
    context.job_queue.run_once(auto_end_game, 60, chat_id=chat.id, name=f"ws_{chat.id}")

    await update.message.reply_text(
        "🎮 <b>WordSeek</b>\nGame started! Guess the 5 letter word!\n<i>(Jaldi guess karein, time limited hai!)</i>", 
        parse_mode=ParseMode.HTML
    )

# ================= GUESS LOGIC (CLEAN) =================
async def guess(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    
    if not update.message or not update.message.text: return
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

    board.append(f"{row} {text}")
    ws_update_board(chat.id, board)
    
    board_text = "<b>WordSeek</b>\n" + "\n".join(board)

    if text == word:
        # Winner milte hi background timer ko cancel kar do
        current_jobs = context.job_queue.get_jobs_by_name(f"ws_{chat.id}")
        for job in current_jobs:
            job.schedule_removal()

        ws_end_game(chat.id)
        ws_add_win(chat.id, user.id, user.first_name)
        await update.message.reply_text(
            f"{board_text}\n\n🎉 <b>{user.first_name} WON!</b>\nNaya game shuru karne ke liye <b>/word</b> likhein!", 
            parse_mode=ParseMode.HTML
        )
    else:
        # Guess par koi mention nahi
        await context.bot.send_message(chat_id=chat.id, text=board_text, parse_mode=ParseMode.HTML)
