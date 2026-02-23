# Copyright (c) 2026 Telegram:- @WTF_Phantom <DevixOP>
# Fast Action Version with Inline Buttons - ZEXX

import random
from datetime import datetime, timedelta
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from baka.config import PROTECT_1D_COST, REVIVE_COST, OWNER_ID
from baka.utils import ensure_user_exists, resolve_target, get_active_protection, format_money, get_mention
from baka.database import users_collection

# Help Button Utility
def get_help_btn():
    return InlineKeyboardMarkup([[InlineKeyboardButton("🆘 Hᴇʟᴩ Mᴇɴᴜ", callback_data="help_menu")]])

# Safe Name Helper
def get_safe_name(user_obj):
    if isinstance(user_obj, dict):
        return user_obj.get('first_name', 'User')
    return getattr(user_obj, 'first_name', 'User')

# ================= ⚔️ KILL =================
async def kill(update: Update, context: ContextTypes.DEFAULT_TYPE):
    attacker = ensure_user_exists(update.effective_user)
    target, _ = await resolve_target(update, context)

    if not target:
        return await update.message.reply_text("⚠️ Reply to someone to kill them!", reply_markup=get_help_btn())
    
    if target.get('user_id') == attacker.get('user_id'): return
    if target.get('user_id') == OWNER_ID: return await update.message.reply_text("❌ You cannot kill God!")
    if target.get('status') == 'dead': return await update.message.reply_text("💀 Target is already dead!")
    if attacker.get('status') == 'dead': return await update.message.reply_text("👻 Ghosts can't kill!")

    if get_active_protection(target):
        return await update.message.reply_text(f"🛡️ <b>{get_safe_name(target)}</b> is under protection!", parse_mode=ParseMode.HTML)

    reward = random.randint(200, 500)
    users_collection.update_one({"user_id": target["user_id"]}, {"$set": {"status": "dead", "death_time": datetime.utcnow()}})
    users_collection.update_one({"user_id": attacker["user_id"]}, {"$inc": {"kills": 1, "balance": reward}})

    await update.message.reply_text(
        f"⚔️ {get_mention(attacker)} ᴋɪʟʟᴇᴅ <b>{get_safe_name(target)}</b>!\n💰 ᴇᴀʀɴᴇᴅ: <code>{format_money(reward)}</code>",
        parse_mode=ParseMode.HTML,
        reply_markup=get_help_btn()
    )

# ================= 💸 ROB =================
async def rob(update: Update, context: ContextTypes.DEFAULT_TYPE):
    attacker = ensure_user_exists(update.effective_user)
    target, _ = await resolve_target(update, context)

    if not target:
        return await update.message.reply_text("⚠️ Reply to someone to rob them!", reply_markup=get_help_btn())
    
    if target.get('balance', 0) < 100:
        return await update.message.reply_text("🪙 Target is too poor to rob!")

    # 25% Instant Rob
    amount = int(target.get('balance', 0) * 0.25)
    users_collection.update_one({"user_id": target["user_id"]}, {"$inc": {"balance": -amount}})
    users_collection.update_one({"user_id": attacker["user_id"]}, {"$inc": {"balance": amount}})

    await update.message.reply_text(
        f"💸 {get_mention(attacker)} ʀᴏʙʙᴇᴅ <code>{format_money(amount)}</code> ғʀᴏᴍ <b>{get_safe_name(target)}</b>!",
        parse_mode=ParseMode.HTML,
        reply_markup=get_help_btn()
    )

# ================= 🛡️ PROTECT =================
async def protect(update: Update, context: ContextTypes.DEFAULT_TYPE):
    sender = ensure_user_exists(update.effective_user)
    if sender.get('balance', 0) < PROTECT_1D_COST:
        return await update.message.reply_text(f"❌ Need {format_money(PROTECT_1D_COST)} for a Shield!")

    expiry_dt = datetime.utcnow() + timedelta(days=1)
    users_collection.update_one({"user_id": sender["user_id"]}, {"$inc": {"balance": -PROTECT_1D_COST}, "$set": {"protection_expiry": expiry_dt}})

    await update.message.reply_text(
        f"🛡️ ꜱʜɪᴇʟᴅ ᴀᴄᴛɪᴠᴀᴛᴇᴅ ғᴏʀ 24 ʜᴏᴜʀꜱ!",
        reply_markup=get_help_btn()
    )

# ================= 💉 REVIVE =================
async def revive(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = ensure_user_exists(update.effective_user)
    target, _ = await resolve_target(update, context)
    if not target: target = user

    if target.get('status') != 'dead':
        return await update.message.reply_text("💉 User is already alive!")

    if user.get('balance', 0) < REVIVE_COST:
        return await update.message.reply_text(f"❌ Need {format_money(REVIVE_COST)} to Revive!")

    users_collection.update_one({"user_id": user["user_id"]}, {"$inc": {"balance": -REVIVE_COST}})
    users_collection.update_one({"user_id": target["user_id"]}, {"$set": {"status": "alive", "death_time": None}})
    
    await update.message.reply_text(
        f"💖 {get_mention(target)} ʜᴀꜱ ʙᴇᴇɴ ʀᴇᴠɪᴠᴇᴅ!",
        reply_markup=get_help_btn()
    )
