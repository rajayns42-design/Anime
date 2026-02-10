# Copyright (c) 2025 Telegram:- @WTF_Phantom <DevixOP>
# Edited for Malik: ZEXX (Fast Economy Version)

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from telegram.constants import ParseMode, ChatType
from baka.config import REGISTER_BONUS, OWNER_ID, TAX_RATE, CLAIM_BONUS, MARRIED_TAX_RATE, SHOP_ITEMS, MIN_CLAIM_MEMBERS
from baka.utils import ensure_user_exists, get_mention, format_money, resolve_target, log_to_channel, stylize_text, track_group
from baka.database import users_collection, groups_collection
import random # Local roasts ke liye

# --- INVENTORY CALLBACK (FAST) ---
async def inventory_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data.split("|")
    item_id = data[1]

    item = next((i for i in SHOP_ITEMS if i['id'] == item_id), None)
    if not item: 
        await query.answer("❌ Item data not found.", show_alert=True)
        return

    rarity_text = "Common"
    if item['price'] > 100000: rarity_text = "Rare"
    if item['price'] > 1000000: rarity_text = "Legendary"
    if item['price'] > 100000000: rarity_text = "Godly"

    text = (
        f"💎 𝐅𝐥𝐞𝐱 𝐈𝐭𝐞𝐦: {item['name']}\n"
        f"💰 𝐕𝐚𝐥𝐮𝐞: {format_money(item['price'])}\n"
        f"🌟 𝐑𝐚𝐫𝐢𝐭𝐲: {rarity_text}\n"
        f"🛡️ 𝐒𝐭𝐚𝐭𝐮𝐬: Safe (Unless you die!)"
    )
    await query.answer(text, show_alert=True)

# --- REGISTER (PM ONLY) ---
async def register(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat = update.effective_chat

    if chat.type != ChatType.PRIVATE:
        kb = InlineKeyboardMarkup([[InlineKeyboardButton("🚀 Register Here", url=f"https://t.me/{context.bot.username}?start=register")]])
        return await update.message.reply_text(
            "❌ <b>Angel!</b> You cannot register in a group!\n"
            "<i>Go to my PM to create your wallet securely.</i>",
            parse_mode=ParseMode.HTML,
            reply_markup=kb
        )

    if users_collection.find_one({"user_id": user.id}): 
        return await update.message.reply_text(f"✨ <b>Ara?</b> {get_mention(user)}, you are already registered!", parse_mode=ParseMode.HTML)

    ensure_user_exists(user)
    users_collection.update_one({"user_id": user.id}, {"$set": {"balance": REGISTER_BONUS}})

    await update.message.reply_text(
        f"🎉 <b>Yayy!</b> {get_mention(user)} Registered!\n"
        f"🎁 <b>Welcome Bonus:</b> <code>+{format_money(REGISTER_BONUS)}</code>", 
        parse_mode=ParseMode.HTML
    )

# --- CLAIM (INSTANT NO AI) ---
async def claim(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user

    if chat.type == ChatType.PRIVATE:
        return await update.message.reply_text("⚠️ <b>Angel!</b> Group only command.", parse_mode=ParseMode.HTML)

    ensure_user_exists(user)
    track_group(chat, user)

    group_doc = groups_collection.find_one({"chat_id": chat.id})
    if group_doc and group_doc.get("claimed"): 
        return await update.message.reply_text("❌ <b>Too late!</b> Already claimed.", parse_mode=ParseMode.HTML)

    try: 
        count = await context.bot.get_chat_member_count(chat.id)
    except: 
        return await update.message.reply_text("⚠️ Need <b>Admin Rights</b> to count members!", parse_mode=ParseMode.HTML)

    if count < MIN_CLAIM_MEMBERS:
        # AI Hata kar local fast roasts add kiye
        local_roasts = [
            f"Sirf {count} log? Itne mein toh Angel chai bhi nahi peeta! 😂",
            f"Itne kam logo mein claim? Sharam karo thodi! 💀",
            f"Group hai ya shamshaan ghat? {MIN_CLAIM_MEMBERS} members lao pehle.",
            f"Gali ke kutton ki sankhya isse zyada hai, aur tumhe reward chahiye? 🤡"
        ]
        final_roast = random.choice(local_roasts)

        return await update.message.reply_text(
            f"❌ <b>Claim Failed!</b>\n\n"
            f"📉 <b>Members:</b> {count}/{MIN_CLAIM_MEMBERS}\n"
            f"🔥 <b>Roast:</b> <i>{stylize_text(final_roast)}</i>", 
            parse_mode=ParseMode.HTML
        )

    users_collection.update_one({"user_id": user.id}, {"$inc": {"balance": CLAIM_BONUS}})
    groups_collection.update_one({"chat_id": chat.id}, {"$set": {"claimed": True}}, upsert=True)

    await update.message.reply_text(
        f"💎 <b>𝐂𝐥𝐚𝐢𝐦 𝐒𝐮𝐜𝐜𝐞𝐬𝐬𝐟𝐮𝐥!</b>\n\n"
        f"💰 <b>Reward:</b> <code>+{format_money(CLAIM_BONUS)}</code>", 
        parse_mode=ParseMode.HTML
    )

# --- BALANCE & RANKING (FAST) ---
async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    target, error = await resolve_target(update, context)
    if not target and error == "No target": target = ensure_user_exists(update.effective_user)
    elif not target: return await update.message.reply_text(error, parse_mode=ParseMode.HTML)

    rank = users_collection.count_documents({"balance": {"$gt": target["balance"]}}) + 1
    status = "💖 Alive" if target['status'] == 'alive' else "💀 Dead"

    inventory = target.get('inventory', [])
    flex_items = [i for i in inventory if i.get('type') == 'flex']

    kb = []
    row = []
    for item in flex_items:
        row.append(InlineKeyboardButton(item['name'], callback_data=f"inv_view|{item['id']}"))
        if len(row) == 2:
            kb.append(row); row = []
    if row: kb.append(row)

    msg = (
        f"👤 <b>User:</b> {get_mention(target)}\n"
        f"👛 <b>Balance:</b> <code>{format_money(target['balance'])}</code>\n"
        f"🏆 <b>Rank:</b> <code>#{rank}</code>\n"
        f"❤️ <b>Status:</b> {status}\n"
        f"⚔️ <b>Kills:</b> <code>{target['kills']}</code>"
    )
    await update.message.reply_text(msg, parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup(kb) if kb else None)

async def ranking(update: Update, context: ContextTypes.DEFAULT_TYPE):
    rich = users_collection.find().sort("balance", -1).limit(10)
    msg = "🏆 <b>𝐆𝐋𝐎𝐁𝐀𝐋 𝐋𝐄𝐀𝐃𝐄𝐑𝐁𝐎𝐀𝐑𝐃</b>\n\n💰 <b>𝐓𝐨𝐩 𝐑𝐢𝐜𝐡𝐞𝐬𝐭:</b>\n"
    for i, d in enumerate(rich, 1): 
        msg += f"{i}. {get_mention(d)} » <b>{format_money(d['balance'])}</b>\n"
    await update.message.reply_text(msg, parse_mode=ParseMode.HTML)

# --- GIVE (FAST) ---
async def give(update: Update, context: ContextTypes.DEFAULT_TYPE):
    sender = ensure_user_exists(update.effective_user)
    args = context.args
    if not args: return await update.message.reply_text("⚠️ <code>/give [amt] [@user]</code>", parse_mode=ParseMode.HTML)

    amount = next((int(a) for a in args if a.isdigit()), None)
    if amount is None or amount <= 0: return await update.message.reply_text("❌ Invalid amount.", parse_mode=ParseMode.HTML)

    target, error = await resolve_target(update, context)
    if not target: return await update.message.reply_text(error or "❌ Target not found.", parse_mode=ParseMode.HTML)

    if sender['balance'] < amount: return await update.message.reply_text("📉 Balance low!", parse_mode=ParseMode.HTML)
    if sender['user_id'] == target['user_id']: return await update.message.reply_text("🤔 Yourself?", parse_mode=ParseMode.HTML)

    tax_rate = MARRIED_TAX_RATE if sender.get("partner_id") == target["user_id"] else TAX_RATE
    tax = int(amount * tax_rate)
    final_amt = amount - tax

    users_collection.update_one({"user_id": sender["user_id"]}, {"$inc": {"balance": -amount}})
    users_collection.update_one({"user_id": target["user_id"]}, {"$inc": {"balance": final_amt}})
    users_collection.update_one({"user_id": OWNER_ID}, {"$inc": {"balance": tax}})

    await update.message.reply_text(f"💸 <b>Transfer Done!</b>\n💰 Sent: <code>{format_money(final_amt)}</code>\n🏦 Tax: <code>{format_money(tax)}</code>", parse_mode=ParseMode.HTML)
