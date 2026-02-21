# Copyright (c) 2026 Telegram:- @WTF_Phantom <DevixOP>
# Edited for Malik: ZEXX (Fast Action Version - Fixed)

import random
from datetime import datetime, timedelta
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from baka.config import PROTECT_1D_COST, PROTECT_2D_COST, REVIVE_COST, OWNER_ID
from baka.utils import ensure_user_exists, resolve_target, get_active_protection, format_time, format_money, get_mention
from baka.database import users_collection

# Utility function to safely get first_name
def get_safe_name(user_obj):
    if isinstance(user_obj, dict):
        return user_obj.get('first_name', 'User')
    return getattr(user_obj, 'first_name', 'User')

# ================= ⚔️ KILL =================
async def kill(update: Update, context: ContextTypes.DEFAULT_TYPE):
    attacker = ensure_user_exists(update.effective_user)
    target, error = await resolve_target(update, context)

    if not target or target.get('user_id') == attacker.get('user_id'): return
    if target.get('user_id') == OWNER_ID or target.get('status') == 'dead' or attacker.get('status') == 'dead': return

    expiry = get_active_protection(target)
    if expiry: return await update.message.reply_text(f"🛡️ Protected!")

    final_reward = random.randint(100, 200)
    users_collection.update_one({"user_id": target["user_id"]}, {"$set": {"status": "dead", "death_time": datetime.utcnow()}})
    users_collection.update_one({"user_id": attacker["user_id"]}, {"$inc": {"kills": 1, "balance": final_reward}})

    # FIXED: KeyError 'first_name' removed using get_safe_name
    t_name = get_safe_name(target)
    await update.message.reply_text(
        f"👤 {get_mention(attacker)} killed <b>{t_name}</b>!\n💰 Earned: <code>{format_money(final_reward)}</code>", 
        parse_mode=ParseMode.HTML
    )

# ================= 💸 ROB =================
async def rob(update: Update, context: ContextTypes.DEFAULT_TYPE):
    attacker = ensure_user_exists(update.effective_user)
    target, _ = await resolve_target(update, context)

    if not target or target.get('user_id') == attacker.get('user_id'): return
    if target.get('user_id') == OWNER_ID or attacker.get('status') == 'dead' or target.get('balance', 0) <= 0: return

    # Fast Rob: 20% of target's balance
    amount = int(target.get('balance', 0) * 0.2)
    
    users_collection.update_one({"user_id": target["user_id"]}, {"$inc": {"balance": -amount}})
    users_collection.update_one({"user_id": attacker["user_id"]}, {"$inc": {"balance": amount}})

    t_name = get_safe_name(target)
    await update.message.reply_text(
        f"👤 {get_mention(attacker)} robbed <code>{format_money(amount)}</code> from <b>{t_name}</b>!", 
        parse_mode=ParseMode.HTML
    )

# ================= 🛡️ PROTECT =================
async def protect(update: Update, context: ContextTypes.DEFAULT_TYPE):
    sender = ensure_user_exists(update.effective_user)
    target, _ = await resolve_target(update, context)
    if not target: target = sender

    cost = PROTECT_1D_COST
    if sender.get('balance', 0) < cost: return

    expiry_dt = datetime.utcnow() + timedelta(days=1)
    users_collection.update_one({"user_id": sender["user_id"]}, {"$inc": {"balance": -cost}})
    users_collection.update_one({"user_id": target["user_id"]}, {"$set": {"protection_expiry": expiry_dt}})

    await update.message.reply_text(f"🛡️ Shield Active for {get_mention(target)}!")

# ================= 💉 REVIVE =================
async def revive(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reviver = ensure_user_exists(update.effective_user)
    target, _ = await resolve_target(update, context)
    if not target: target = reviver

    if target.get('status') == 'alive' or reviver.get('balance', 0) < REVIVE_COST: return

    users_collection.update_one({"user_id": reviver["user_id"]}, {"$inc": {"balance": -REVIVE_COST}})
    users_collection.update_one({"user_id": target["user_id"]}, {"$set": {"status": "alive", "death_time": None}})
    await update.message.reply_text(f"💖 {get_mention(target)} Revived!")
