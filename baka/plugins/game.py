import random
from datetime import datetime, timedelta
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from baka.config import PROTECT_1D_COST, PROTECT_2D_COST, REVIVE_COST, OWNER_ID
from baka.utils import ensure_user_exists, resolve_target, get_active_protection, format_time, format_money, get_mention
from baka.database import users_collection

# =====================================
# ⚔️ KILL COMMAND
# =====================================
async def kill(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message: return
    attacker = ensure_user_exists(update.effective_user)
    target, error = await resolve_target(update, context)

    if not target: 
        return await update.message.reply_text("⚠️ <b>Usage:</b> <code>/kill @user</code>", parse_mode=ParseMode.HTML)

    # 1-Click Fast Validation
    if target['user_id'] == attacker['user_id']:
        return await update.message.reply_text("🤡 <b>Khud ko nahi maar sakte!</b>", parse_mode=ParseMode.HTML)
    if target.get('is_bot') or target['user_id'] == OWNER_ID:
        return await update.message.reply_text("🛡️ <b>Protected!</b>", parse_mode=ParseMode.HTML)
    if attacker['status'] == 'dead': 
        return await update.message.reply_text("💀 <b>You are dead.</b>", parse_mode=ParseMode.HTML)
    if target['status'] == 'dead': 
        return await update.message.reply_text("⚰️ <b>Already dead.</b>", parse_mode=ParseMode.HTML)

    expiry = get_active_protection(target)
    if expiry:
        rem = expiry - datetime.utcnow()
        return await update.message.reply_text(f"🛡️ Safe for <code>{format_time(rem)}</code>.", parse_mode=ParseMode.HTML)

    final_reward = random.randint(100, 200)
    users_collection.update_one({"user_id": target["user_id"]}, {"$set": {"status": "dead", "death_time": datetime.utcnow()}})
    users_collection.update_one({"user_id": attacker["user_id"]}, {"$inc": {"kills": 1, "balance": final_reward}})

    await update.message.reply_text(
        f"👤 {get_mention(attacker)} killed <b>{target['first_name']}</b>!\n💰 <b>Earned:</b> <code>{format_money(final_reward)}</code>", 
        parse_mode=ParseMode.HTML
    )

# =====================================
# 💸 ROB COMMAND
# =====================================
async def rob(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message: return
    attacker = ensure_user_exists(update.effective_user)
    
    if not context.args: 
        return await update.message.reply_text("⚠️ <b>Usage:</b> <code>/rob [amount] @user</code>", parse_mode=ParseMode.HTML)

    try: 
        amount = int(context.args[0])
        if amount <= 0: raise ValueError
    except: 
        return await update.message.reply_text("⚠️ <b>Sahi amount dalo!</b>", parse_mode=ParseMode.HTML)

    target, _ = await resolve_target(update, context)
    if not target or target['user_id'] == attacker['user_id']: 
        return await update.message.reply_text("⚠️ <b>Sahi target tag karo!</b>", parse_mode=ParseMode.HTML)

    if target.get('is_bot') or target['user_id'] == OWNER_ID or attacker['status'] == 'dead':
        return await update.message.reply_text("🛡️ <b>Failed!</b> Target protected hai.", parse_mode=ParseMode.HTML)

    if target['balance'] < amount: 
        return await update.message.reply_text(f"📉 <b>Target ke paas sirf {format_money(target['balance'])} hai.</b>", parse_mode=ParseMode.HTML)

    users_collection.update_one({"user_id": target["user_id"]}, {"$inc": {"balance": -amount}})
    users_collection.update_one({"user_id": attacker["user_id"]}, {"$inc": {"balance": amount}})

    await update.message.reply_text(
        f"👤 {get_mention(attacker)} robbed <code>{format_money(amount)}</code> from <b>{target['first_name']}</b>!", 
        parse_mode=ParseMode.HTML
    )

# =====================================
# 🛡️ PROTECTION
# =====================================
async def protect(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message: return
    sender = ensure_user_exists(update.effective_user)
    if not context.args: 
        return await update.message.reply_text("⚠️ <code>/protect 1d</code> or <code>2d</code>", parse_mode=ParseMode.HTML)

    dur = context.args[0].lower()
    if dur == '1d': cost, days = PROTECT_1D_COST, 1
    elif dur == '2d': cost, days = PROTECT_2D_COST, 2
    else: return await update.message.reply_text("⚠️ 1d or 2d only!", parse_mode=ParseMode.HTML)

    target, _ = await resolve_target(update, context)
    if not target: target = sender

    if sender['balance'] < cost: 
        return await update.message.reply_text(f"❌ Need {format_money(cost)}", parse_mode=ParseMode.HTML)

    expiry_dt = datetime.utcnow() + timedelta(days=days)
    users_collection.update_one({"user_id": sender["user_id"]}, {"$inc": {"balance": -cost}})
    users_collection.update_one({"user_id": target["user_id"]}, {"$set": {"protection_expiry": expiry_dt}})

    await update.message.reply_text(f"🛡️ <b>Shield Active!</b> {get_mention(target)} safe for {days} day(s).", parse_mode=ParseMode.HTML)

# =====================================
# 💉 REVIVE
# =====================================
async def revive(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message: return
    reviver = ensure_user_exists(update.effective_user)
    target, _ = await resolve_target(update, context)
    if not target: target = reviver

    if target['status'] == 'alive': 
        return await update.message.reply_text("✨ <b>Alive!</b>", parse_mode=ParseMode.HTML)
    if reviver['balance'] < REVIVE_COST: 
        return await update.message.reply_text(f"❌ Need {format_money(REVIVE_COST)}", parse_mode=ParseMode.HTML)

    users_collection.update_one({"user_id": reviver["user_id"]}, {"$inc": {"balance": -REVIVE_COST}})
    users_collection.update_one({"user_id": target["user_id"]}, {"$set": {"status": "alive", "death_time": None}})
    await update.message.reply_text(f"💖 <b>Revived!</b> {get_mention(target)} is back.", parse_mode=ParseMode.HTML)

# =====================================
# 💰 PAY
# =====================================
async def pay(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message: return
    user = ensure_user_exists(update.effective_user)
    if len(context.args) < 1: 
        return await update.message.reply_text("⚠️ <code>/pay [amount] @user</code>", parse_mode=ParseMode.HTML)

    try: 
        amount = int(context.args[0])
        if amount <= 0: raise ValueError
    except: 
        return await update.message.reply_text("⚠️ <b>Sahi amount dalo.</b>", parse_mode=ParseMode.HTML)

    if user['balance'] < amount: 
        return await update.message.reply_text("❌ <b>Paisa kam hai!</b>", parse_mode=ParseMode.HTML)

    target, _ = await resolve_target(update, context)
    if not target or target['user_id'] == user['user_id']: 
        return await update.message.reply_text("⚠️ <b>Sahi user tag karo.</b>", parse_mode=ParseMode.HTML)

    users_collection.update_one({"user_id": user["user_id"]}, {"$inc": {"balance": -amount}})
    users_collection.update_one({"user_id": target["user_id"]}, {"$inc": {"balance": amount}})
    await update.message.reply_text(f"✅ Sent <code>{format_money(amount)}</code> to <b>{target['first_name']}</b>.", parse_mode=ParseMode.HTML)
