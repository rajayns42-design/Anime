# Copyright (c) 2026 Telegram:- @WTF_Phantom <DevixOP>
# Love Percentage Matching Plugin

import random
from telegram import Update
from telegram.ext import ContextTypes

async def love_match(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Calculates love percentage between two people"""
    msg = update.effective_message
    
    # Check if user provided a name
    if not context.args:
        return await msg.reply_text("Babu, kiske saath matching check karni hai? Naam toh likho! 😂\nExample: `/love @username` ya `/love Neha`")

    partner_name = " ".join(context.args)
    user_name = update.effective_user.first_name
    
    # Generate a random percentage
    percentage = random.randint(1, 100)
    
    # Result messages based on percentage
    if percentage > 90:
        comment = "Mashallah! Ye toh Rab ne bana di jodi hai. ❤️✨"
    elif percentage > 75:
        comment = "Sacha pyar hai bhai, shaadi pakki samjho! 💍🌸"
    elif percentage > 50:
        comment = "Thoda effort dalo toh baat ban jayegi. 😉"
    elif percentage > 25:
        comment = "Bas thik-thak hi hai, zyada umeed mat rakho. 🙄"
    else:
        comment = "Beta, tumse na ho payega. Katne wala hai tumhara! 😂🤡"

    response = (
        f"<b>❤️ LOVE MATCHING ❤️</b>\n\n"
        f"<b>👤 You:</b> {user_name}\n"
        f"<b>👤 Partner:</b> {partner_name}\n\n"
        f"<b>📊 Percentage:</b> {percentage}%\n"
        f"<b>📝 Result:</b> {comment}"
    )

    await msg.reply_text(response, parse_mode="HTML")
