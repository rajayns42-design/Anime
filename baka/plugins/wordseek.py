# Copyright (c) 2026 Telegram:- @WTF_Phantom <DevixOP>
# Edited for Malik: ZEXX (Timar + Leaderboard)

import random
from datetime import datetime
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes, filters

from baka.database import (
    ws_start_game, ws_get_game, ws_update_board, 
    ws_end_game, ws_add_win, ws_get_leaderboard
)

WORDS = ["APPLE", "HEART", "SMILE", "TIGER", "QUEEN", "ANGEL", "DREAM", "LIGHT", "WORLD", "BRUSH", "CANDY", "GHOST", "PIZZA", "STORM", "WATER"]

# --- ⏰ BACKGROUND AUTO-END ---
async def auto_end_game(context: ContextTypes.DEFAULT_TYPE):
    job = context.job
    chat_id = job.chat_id
    game = ws_get_game(chat_id)
    
    if game and game.get("active"):
        word = game["word"]
        ws_end_game(chat_id)
        await context.bot.send_message(
            chat_id=chat_id,
            text=f"⌛ <b>Time's Up!</b>\n\nSahi word tha: <b>{word}</b>\nNaya game <b>/word</b> se shuru karein!",
            parse_mode=ParseMode.HTML
        )

# ================= START =================
async def start_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    if ws_get_game(chat.id):
        return await update.message.reply_text("⚠️  game All redy started!")

    word = random.choice(WORDS)
    ws_start_game(chat.id, word) 
    context.job_queue.run_once(auto_end_game, 60, chat_id=chat.id, name=f"ws_{chat.id}")
    await update.message.reply_text("🎮 <b>WordSeek Started!</b>\nGame started! Guess the 5 letter word!", parse_mode=ParseMode.HTML)

# ================= GUESS LOGIC =================
async def guess(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat, user = update.effective_chat, update.effective_user
    if not update.message or not update.message.text: return
    text = update.message.text.upper().strip()
    if len(text) != 5 or not text.isalpha() or text.startswith('/'): return

    game = ws_get_game(chat.id)
    if not game or not game.get("active"): return

    word, board = game["word"], game.get("board", [])
    row = "".join(["🟩" if text[i] == word[i] else "🟨" if text[i] in word else "🟥" for i in range(5)])
    board.append(f"{row} {text}")
    ws_update_board(chat.id, board)
    
    if text == word:
        # Timer stop aur winner update
        current_jobs = context.job_queue.get_jobs_by_name(f"ws_{chat.id}")
        for job in current_jobs: job.schedule_removal()
        ws_end_game(chat.id)
        ws_add_win(chat.id, user.id, user.first_name)
        await update.message.reply_text(f"🎉 <b>{user.first_name} WON!</b>\n\nWins update ho gayi hain. Check: /wlb", parse_mode=ParseMode.HTML)
    else:
        await context.bot.send_message(chat_id=chat.id, text="<b>WordSeek</b>\n" + "\n".join(board), parse_mode=ParseMode.HTML)

# ================= LEADERBOARD =================
async def leaderboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Database se top users fetch karega
    lb_data = ws_get_leaderboard(update.effective_chat.id)
    if not lb_data:
        return await update.message.reply_text("📉 Abhi tak koi winner nahi hai!")

    # Sorting wins ke hisaab se
    sorted_lb = sorted(lb_data.items(), key=lambda x: x[1].get('wins', 0), reverse=True)
    
    text = "🏆 <b>WordSeek Leaderboard</b>\n\n"
    for i, (uid, data) in enumerate(sorted_lb[:10], 1):
        emoji = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
        text += f"{emoji} {data.get('name')} — <b>{data.get('wins')}</b> wins\n"
    
    await update.message.reply_text(text, parse_mode=ParseMode.HTML)
