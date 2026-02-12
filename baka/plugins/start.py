# Copyright (c) 2025 Telegram:- @WTF_Phantom <DevixOP>
# Edited for Malik: ZEXX

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto
from telegram.ext import ContextTypes
from telegram.constants import ParseMode, ChatType
from baka.config import BOT_NAME, START_IMG_URL, HELP_IMG_URL, SUPPORT_GROUP, SUPPORT_CHANNEL, OWNER_LINK
from baka.utils import ensure_user_exists, get_mention, track_group, log_to_channel, SUDO_USERS

# --- 🖼️ IMAGES ---
SUDO_IMG = "https://files.catbox.moe/gyi5iu.jpg"

# --- ⌨️ KEYBOARDS (STYLISH DESIGN) ---

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
        [InlineKeyboardButton("💍 𝐒𝐨𝐜𝐢𝐚𝐥", callback_data="help_social"), InlineKeyboardButton("💰 𝐄𝐜𝐨𝐧𝐨𝐦𝐲", callback_data="help_economy")],
        [InlineKeyboardButton("⚔️ 𝐑𝐏𝐆", callback_data="help_rpg"), InlineKeyboardButton("🧠 𝐀𝐈 & 𝐅𝐮𝐧", callback_data="help_fun")],
        [InlineKeyboardButton("⚙️ 𝐆𝐫𝐨𝐮𝐩", callback_data="help_group"), InlineKeyboardButton("🔐 𝐒𝐮𝐝𝐨", callback_data="help_sudo")],
        [InlineKeyboardButton("🔙 𝐁𝐚𝐜𝐤", callback_data="return_start")]
    ])

def get_back_keyboard():
    return InlineKeyboardMarkup([[InlineKeyboardButton("🔙 𝐁𝐚𝐜𝐤", callback_data="help_main")]])

# --- 🚀 START COMMAND (UNDERWORLD LOOK) ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat = update.effective_chat
    ensure_user_exists(user)
    track_group(chat, user)
    
    # Aapka Stylish Caption
    caption = (
        f"❖ Hʏ {get_mention(user)}\n\n"
        f"I Aᴍ <b>{BOT_NAME}</b>\n"
        f"Tʜᴇ Aᴇꜱᴛʜᴇᴛɪᴄ  Aɪ Rᴩɢ & Uʟᴛɪᴍᴀᴛᴇ ɢᴀᴍᴇ'ꜱ  Bᴏᴛ\n\n"f"━━━━━━━━━━━━━━━\n"
        f"🎮 Fᴇᴀᴛᴜʀᴇꜱ\n\n"
        f"⚔️ Rᴩɢ : Kɪʟʟ•Pʀᴏᴛᴇᴄᴛ•Rᴇᴠɪᴠᴇ\n"
        f"💗 Sᴏᴄɪᴀʟ : M𝐀ᴀʀʀʏ•Cᴏᴜᴩʟᴇ• Wᴀɪꜰᴜ\n"
        f"💰 Eᴄᴏɴᴏᴍʏ : Cᴀʟɪᴍ•Gɪᴠᴇ Sʜᴏᴩ•Dᴀɪʟʏ & Uʟᴛɪᴍᴀᴛᴇ ɢᴀᴍᴇ'ꜱ  Bᴏᴛ\n"
        f"🤖 ᴀɪ : Sᴍᴀʀᴛ Cʜᴀᴛʙᴏᴛ•Aꜱᴋ Aɴʏᴛʜɪɴᴋ\n"
   f"━━━━━━━━━━━━━━━\n"
        f"💭 Pʀᴇꜱʜ Tᴏ HᴇʟᴩBᴜᴛᴛᴏɴ\n"
        f"Sᴇᴇ Aʟʟ Fᴇᴀᴛᴜʀᴇ & Uꜱᴇ Wɪᴛʜ ./\n\n"
      )

    kb = get_start_keyboard(context.bot.username)

    if update.callback_query:
        try: await update.callback_query.message.edit_media(InputMediaPhoto(media=START_IMG_URL, caption=caption, parse_mode=ParseMode.HTML), reply_markup=kb)
        except: await update.callback_query.message.edit_caption(caption=caption, parse_mode=ParseMode.HTML, reply_markup=kb)
    else:
        if START_IMG_URL and START_IMG_URL.startswith("http"):
            try: await update.message.reply_photo(photo=START_IMG_URL, caption=caption, parse_mode=ParseMode.HTML, reply_markup=kb)
            except: await update.message.reply_text(caption, parse_mode=ParseMode.HTML, reply_markup=kb)
        else: await update.message.reply_text(caption, parse_mode=ParseMode.HTML, reply_markup=kb)

    if chat.type == ChatType.PRIVATE and not update.callback_query:
        await log_to_channel(context.bot, "command", {"user": f"{get_mention(user)} (`{user.id}`)", "action": "Started Bot", "chat": "Private"})

# --- 📖 HELP COMMAND ---

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_photo(
        photo=HELP_IMG_URL,
        caption=f"📖 <b>{BOT_NAME} 𝐂𝐨𝐦𝐦𝐚𝐧𝐝 𝐃𝐢𝐚𝐫𝐲</b> 🌸\n\n<i>Select a category below to explore all features!</i>",
        parse_mode=ParseMode.HTML,
        reply_markup=get_help_keyboard()
    )

# --- 🖱️ CALLBACK HANDLER ---

async def help_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data
    
    if data == "return_start":
        await start(update, context)
        return

    if data == "help_main":
        try: await query.message.edit_media(InputMediaPhoto(media=HELP_IMG_URL, caption=f"📖 <b>{BOT_NAME} 𝐂𝐨𝐦𝐦𝐚𝐧𝐝 𝐃𝐢𝐚𝐫𝐲</b> 🌸\n\n<i>Select a category below to explore all features!</i>", parse_mode=ParseMode.HTML), reply_markup=get_help_keyboard())
        except: await query.message.edit_caption(caption=f"📖 <b>{BOT_NAME} 𝐂𝐨𝐦𝐦𝐚𝐧𝐝 𝐃𝐢𝐚𝐫𝐲</b> 🌸\n\n<i>Select a category below to explore all features!</i>", parse_mode=ParseMode.HTML, reply_markup=get_help_keyboard())
        return

    target_photo = HELP_IMG_URL
    kb = get_back_keyboard()
    text = ""
    
    if data == "help_social":
        text = "💍 <b>𝐒𝐨𝐜𝐢𝐚𝐥 & 𝐋𝐨𝐯𝐞</b>\n\n<b>/propose @user</b>\n↳ Marry someone.\n<b>/marry</b>\n↳ Check status.\n<b>/divorce</b>\n<b>/couple</b>"
    elif data == "help_economy":
        text = "💰 <b>𝐄𝐜𝐨𝐧𝐨𝐦𝐲</b>\n\n<b>/bal</b>\n<b>/shop</b>\n<b>/give</b>\n<b>/claim</b>\n<b>/daily</b>"
    elif data == "help_rpg":
        text = "⚔️ <b>𝐑𝐏𝐆 & 𝐖𝐚𝐫</b>\n\n<b>/kill</b>\n<b>/rob</b>\n<b>/protect</b>\n<b>/revive</b>"
    elif data == "help_fun":
        text = "🧠 <b>𝐀𝐈 & 𝐅𝐮𝐧</b>\n\n<b>/draw</b>\n<b>/speak</b>\n<b>/chatbot</b>\n<b>/riddle</b>\n<b>/dice</b>"
    elif data == "help_group":
        text = "⚙️ <b>𝐆𝐫𝐨𝐮𝐩</b>\n\n<b>/welcome on/off</b>\n<b>/ping</b>"
    elif data == "help_sudo":
        if query.from_user.id not in SUDO_USERS: return await query.answer("❌ Baka! Owner Only!", show_alert=True)
        target_photo = SUDO_IMG
        text = "🔐 <b>𝐒𝐮𝐝𝐨 𝐏𝐚𝐧𝐞𝐥</b>\n\n<b>/addcoins</b>\n<b>/broadcast</b>\n<b>/update</b>"

    try: await query.message.edit_media(InputMediaPhoto(media=target_photo, caption=text, parse_mode=ParseMode.HTML), reply_markup=kb)
    except: await query.message.edit_caption(caption=text, parse_mode=ParseMode.HTML, reply_markup=kb)
