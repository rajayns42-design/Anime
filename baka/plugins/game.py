# Copyright (c) 2025 Telegram:- @WTF_Phantom <DevixOP>
# Edited for Malik: ZEXX

import random
from datetime import datetime, timedelta
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from baka.config import PROTECT_1D_COST, PROTECT_2D_COST, REVIVE_COST, OWNER_ID
from baka.utils import ensure_user_exists, resolve_target, get_active_protection, format_time, format_money, get_mention
from baka.database import users_collection

# --- KILL COMMAND ---
async def kill(update: Update, context: ContextTypes.DEFAULT_TYPE):
    attacker = ensure_user_exists(update.effective_user)
    target, error = await resolve_target(update, context)

    if not target: 
        return await update.message.reply_text(error if error else "⚠️ <b>Usage:</b> <code>/kill @user</code>", parse_mode=ParseMode.HTML)

    if target.get('is_bot') or target['user_id'] == OWNER_ID:
        return await update.message.reply_text("🤖 Bot Shield!", parse_mode=ParseMode.HTML)
    if attacker['status'] == 'dead': 
        return await update.message.reply_text("💀 You are dead.", parse_mode=ParseMode.HTML)
    if target['status'] == 'dead': 
        return await update.message.reply_text("⚰️ Already dead.", parse_mode=ParseMode.HTML)
    if target['user_id'] == attacker['user_id']: 
        return await update.message.reply_text("🤔 No.", parse_mode=ParseMode.HTML)

    expiry = get_active_protection(target)
    if expiry:
        rem = expiry - datetime.utcnow()
        return await update.message.reply_text(f"🛡️ <b>Blocked!</b> Safe for <code>{format_time(rem)}</code>.", parse_mode=ParseMode.HTML)

    base_reward = random.randint(100, 200)
    weapons = [i for i in attacker.get('inventory', []) if i['type'] == 'weapon']
    best_w = max(weapons, key=lambda x: x['buff']) if weapons else None
    buff = best_w['buff'] if best_w else 0
    final_reward = int(base_reward * (1 + buff))

    flex_burn_text = ""
    target_inv = target.get('inventory', [])
    flex_items = [i for i in target_inv if i['type'] == 'flex']
    if flex_items:
        users_collection.update_one({"user_id": target["user_id"]}, {"$pull": {"inventory": {"type": "flex"}}})
        flex_burn_text = f"\n🔥 <b>Burned:</b> {len(flex_items)} Flex Items destroyed!"

    users_collection.update_one({"user_id": target["user_id"]}, {"$set": {"status": "dead", "death_time": datetime.utcnow()}})
    users_collection.update_one({"user_id": attacker["user_id"]}, {"$inc": {"kills": 1, "balance": final_reward}})

    # Output exactly like Image 1000071014.jpg
    await update.message.reply_text(
        f"👤 {get_mention(attacker)} killed <b>{target['first_name']}</b>!\n"
        f"💰 <b>Earned:</b> <code>{format_money(final_reward)}</code>{flex_burn_text}", 
        parse_mode=ParseMode.HTML
    )

# --- ROB COMMAND ---
async def rob(update: Update, context: ContextTypes.DEFAULT_TYPE):
    attacker = ensure_user_exists(update.effective_user)
    if not context.args: 
        return await update.message.reply_text("⚠️ <b>Usage:</b> <code>/rob [amount] @user</code>", parse_mode=ParseMode.HTML)

    try: amount = int(context.args[0])
    except: return await update.message.reply_text("⚠️ Invalid Amount", parse_mode=ParseMode.HTML)
    
    target_arg = context.args[1] if len(context.args) > 1 else None
    target, error = await resolve_target(update, context, specific_arg=target_arg)
    if not target: return await update.message.reply_text(error or "⚠️ Tag victim", parse_mode=ParseMode.HTML)

    if target.get('is_bot') or target['user_id'] == OWNER_ID:
        return await update.message.reply_text("🛡️ Protected.", parse_mode=ParseMode.HTML)
    if attacker['status'] == 'dead': 
        return await update.message.reply_text("💀 Dead.", parse_mode=ParseMode.HTML)

    expiry = get_active_protection(target)
    if expiry:
        rem = expiry - datetime.utcnow()
        return await update.message.reply_text(f"🛡️ <b>Shielded!</b> Safe for <code>{format_time(rem)}</code>.", parse_mode=ParseMode.HTML)

    if target['balance'] < amount: 
        return await update.message.reply_text("📉 Too poor.", parse_mode=ParseMode.HTML)

    armors = [i for i in target.get('inventory', []) if i['type'] == 'armor']
    best_a = max(armors, key=lambda x: x['buff']) if armors else None
    if best_a and random.random() < best_a['buff']:
        return await update.message.reply_text(f"🛡️ <b>BLOCKED!</b> {get_mention(target)} used {best_a['name']} to stop you!", parse_mode=ParseMode.HTML)

    users_collection.update_one({"user_id": target["user_id"]}, {"$inc": {"balance": -amount}})
    users_collection.update_one({"user_id": attacker["user_id"]}, {"$inc": {"balance": amount}})

    # Output exactly like Image 1000071015.jpg
    # Note: Using $ symbol or format_money as per your DB setup
    await update.message.reply_text(
        f"👤 {get_mention(attacker)} robbed <code>{format_money(amount)}</code> from <b>{target['first_name']}</b>\n"
        f"💰 <b>gained:</b> <code>{format_money(amount)}</code>", 
        parse_mode=ParseMode.HTML
    )

# --- PROTECT & REVIVE (REMAIN SAME) ---
async def protect(update: Update, context: ContextTypes.DEFAULT_TYPE):
    sender = ensure_user_exists(update.effective_user)
    if not context.args: return await update.message.reply_text("⚠️ 1d or 2d only!", parse_mode=ParseMode.HTML)
    dur = context.args[0].lower()
    if dur == '1d': cost, days = PROTECT_1D_COST, 1
    elif dur == '2d': cost, days = PROTECT_2D_COST, 2
    else: return await update.message.reply_text("⚠️ 1d or 2d only!", parse_mode=ParseMode.HTML)

    target_arg = context.args[1] if len(context.args) > 1 else None
    target, _ = await resolve_target(update, context, specific_arg=target_arg)
    if not target: target = sender
    
    if sender['balance'] < cost: return await update.message.reply_text(f"❌ Need {format_money(cost)}", parse_mode=ParseMode.HTML)

    expiry_dt = datetime.utcnow() + timedelta(days=days)
    users_collection.update_one({"user_id": sender["user_id"]}, {"$inc": {"balance": -cost}})
    users_collection.update_one({"user_id": target["user_id"]}, {"$set": {"protection_expiry": expiry_dt}})
    await update.message.reply_text(f"🛡️ <b>Shield Active!</b> Safe for {days} days.", parse_mode=ParseMode.HTML)

async def revive(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reviver = ensure_user_exists(update.effective_user)
    target, _ = await resolve_target(update, context)
    if not target: target = reviver
    if target['status'] == 'alive': return await update.message.reply_text("✨ Alive!", parse_mode=ParseMode.HTML)
    if reviver['balance'] < REVIVE_COST: return await update.message.reply_text(f"❌ Need {format_money(REVIVE_COST)}", parse_mode=ParseMode.HTML)

    users_collection.update_one({"user_id": reviver["user_id"]}, {"$inc": {"balance": -REVIVE_COST}})
    users_collection.update_one({"user_id": target["user_id"]}, {"$set": {"status": "alive", "death_time": None}})
    await update.message.reply_text(f"💖 <b>Revived!</b> {get_mention(target)} is back.", parse_mode=ParseMode.HTML)
