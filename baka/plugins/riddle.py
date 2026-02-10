# Copyright (c) 2025 Telegram:- @WTF_Phantom <DevixOP>
# Edited for Malik: ZEXX

import random
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode, ChatType
from baka.database import riddles_collection, users_collection
from baka.utils import format_money, ensure_user_exists, get_mention
from baka.config import RIDDLE_REWARD

# --- EXTENDED LOCAL RIDDLE DATABASE ---
RIDDLES = [
    {"q": "I speak without a mouth and hear without ears. I have no body, but I come alive with wind.", "a": "echo"},
    {"q": "You measure my life in hours and I serve you by expiring. I’m quick when I’m thin and slow when I’m fat.", "a": "candle"},
    {"q": "I have cities, but no houses. I have mountains, but no trees. I have water, but no fish.", "a": "map"},
    {"q": "What has keys, but no locks; space, but no room; and you can enter, but never leave?", "a": "keyboard"},
    {"q": "What gets wet while drying?", "a": "towel"},
    {"q": "The more of this there is, the less you see.", "a": "darkness"},
    {"q": "What has hands, but can’t clap?", "a": "clock"},
    {"q": "What has to be broken before you can use it?", "a": "egg"},
    {"q": "I’m tall when I’m young, and I’m short when I’m old.", "a": "candle"},
    {"q": "What month of the year has 28 days?", "a": "all"},
    {"q": "What is full of holes but still holds water?", "a": "sponge"},
    {"q": "What question can you never answer yes to?", "a": "are you asleep"},
    {"q": "What is always in front of you but can’t be seen?", "a": "future"},
    {"q": "There’s a one-story house where everything is yellow. What color are the stairs?", "a": "none"},
    {"q": "What can you break, even if you never pick it up or touch it?", "a": "promise"},
    {"q": "What goes up but never comes down?", "a": "age"},
    {"q": "A man who was outside in the rain without an umbrella or hat didn’t get a single hair on his head wet. Why?", "a": "he was bald"},
    {"q": "What has a head and a tail but no body?", "a": "coin"},
    {"q": "What has a thumb and four fingers, but is not a hand?", "a": "glove"},
    {"q": "What has many needles, but can’t sew?", "a": "pine tree"}
]

async def riddle_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    if chat.type == ChatType.PRIVATE: 
        return await update.message.reply_text("❌ <b>Group Only!</b>", parse_mode=ParseMode.HTML)

    if riddles_collection.find_one({"chat_id": chat.id}):
        return await update.message.reply_text("⚠️ A riddle is already active!", parse_mode=ParseMode.HTML)

    # Fast selection from local list
    selected = random.choice(RIDDLES)
    question = selected['q']
    answer = selected['a'].lower()

    riddles_collection.insert_one({"chat_id": chat.id, "answer": answer})

    await update.message.reply_text(
        f"🧩 <b>𝐀𝐈 𝐑𝐢𝐝𝐝𝐥𝐞 𝐂𝐡𝐚𝐥𝐥𝐞𝐧𝐠𝐞!</b>\n\n"
        f"<i>{question}</i>\n\n"
        f"💡 <b>Reward:</b> <code>{format_money(RIDDLE_REWARD)}</code>\n"
        f"👇 <i>Reply with your answer!</i>",
        parse_mode=ParseMode.HTML
    )

async def check_riddle_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text: return
    chat = update.effective_chat
    text = update.message.text.strip().lower()

    riddle = riddles_collection.find_one({"chat_id": chat.id})
    if not riddle: return

    if text == riddle['answer']:
        user = update.effective_user
        ensure_user_exists(user)

        users_collection.update_one({"user_id": user.id}, {"$inc": {"balance": RIDDLE_REWARD}})
        riddles_collection.delete_one({"chat_id": chat.id})

        await update.message.reply_text(
            f"🎉 <b>𝐂𝐨𝐫𝐫𝐞𝐜𝐭!</b>\n\n"
            f"👤 <b>Winner:</b> {get_mention(user)}\n"
            f"💰 <b>Won:</b> <code>{format_money(RIDDLE_REWARD)}</code>\n"
            f"🔑 <b>Answer:</b> <i>{riddle['answer'].title()}</i>",
            parse_mode=ParseMode.HTML
        )
