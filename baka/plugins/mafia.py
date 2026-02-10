import random
from datetime import datetime, timedelta
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from baka.database import users_collection, mafia_collection
from baka.utils import ensure_user_exists, format_money, get_mention

# =====================================
# 🤝 TEAM CORE (Create, Join, Leave, Kick, Promote)
# =====================================

async def create_team(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = ensure_user_exists(update.effective_user)
    if not context.args:
        return await update.message.reply_text("⚠️ <b>Usage:</b> <code>/create_team [Name]</code>", parse_mode=ParseMode.HTML)
    
    team_name = " ".join(context.args)
    if user['balance'] < 50000:
        return await update.message.reply_text("❌ Team banane ke liye 50,000 cash chahiye!")
    if user.get('mafia'):
        return await update.message.reply_text("❌ Aap pehle se ek Team mein hain!")

    t_id = str(random.randint(1111, 9999))
    mafia_collection.insert_one({
        "mafia_id": t_id, "name": team_name, "boss": user['user_id'],
        "members": [user['user_id']], "bank": 0, "power": 10
    })
    users_collection.update_one({"user_id": user['user_id']}, {"$set": {"mafia": t_id, "mafia_rank": "Leader"}, "$inc": {"balance": -50000}})
    await update.message.reply_text(f"✅ <b>Team Created!</b>\n📛 <b>Name:</b> {team_name}\n🆔 <b>ID:</b> <code>{t_id}</code>\n👤 <b>Leader:</b> {user['first_name']}", parse_mode=ParseMode.HTML)

async def join_team(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = ensure_user_exists(update.effective_user)
    if not context.args: return await update.message.reply_text("⚠️ <code>/join_team [ID]</code>")
    t_id = context.args[0]
    if user.get('mafia'): return await update.message.reply_text("❌ Already in a team!")
    team = mafia_collection.find_one({"mafia_id": t_id})
    if not team: return await update.message.reply_text("❌ Invalid Team ID!")

    mafia_collection.update_one({"mafia_id": t_id}, {"$push": {"members": user['user_id']}})
    users_collection.update_one({"user_id": user['user_id']}, {"$set": {"mafia": t_id, "mafia_rank": "Member"}})
    await update.message.reply_text(f"🤝 Joined <b>{team['name']}</b>!", parse_mode=ParseMode.HTML)

async def promote_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = ensure_user_exists(update.effective_user)
    mafia = mafia_collection.find_one({"mafia_id": user.get('mafia')})
    if not mafia or mafia['boss'] != user['user_id']: return await update.message.reply_text("❌ Sirf Leader promote kar sakta hai!")
    if not update.message.reply_to_message: return await update.message.reply_text("⚠️ Reply to member.")
    
    target_id = update.message.reply_to_message.from_user.id
    users_collection.update_one({"user_id": target_id}, {"$set": {"mafia_rank": "Underboss"}})
    await update.message.reply_text("🎖️ Member promoted to Underboss!")

async def kick_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = ensure_user_exists(update.effective_user)
    mafia = mafia_collection.find_one({"mafia_id": user.get('mafia')})
    if not mafia or mafia['boss'] != user['user_id']: return await update.message.reply_text("❌ Sirf Leader kick kar sakta hai!")
    if not update.message.reply_to_message: return await update.message.reply_text("⚠️ Reply to kick.")
    
    target_id = update.message.reply_to_message.from_user.id
    mafia_collection.update_one({"mafia_id": mafia['mafia_id']}, {"$pull": {"members": target_id}})
    users_collection.update_one({"user_id": target_id}, {"$unset": {"mafia": "", "mafia_rank": ""}})
    await update.message.reply_text("👞 Member kicked from the team!")

async def leave_team(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = ensure_user_exists(update.effective_user)
    if not user.get('mafia'): return
    mafia = mafia_collection.find_one({"mafia_id": user['mafia']})
    if mafia['boss'] == user['user_id']: return await update.message.reply_text("❌ Leader team nahi chhod sakta!")
    
    mafia_collection.update_one({"mafia_id": user['mafia']}, {"$pull": {"members": user['user_id']}})
    users_collection.update_one({"user_id": user['user_id']}, {"$unset": {"mafia": "", "mafia_rank": ""}})
    await update.message.reply_text("🚪 You left the team.")

# =====================================
# 🏦 TEAM BANK & WAR (WCW)
# =====================================

async def team_deposit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = ensure_user_exists(update.effective_user)
    if not user.get('mafia') or not context.args: return await update.message.reply_text("⚠️ <code>/t_deposit [amount]</code>")
    amt = int(context.args[0])
    if user['balance'] < amt: return await update.message.reply_text("❌ Balance kam hai!")
    
    mafia_collection.update_one({"mafia_id": user['mafia']}, {"$inc": {"bank": amt, "power": amt // 1000}})
    users_collection.update_one({"user_id": user['user_id']}, {"$inc": {"balance": -amt}})
    await update.message.reply_text(f"💰 Deposited! Team Power Increased! ⚡")

async def team_withdraw(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = ensure_user_exists(update.effective_user)
    mafia = mafia_collection.find_one({"mafia_id": user.get('mafia')})
    if not mafia or mafia['boss'] != user['user_id']: return await update.message.reply_text("❌ Only Leader can withdraw!")
    amt = int(context.args[0])
    if mafia['bank'] < amt: return await update.message.reply_text("❌ Team bank khali hai!")
    
    mafia_collection.update_one({"mafia_id": mafia['mafia_id']}, {"$inc": {"bank": -amt}})
    users_collection.update_one({"user_id": user['user_id']}, {"$inc": {"balance": amt}})
    await update.message.reply_text(f"💸 Withdrew {format_money(amt)} from Team Bank.")

async def team_war(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = ensure_user_exists(update.effective_user)
    if not user.get('mafia') or not context.args: return await update.message.reply_text("⚠️ <code>/team_war [Target_ID]</code>")
    my_t = mafia_collection.find_one({"mafia_id": user['mafia']})
    target_t = mafia_collection.find_one({"mafia_id": context.args[0]})
    if not target_t or target_t['mafia_id'] == user['mafia']: return await update.message.reply_text("❌ Invalid Target!")

    win_chance = my_t['power'] / (my_t['power'] + target_t['power'])
    await update.message.reply_text(f"⚔️ <b>WAR!</b> {my_t['name']} vs {target_t['name']}...")
    if random.random() < win_chance:
        loot = random.randint(20000, 50000)
        mafia_collection.update_one({"mafia_id": my_t['mafia_id']}, {"$inc": {"bank": loot, "power": 15}})
        mafia_collection.update_one({"mafia_id": target_t['mafia_id']}, {"$inc": {"bank": -loot if target_t['bank'] > loot else -target_t['bank'], "power": -10}})
        await update.message.reply_text(f"🏆 <b>Victory!</b> Looted {format_money(loot)}!")
    else:
        mafia_collection.update_one({"mafia_id": my_t['mafia_id']}, {"$inc": {"power": -10}})
        await update.message.reply_text("💀 <b>Defeat!</b> Team power lost.")

# =====================================
# 🏟️ ARENA (1vs1) & LEADERBOARD
# =====================================

async def arena_fight(update: Update, context: ContextTypes.DEFAULT_TYPE):
    attacker = ensure_user_exists(update.effective_user)
    if not context.args or not update.message.reply_to_message:
        return await update.message.reply_text("⚠️ Reply to someone: <code>/arena [amount]</code>")
    bet = int(context.args[0])
    victim = ensure_user_exists(update.message.reply_to_message.from_user)
    if attacker['balance'] < bet or victim['balance'] < bet: return await update.message.reply_text("❌ Low Balance!")
    
    winner = random.choice([attacker, victim])
    loser = victim if winner == attacker else attacker
    users_collection.update_one({"user_id": winner['user_id']}, {"$inc": {"balance": bet}})
    users_collection.update_one({"user_id": loser['user_id']}, {"$inc": {"balance": -bet}})
    await update.message.reply_text(f"🏆 <b>Arena Winner: {winner['first_name']}</b>\n💰 Prize: {format_money(bet*2)}")

async def team_leaderboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    top = list(mafia_collection.find().sort([("power", -1)]).limit(10))
    if not top: return
    try: boss = (await context.bot.get_chat(top[0]['boss'])).first_name
    except: boss = "Unknown"
    text = f"<b>👑 『 𝐓𝐎𝐏 𝐓𝐄𝐀𝐌 』 👑</b>\n━━━━━━━━━━━━━━━━━━━━\n🥇 <b>𝐍𝐚𝐦𝐞:</b> {top[0]['name']}\n👤 <b>𝐋𝐞𝐚𝐝𝐞𝐫:</b> {boss}\n⚡ <b>𝐏𝐨𝐰𝐞𝐫:</b> {top[0]['power']}\n━━━━━━━━━━━━━━━━━━━━\n"
    for i, t in enumerate(top[1:], 2): text += f"{i}. <b>{t['name']}</b> | ⚡ {t['power']}\n"
    await update.message.reply_text(text + "\n🔥 <i>ZEXX World</i>", parse_mode=ParseMode.HTML)
