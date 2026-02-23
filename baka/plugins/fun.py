import asyncio
import random
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from baka.utils import ensure_user_exists, format_money
from baka.database import users_collection

# --- EXISTING DICE & SLOTS ---
async def dice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = ensure_user_exists(update.effective_user)
    chat_id = update.effective_chat.id
    if not context.args: 
        return await update.message.reply_text("🎲 <b>Usage:</b> <code>/dice [amount]</code>", parse_mode=ParseMode.HTML)
    try: bet = int(context.args[0])
    except: return await update.message.reply_text("⚠️ Invalid bet.")
    if user['balance'] < bet: return await update.message.reply_text("📉 Not enough money.")
    msg = await context.bot.send_dice(chat_id, emoji='🎲')
    result = msg.dice.value 
    await asyncio.sleep(3)
    if result > 3:
        win_amt = bet 
        users_collection.update_one({"user_id": user["user_id"]}, {"$inc": {"balance": win_amt}})
        await update.message.reply_text(f"🎲 <b>Result:</b> {result}\n🎉 <b>Won!</b> +<code>{format_money(win_amt)}</code>", reply_to_message_id=msg.message_id, parse_mode=ParseMode.HTML)
    else:
        users_collection.update_one({"user_id": user["user_id"]}, {"$inc": {"balance": -bet}})
        await update.message.reply_text(f"🎲 <b>Result:</b> {result}\n💀 <b>Lost!</b> -<code>{format_money(bet)}</code>", reply_to_message_id=msg.message_id, parse_mode=ParseMode.HTML)

# --- NEW FUNCTIONS TO FIX CRASH ---

async def truth(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Answers a random truth question."""
    questions = [
        "Aapka sabse bada secret kya hai?",
        "Kya aapne kabhi kisi se jhoot bola hai?",
        "Aapka pehla crush kaun tha?",
        "Sabse embarrassing moment kya tha aapka?",
        "Kya aapne kabhi group me kisi ko block kiya hai?"
    ]
    await update.message.reply_text(f"✨ <b>TRUTH:</b>\n\n<i>{random.choice(questions)}</i>", parse_mode=ParseMode.HTML)

async def dare(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Gives a random dare task."""
    tasks = [
        "Apne crush ko I Love You bolo aur screenshot dikhao!",
        "Group me koi funny audio message bhejo.",
        "Agle 5 minutes tak har message ke baad 'Me Pagal Hu' likho.",
        "Apni DP change karke kisi cartoon ki photo lagao.",
        "Group me kisi random member ki tareef karo."
    ]
    await update.message.reply_text(f"🔥 <b>DARE:</b>\n\n<i>{random.choice(tasks)}</i>", parse_mode=ParseMode.HTML)

async def quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Simple Quiz Logic."""
    await update.message.reply_text("❓ <b>Quiz:</b>\n\nLogic building in progress... Try /truth or /dare for now!", parse_mode=ParseMode.HTML)
