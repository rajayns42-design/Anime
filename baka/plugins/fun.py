import asyncio
import random
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from baka.utils import ensure_user_exists, format_money
from baka.database import users_collection

async def truth(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Badi list ke saath Unlimited Truth"""
    questions = [
        "Aapka sabse bada dar (fear) kya hai?",
        "Kya aapne kabhi kisi ka phone chhupkar check kiya hai?",
        "Aapka sabse ganda habit kya hai?",
        "Kya aapne kabhi school/college me cheat kiya hai?",
        "Aapki pehli kamai kitni thi?",
        "Agar aap ek din ke liye ladki/ladka ban jaye toh kya karenge?",
        "Aapka sabse bada regret kya hai?",
        "Aapne aakhri baar kab jhoot bola tha aur kisse?",
        "Kya aapko kisi member par crush hai is group me?",
        "Aapka sabse ajeeb sapna (weirdest dream) kya tha?",
        "Agar aapko $1 Million mile toh aap sabse pehle kya kharidenge?",
        "Kya aapne kabhi public me kuch embarrassing kiya hai?"
    ]
    await update.message.reply_text(
        f"✨ <b>『 𝐓𝐑𝐔𝐓𝐇 』</b>\n━━━━━━━━━━━━━━━━━━\n💬 <i>{random.choice(questions)}</i>\n━━━━━━━━━━━━━━━━━━\n🔥 <i>ZEXX Fun Mode</i>",
        parse_mode=ParseMode.HTML
    )

async def dare(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Badi list ke saath Unlimited Dare"""
    tasks = [
        "Apne kisi ex ko 'I miss you' message karo aur screen recording dikhao.",
        "Group me 1 minute tak bina ruke voice note me gana gao.",
        "Apni sabse purani/ajeeb photo group me share karo.",
        "Agle 10 minutes tak kisi bhi member ki har baat par 'Ji Huzoor' bolo.",
        "Apna status change karke likho 'Me sabse bada namuna hu'.",
        "Group ke admin ki tareef me 5 lines likho.",
        "Kisi random member ko private me 'Will you marry me?' bolo.",
        "Apni gallery ki 5th photo bina dekhe group me bhejo.",
        "Ek glass paani 5 second me pi kar dikhao (Video proof).",
        "Apne ghar me kisi ke saath prank karke audio bhejo."
    ]
    await update.message.reply_text(
        f"🔥 <b>『 𝐃𝐀𝐑𝐄 』</b>\n━━━━━━━━━━━━━━━━━━\n🎯 <i>{random.choice(tasks)}</i>\n━━━━━━━━━━━━━━━━━━\n⚡ <i>ZEXX Fun Mode</i>",
        parse_mode=ParseMode.HTML
    )

async def quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Quiz logic link"""
    await update.message.reply_text("❓ <b>Quiz module online!</b>\nAnswer carefully to win rewards.", parse_mode
