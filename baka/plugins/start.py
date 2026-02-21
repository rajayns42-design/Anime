# Copyright (c) 2026 Telegram:- @WTF_Phantom <DevixOP>
# Edited for Malik: ZEXX (Final Aesthetic Edition)

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto
from telegram.ext import ContextTypes
from telegram.constants import ParseMode, ChatType
from baka.config import BOT_NAME, START_IMG_URL, SUPPORT_GROUP, SUPPORT_CHANNEL, OWNER_LINK
from baka.utils import ensure_user_exists, get_mention, track_group, log_to_channel

# --- ⌨️ KEYBOARDS ---

def get_start_keyboard(bot_username):
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("❍ 𝐔ᴩᴅᴀᴛᴇ ❍", url=SUPPORT_CHANNEL), 
            InlineKeyboardButton("❍ 𝐒ᴜᴩᴏᴏʀᴛ ❍", url=SUPPORT_GROUP)
        ],
        [InlineKeyboardButton("➕ 𝐀𝐝𝐝 𝐌𝐞 𝐁𝐚𝐛𝐲 ➕", url=f"https://t.me/{bot_username}?startgroup=true")],
        [
            InlineKeyboardButton("✿ 𝐇ᴇʟᴩ ✿", callback_data="help_main"), 
            InlineKeyboardButton("♡︎ 𝐇ᴀʀɪ ♡︎", url=OWNER_LINK)
        ]
    ])

def get_help_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("⚔️ RPG", callback_data="help_rpg"), 
            InlineKeyboardButton("💰 Economy", callback_data="help_eco")
        ],
        [
            InlineKeyboardButton("💗 Social", callback_data="help_social"), 
            InlineKeyboardButton("🤖 AI Chat", callback_data="help_ai")
        ],
        [InlineKeyboardButton("⬅️ Back to Home", callback_data="start_return")]
    ])

# --- 🚀 START COMMAND ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat = update.effective_chat
    
    # Ensure user is in DB
    ensure_user_exists(user)
    track_group(chat, user)
    
    # 📸 User Profile Photo Logic
    display_photo = START_IMG_URL 
    try:
        photos = await context.bot.get_user_profile_photos(user.id, limit=1)
        if photos.total_count > 0:
            display_photo = photos.photos[0][-1].file_id
    except Exception:
        pass

    # ✨ Your Aesthetic Caption
    caption = (
        f"❖ Hʏ {get_mention(user)}\n"
        f"I Aᴍ <b>{BOT_NAME}</b>\n"
        f"Tʜᴇ Aᴇꜱᴛʜᴇᴛɪᴄ AI Rᴩɢ Gᴀᴍᴇ'ꜱ Bᴏᴛ\n"
        f"━━━━━━━━━━━━━━━\n"
        f"🎮 Fᴇᴀᴛᴜʀᴇꜱ\n\n"
        f"⚔️ Rᴩɢ : Kɪʟʟ•Pʀᴏᴛᴇᴄᴛ•Rᴇᴠɪᴠᴇ\n"
        f"💗 Sᴏᴄɪᴀʟ : Mᴀʀʀʏ•Cᴏᴜᴩʟᴇ• Wᴀɪꜰᴜ\n"
        f"💰 Eᴄᴏɴᴏᴍʏ : Cᴀʟɪᴍ•Gɪᴠᴇ Sʜᴏᴩ•Dᴀɪʟʏ\n"
        f"🤖 AI : Sᴍᴀʀᴛ Cʜᴀᴛʙᴏᴛ•Aꜱᴋ Aɴʏᴛʜɪɴᴋ\n"
        f"━━━━━━━━━━━━━━━\n"
        f"💭 Pʀᴇꜱꜱ Tᴏ Hᴇʟᴩ Bᴜᴛᴛᴏɴ\n"
        f"Sᴇᴇ Aʟʟ Fᴇᴀᴛᴜʀᴇ & Uꜱᴇ Wɪᴛʜ ./\n"
    )

    kb = get_start_keyboard(context.bot.username)

    # Message send logic
    if update.message:
        await update.message.reply_photo(
            photo=display_photo, 
            caption=caption, 
            parse_mode=ParseMode.HTML, 
            reply_markup=kb
        )
    
    # Log private starts
    if chat.type == ChatType.PRIVATE:
        await log_to_channel(context.bot, "command", {"user": f"{get_mention(user)}", "action": "Started Bot"})

# --- 🛠️ FIX: HELP CALLBACK (Fixes Heroku Crash) ---

async def help_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data
    user = update.effective_user

    # 1. Help Main Menu
    if data == "help_main":
        await query.edit_message_caption(
            caption=f"<b>📚 {BOT_NAME} Help Menu</b>\n\nExplore all modules using the buttons below. Every command starts with <code>/</code>.",
            reply_markup=get_help_keyboard(),
            parse_mode=ParseMode.HTML
        )
    
    # 2. Return to Start
    elif data == "start_return":
        caption = (
            f"❖ Welcome Back {get_mention(user)}!\n\n"
            f"Choose an option from the menu below to interact with <b>{BOT_NAME}</b>."
        )
        await query.edit_message_caption(
            caption=caption,
            reply_markup=get_start_keyboard(context.bot.username),
            parse_mode=ParseMode.HTML
        )

    # 3. Category Placeholders
    elif data.startswith("help_"):
        module_name = data.split("_")[1].upper()
        await query.answer(f"Opening {module_name}...", show_alert=False)
        await query.edit_message_caption(
            caption=f"<b>📖 {module_name} Module</b>\n\nCommands are being updated. Check back in a few minutes! ✨",
            reply_markup=get_help_keyboard(),
            parse_mode=ParseMode.HTML
        )

    await query.answer()
