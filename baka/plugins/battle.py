# Copyright (c) 2026 Telegram:- @WTF_Phantom <DevixOP>
# Battle Arena & Global Leaderboard - Full Integrated Version

import random
import asyncio
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from baka.utils import (
    ensure_user_exists, get_mention, 
    format_money, stylize_text
)
from baka.database import users_collection

# --- ⚔️ UNLIMITED BATTLE SYSTEM ---
async def battle_system(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    
    if not update.message.reply_to_message:
        return await update.message.reply_text(
            "<b>❌ 𝐀𝐧𝐠𝐞𝐥! 𝐑𝐞𝐩𝐥𝐲 𝐭𝐨 𝐚 𝐮𝐬𝐞𝐫 𝐭𝐨 𝐜𝐡𝐚𝐥𝐥𝐞𝐧𝐠𝐞 𝐭𝐡𝐞𝐦.</b>",
            parse_mode=ParseMode.HTML
        )

    target = update.message.reply_to_message.from_user
    if target.id == user.id or target.is_bot:
        return await update.message.reply_text("<b>⚠️ 𝐈𝐧𝐯𝐚𝐥𝐢𝐝 𝐓𝐚𝐫𝐠𝐞𝐭! 𝐅𝐢𝐠𝐡𝐭 𝐚 𝐫𝐞𝐚𝐥 𝐩𝐥𝐚𝐲𝐞𝐫.</b>", parse_mode=ParseMode.HTML)

    ensure_user_exists(user)
    ensure_user_exists(target)

    u_pwr, t_pwr = random.randint(10, 100), random.randint(10, 100)
    reward = random.randint(2500, 8000)

    msg = await update.message.reply_text(f"⚔️ <b>{user.first_name}</b> 𝐕𝐒 <b>{target.first_name}</b>\n🔥 <i>𝐅𝐢𝐠𝐡𝐭𝐢𝐧𝐠...</i>", parse_mode=ParseMode.HTML)
    await asyncio.sleep(2)

    if u_pwr > t_pwr:
        winner, loser = user, target
        users_collection.update_one({"user_id": user.id}, {"$inc": {"balance": reward, "wins": 1}})
        users_collection.update_one({"user_id": target.id}, {"$inc": {"losses": 1}})
        res = f"🏆 <b>𝐖𝐈𝐍𝐍𝐄𝐑:</b> {get_mention(user)}\n💰 <b>𝐋𝐎𝐎𝐓:</b> <code>{format_money(reward)}</code>"
    elif t_pwr > u_pwr:
        winner, loser = target, user
        users_collection.update_one({"user_id": target.id}, {"$inc": {"balance": reward, "wins": 1}})
        users_collection.update_one({"user_id": user.id}, {"$inc": {"losses": 1}})
        res = f"🏆 <b>𝐖𝐈𝐍𝐍𝐄𝐑:</b> {get_mention(target)}\n💰 <b>𝐋𝐎𝐎𝐓:</b> <code>{format_money(reward)}</code>"
    else:
        return await msg.edit_text("🤝 <b>𝐃𝐑𝐀𝐖! 𝐍𝐨 𝐨𝐧𝐞 𝐰𝐨𝐧.</b>", parse_mode=ParseMode.HTML)

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔄 𝐁𝐚𝐭𝐭𝐥𝐞 𝐀𝐠𝐚𝐢𝐧", callback_data="cb_battle_retry")],
        [InlineKeyboardButton("🆘 𝐇𝐄𝐋𝐏", callback_data="help_main")]
    ])

    await msg.edit_text(f"⚔️ <b><u>𝐁𝐀𝐓𝐓𝐋𝐄 𝐑𝐄𝐒𝐔𝐋𝐓</u></b> ⚔️\n\n{res}\n━━━━━━━━━━━━━━\n🆘 <i>𝐂𝐥𝐢𝐜𝐤 𝐇𝐞𝐥𝐩 𝐟𝐨𝐫 𝐦𝐨𝐫𝐞 𝐢𝐧𝐟𝐨!</i>", parse_mode=ParseMode.HTML, reply_markup=keyboard)

# --- 🏆 GLOBAL LEADERBOARD ---
async def battle_leaderboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Fetching top 10 by balance or wins
    top_list = users_collection.find().sort("balance", -1).limit(10)
    
    lb_text = "🏆 <b><u>𝐁𝐀𝐓𝐓𝐋𝐄 𝐋𝐄𝐀𝐃𝐄𝐑𝐁𝐎𝐀𝐑𝐃</u></b> 🏆\n━━━━━━━━━━━━━━\n"
    for i, doc in enumerate(top_list, 1):
        medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"<b>{i}.</b>"
        lb_text += f"{medal} {doc.get('name', 'User')} — <code>{format_money(doc.get('balance', 0))}</code>\n"
    
    lb_text += "━━━━━━━━━━━━━━\n🔥 <i>𝐁𝐞𝐜𝐨𝐦𝐞 𝐚 𝐋𝐞𝐠𝐞𝐧𝐝!</i>"
    
    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🆘 𝐇𝐄𝐋𝐏", callback_data="help_main")]])
    await update.message.reply_text(lb_text, parse_mode=ParseMode.HTML, reply_markup=keyboard)
