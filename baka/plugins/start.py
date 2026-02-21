# Copyright (c) 2026 Telegram:- @WTF_Phantom <DevixOP>
# Professional Multi-Module Dashboard for ZEXX

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from baka.config import BOT_NAME, START_IMG_URL, OWNER_LINK
from baka.utils import get_mention, ensure_user_exists

# --- ⌨️ KEYBOARDS (Sari files ke liye alag buttons) ---

def get_start_keyboard(bot_username):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("❍ 𝐔ᴩᴅᴀᴛᴇ ❍", url="https://t.me/ZexxUpdates"), InlineKeyboardButton("❍ 𝐒ᴜᴩᴏᴏʀᴛ ❍", url="https://t.me/ZexxSupport")],
        [InlineKeyboardButton("➕ 𝐀𝐝𝐝 𝐌𝐞 𝐁𝐚𝐛𝐲 ➕", url=f"https://t.me/{bot_username}?startgroup=true")],
        [InlineKeyboardButton("✿ 𝐇ᴇʟᴩ ✿", callback_data="help_main"), InlineKeyboardButton("♡︎ 𝐇ᴀʀɪ ♡︎", url=OWNER_LINK)]
    ])

def get_help_keyboard():
    # Screenshots ki sari files yahan buttons mein convert kar di hain
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("⚔️ RPG & Mᴀꜰɪᴀ", callback_data="help_rpg"), InlineKeyboardButton("💰 Eᴄᴏɴᴏᴍʏ", callback_data="help_eco")],
        [InlineKeyboardButton("💗 Sᴏᴄɪᴀʟ & Lᴏᴠᴇ", callback_data="help_social"), InlineKeyboardButton("🤖 AI & Cʜᴀᴛ", callback_data="help_ai")],
        [InlineKeyboardButton("🎮 Gᴀᴍᴇꜱ & Fᴜɴ", callback_data="help_games"), InlineKeyboardButton("🛡️ Sʏꜱᴛᴇᴍ", callback_data="help_system")],
        [InlineKeyboardButton("⬅️ Bᴀᴄᴋ Tᴏ Hᴏᴍᴇ", callback_data="start_return")]
    ])

# --- 🚀 START COMMAND ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    ensure_user_exists(user)
    
    display_photo = START_IMG_URL 
    try:
        photos = await context.bot.get_user_profile_photos(user.id, limit=1)
        if photos.total_count > 0: display_photo = photos.photos[0][-1].file_id
    except: pass

    caption = (
        f"<blockquote>"
        f"❖ Hʏ {get_mention(user)}\n"
        f"I Aᴍ <b>{BOT_NAME}</b>\n"
        f"Tʜᴇ Aᴇꜱᴛʜᴇᴛɪᴄ AI Rᴩɢ Gᴀᴍᴇ'ꜱ Bᴏᴛ\n"
        f"━━━━━━━━━━━━━━━\n"
        f"🎮 Fᴇᴀᴛᴜʀᴇꜱ\n"
        f"⚔️ Rᴩɢ : Kɪʟʟ•Pʀᴏᴛᴇᴄᴛ•Rᴇᴠɪᴠᴇ\n"
        f"💗 Sᴏᴄɪᴀʟ : Mᴀʀʀʏ•Cᴏᴜᴩʟᴇ•Wᴀɪꜰᴜ\n"
        f"💰 Eᴄᴏɴᴏᴍʏ : Cᴀʟɪᴍ•Gɪᴠᴇ•Sʜᴏᴩ•Dᴀɪʟʏ\n"
        f"🤖 AI : Sᴍᴀʀᴛ Cʜᴀᴛʙᴏᴛ•Aꜱᴋ Aɴʏᴛʜɪɴɢ\n"
        f"━━━━━━━━━━━━━━━\n"
        f"💭 Pʀᴇꜱꜱ Hᴇʟᴩ Bᴜᴛᴛᴏɴ\n"
        f"Sᴇᴇ Aʟʟ Fᴇᴀᴛᴜʀᴇꜱ & Uꜱᴇ Wɪᴛʜ ./\n"
        f"</blockquote>"
    )

    if update.callback_query:
        await update.callback_query.message.edit_caption(caption=caption, reply_markup=get_start_keyboard(context.bot.username), parse_mode=ParseMode.HTML)
    else:
        await update.message.reply_photo(photo=display_photo, caption=caption, parse_mode=ParseMode.HTML, reply_markup=get_start_keyboard(context.bot.username))

# --- 🛠️ PERSONAL HELP CALLBACK (Sari Files ka Data) ---

async def help_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data
    mention = get_mention(update.effective_user)

    if data == "help_main":
        text = f"<b>📚 {BOT_NAME} Pᴇʀꜱᴏɴᴀʟ Gᴜɪᴅᴇ</b>\n\nHᴇʏ {mention}, Select a category below to see how to use my features! ✨"
        await query.edit_message_caption(caption=text, reply_markup=get_help_keyboard(), parse_mode=ParseMode.HTML)

    elif data == "help_rpg":
        text = (f"<b>⚔️ RPG & Mᴀꜰɪᴀ Sʏꜱᴛᴇᴍ</b>\n\n"
                f"• <code>/mafia</code> : Create your underworld gang.\n"
                f"• <code>/kill [user]</code> : Eliminate your rivals.\n"
                f"• <code>/rob [user]</code> : Steal gold from others.\n"
                f"• <code>/protect</code> : Guard yourself from attacks.\n"
                f"• <code>/arena</code> : Enter the battlefield.")
        await query.edit_message_caption(caption=text, reply_markup=get_help_keyboard(), parse_mode=ParseMode.HTML)

    elif data == "help_eco":
        text = (f"<b>💰 Eᴄᴏɴᴏᴍʏ & Sʜᴏᴩ</b>\n\n"
                f"• <code>/bal</code> : Check your bank & wallet.\n"
                f"• <code>/daily</code> : Claim your 24h gold reward.\n"
                f"• <code>/shop</code> : Buy items, badges & boosts.\n"
                f"• <code>/give [user] [amt]</code> : Share your money.\n"
                f"• <code>/rank</code> : Top richest players.")
        await query.edit_message_caption(caption=text, reply_markup=get_help_keyboard(), parse_mode=ParseMode.HTML)

    elif data == "help_social":
        text = (f"<b>💗 Sᴏᴄɪᴀʟ & Rᴇʟᴀᴛɪᴏɴꜱʜɪᴩ</b>\n\n"
                f"• <code>/love</code> : Match compatibility with photo.\n"
                f"• <code>/couple</code> : Daily group romantic match.\n"
                f"• <code>/marry</code> : Propose & get certificate.\n"
                f"• <code>/divorce</code> : End your current marriage.\n"
                f"• <code>/waifu</code> : Find your daily AI Waifu.")
        await query.edit_message_caption(caption=text, reply_markup=get_help_keyboard(), parse_mode=ParseMode.HTML)

    elif data == "help_ai":
        text = (f"<b>🤖 AI & Cʜᴀᴛʙᴏᴛ Sᴇᴛᴛɪɴɢꜱ</b>\n\n"
                f"• <code>/ask [query]</code> : Chat with smart AI.\n"
                f"• <code>/chatbot</code> : Enable/Disable auto-replies.\n"
                f"• <code>/draw [prompt]</code> : Create AI Art images.\n"
                f"• <code>/speak [text]</code> : Text to Voice conversion.")
        await query.edit_message_caption(caption=text, reply_markup=get_help_keyboard(), parse_mode=ParseMode.HTML)

    elif data == "help_games":
        text = (f"<b>🎮 Gᴀᴍᴇꜱ & Fᴜɴ Lɪꜱᴛ</b>\n\n"
                f"• <code>/word</code> : Start WordSeek puzzle game.\n"
                f"• <code>/riddle</code> : Solve tricky riddles for gold.\n"
                f"• <code>/dice</code> : Roll & try your luck.\n"
                f"• <code>/wlb</code> : Check game leaderboard.")
        await query.edit_message_caption(caption=text, reply_markup=get_help_keyboard(), parse_mode=ParseMode.HTML)

    elif data == "help_system":
        text = (f"<b>🛡️ Sʏꜱᴛᴇᴍ & Aᴅᴍɪɴ Gᴜɪᴅᴇ</b>\n\n"
                f"• <code>/broadcast</code> : Global message (Owner).\n"
                f"• <code>/ping</code> : Check bot speed & latency.\n"
                f"• <code>/stats</code> : See bot user statistics.\n"
                f"• <code>/events</code> : Check ongoing bot events.")
        await query.edit_message_caption(caption=text, reply_markup=get_help_keyboard(), parse_mode=ParseMode.HTML)

    elif data == "start_return":
        await start(update, context)

    await query.answer()
