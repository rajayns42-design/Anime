# Copyright (c) 2026 Telegram:- @WTF_Phantom <DevixOP>
# Advanced Profile Matching with Deep Links

import random
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode

async def couple_roll(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.effective_message
    user1 = update.effective_user # Command dene wala
    
    # 1. Partner Dhundna (Reply se ya Mention se)
    if msg.reply_to_message:
        user2 = msg.reply_to_message.from_user
    elif context.args:
        # Agar kisi ko tag kiya hai
        user2_text = context.args[0]
        # Hum user2 ka data text se handle karenge
        user2 = None 
    else:
        return await msg.reply_text("<b>Abe akele jodi banaoge?</b> 😂\nKisi ke message pe <code>/couple</code> reply karo!", parse_mode=ParseMode.HTML)

    # 2. Percentage aur Bar Logic
    perc = random.randint(1, 100)
    filled = int(perc / 10)
    bar = "❤️" * filled + "🖤" * (10 - filled)

    # 3. Dynamic Comments
    if perc > 90: status = "Soulmates! ❤️✨"
    elif perc > 70: status = "Hot Couple! 🔥"
    elif perc > 50: status = "Cute Together 🌸"
    else: status = "Bas Timepass 😂"

    # 4. Profile Card Design (Dono ki profile link ke saath)
    if msg.reply_to_message:
        u2_link = f"<a href='tg://user?id={user2.id}'>{user2.first_name}</a>"
    else:
        u2_link = f"<b>{context.args[0]}</b>"

    response = (
        f"<b>┏━━━━━━ 💞 JODI REPORT 💞 ━━━━━━┓</b>\n"
        f"<b>┃</b>\n"
        f"<b>┃ 🤵 BOY:</b> <a href='tg://user?id={user1.id}'>{user1.first_name}</a>\n"
        f"<b>┃ 👰 GIRL:</b> {u2_link}\n"
        f"<b>┃</b>\n"
        f"<b>┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛</b>\n"
        f"<b>┃ 📊 MATCH:</b> <code>{perc}%</code>\n"
        f"<b>┃ ⚡ STATUS:</b> <code>{status}</code>\n"
        f"<b>┃ 🛠 METER:</b> <code>{bar}</code>\n"
        f"<b>┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓</b>\n\n"
        f"<i>Kyu {user1.first_name} bhai, shadi kab hai fir? 🥂</i>"
    )

    await msg.reply_text(response, parse_mode=ParseMode.HTML)
