# Copyright (c) 2026 Telegram:- @WTF_Phantom <DevixOP>
# Love Percentage Matching Plugin - FULL FIXED

import random
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from telegram.constants import ParseMode

async def love_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Calculates love percentage between two people"""
    msg = update.effective_message
    
    # 1. Input Check [cite: 2026-02-21]
    if not context.args:
        return await msg.reply_text(
            "<b>❌ 𝐁𝐚𝐤𝐚! 𝐏𝐥𝐞𝐚𝐬𝐞 𝐩𝐫𝐨𝐯𝐢𝐝𝐞 𝐚 𝐧𝐚𝐦𝐞.</b>\n"
            "𝐄𝐱𝐚𝐦𝐩𝐥𝐞: <code>/love @username</code>",
            parse_mode=ParseMode.HTML
        )

    partner_name = " ".join(context.args)
    user_name = update.effective_user.first_name
    
    # 2. Unlimited Random Logic [cite: 2026-02-21]
    percentage = random.randint(1, 100)
    
    # 3. Dynamic Results [cite: 2026-02-21]
    if percentage > 90:
        comment = "𝐌𝐚𝐬𝐡𝐚𝐥𝐥𝐚𝐡! 𝐘𝐞 𝐭𝐨𝐡 𝐑𝐚𝐛 𝐧𝐞 𝐛𝐚𝐧𝐚 𝐝𝐢 𝐣𝐨𝐝𝐢 𝐡𝐚𝐢. ❤️✨"
    elif percentage > 75:
        comment = "𝐒𝐚𝐜𝐡𝐚 𝐩𝐲𝐚𝐫 𝐡𝐚𝐢 𝐛𝐡𝐚𝐢, 𝐬𝐡𝐚𝐚𝐝𝐢 𝐩𝐚𝐤𝐤𝐢 𝐬𝐚𝐦𝐣𝐡𝐨! 💍🌸"
    elif percentage > 50:
        comment = "𝐓𝐡𝐨𝐝𝐚 𝐞𝐟𝐟𝐨𝐫𝐭 𝐝𝐚𝐥𝐨 𝐭𝐨𝐡 𝐛𝐚𝐚𝐭 𝐛𝐚𝐧 𝐣𝐚𝐲𝐞𝐠𝐢. 😉"
    elif percentage > 25:
        comment = "𝐁𝐚𝐬 𝐭𝐡𝐢𝐤-𝐭𝐡𝐚𝐤 𝐡𝐢 𝐡𝐚𝐢, 𝐳𝐲𝐚𝐝𝐚 𝐮𝐦𝐞𝐞𝐝 𝐦𝐚𝐭 𝐫𝐚𝐤𝐡𝐨. 🙄"
    else:
        comment = "𝐁𝐞𝐭𝐚, 𝐭𝐮𝐦𝐬𝐞 𝐧𝐚 𝐡𝐨 𝐩𝐚𝐲𝐞𝐠𝐚. 𝐊𝐚𝐭𝐧𝐞 𝐰𝐚𝐥𝐚 𝐡𝐚𝐢 𝐭𝐮𝐦𝐡𝐚𝐫𝐚! 😂🤡"

    # 4. Aesthetic Response UI [cite: 2026-02-21]
    response = (
        f"<b>❤️ <u>𝐋𝐎𝐕𝐄 𝐌𝐀𝐓𝐂𝐇𝐈𝐍𝐆</u> ❤️</b>\n"
        f"━━━━━━━━━━━━━━━\n"
        f"<b>👤 𝐘𝐨𝐮:</b> {user_name}\n"
        f"<b>👤 𝐏𝐚𝐫𝐭𝐧𝐞𝐫:</b> {partner_name}\n\n"
        f"<b>📊 𝐏𝐞𝐫𝐜𝐞𝐧𝐭𝐚𝐠𝐞:</b> {percentage}%\n"
        f"<b>📝 𝐑𝐞𝐬𝐮𝐥𝐭:</b> {comment}\n"
        f"━━━━━━━━━━━━━━━"
    )

    # 5. Help Button Integration [cite: 2026-02-21]
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🆘 𝐇𝐄𝐋𝐏", callback_data="help_main")]
    ])

    await msg.reply_text(response, parse_mode=ParseMode.HTML, reply_markup=keyboard)
