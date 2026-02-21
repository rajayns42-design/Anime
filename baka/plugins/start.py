from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from telegram.constants import ParseMode, ChatType
from baka.config import BOT_NAME, START_IMG_URL, SUPPORT_GROUP, SUPPORT_CHANNEL, OWNER_LINK
from baka.utils import ensure_user_exists, get_mention, track_group

def get_start_keyboard(bot_username):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("❍ 𝐔ᴩᴅᴀᴛᴇ ❍", url=SUPPORT_CHANNEL), InlineKeyboardButton("❍ 𝐒ᴜᴩᴏᴏʀᴛ ❍", url=SUPPORT_GROUP)],
        [InlineKeyboardButton("➕ 𝐀𝐝𝐝 𝐌𝐞 𝐁𝐚𝐛𝐲 ➕", url=f"https://t.me/{bot_username}?startgroup=true")],
        [InlineKeyboardButton("✿ 𝐇ᴇʟᴩ ✿", callback_data="help_main"), InlineKeyboardButton("♡︎ 𝐇ᴀʀɪ ♡︎", url=OWNER_LINK)]
    ])

def get_help_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("⚔️ RPG Sʏꜱᴛᴇᴍ", callback_data="help_rpg"), InlineKeyboardButton("💰 Eᴄᴏɴᴏᴍʏ", callback_data="help_eco")],
        [InlineKeyboardButton("💗 Sᴏᴄɪᴀʟ", callback_data="help_social"), InlineKeyboardButton("🤖 AI Cʜᴀᴛ", callback_data="help_ai")],
        [InlineKeyboardButton("⬅️ Bᴀᴄᴋ Tᴏ Hᴏᴍᴇ", callback_data="start_return")]
    ])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    ensure_user_exists(user)
    display_photo = START_IMG_URL 
    try:
        photos = await context.bot.get_user_profile_photos(user.id, limit=1)
        if photos.total_count > 0: display_photo = photos.photos[0][-1].file_id
    except: pass

    caption = (
        f"❖ Hʏ {get_mention(user)}\n\n"
        f"I Aᴍ <b>{BOT_NAME}</b>\n"
        f"Tʜᴇ Aᴇꜱᴛʜᴇᴛɪᴄ AI Rᴩɢ Gᴀᴍᴇ'ꜱ Bᴏᴛ\n"
        f"━━━━━━━━━━━━━━━\n"
        f"🎮 Fᴇᴀᴛᴜʀᴇꜱ\n"
        f"⚔️ Rᴩɢ : Kɪʟʟ•Pʀᴏᴛᴇᴄᴛ•Rᴇᴠɪᴠᴇ\n"
        f"💗 Sᴏᴄɪᴀʟ : Mᴀʀʀʏ•Cᴏᴜᴩʟᴇ• Wᴀɪꜰᴜ\n"
        f"💰 Eᴄᴏɴᴏᴍʏ : Cᴀʟɪᴍ•Gɪᴠᴇ Sʜᴏᴩ•Dᴀɪʟʏ\n"
        f"🤖 AI : Sᴍᴀʀᴛ Cʜᴀᴛʙᴏᴛ•Aꜱᴋ Aɴʏᴛʜɪɴᴋ\n"
        f"━━━━━━━━━━━━━━━\n"
        f"💭 Pʀᴇꜱꜱ Tᴏ Hᴇʟᴩ Bᴜᴛᴛᴏɴ\n"
        f"Sᴇᴇ Aʟʟ Fᴇᴀᴛᴜʀᴇ & Uꜱᴇ Wɪᴛʜ ./\n"
    )
    
    if update.callback_query:
        await update.callback_query.message.edit_caption(caption=caption, reply_markup=get_start_keyboard(context.bot.username), parse_mode=ParseMode.HTML)
    else:
        await update.message.reply_photo(photo=display_photo, caption=caption, parse_mode=ParseMode.HTML, reply_markup=get_start_keyboard(context.bot.username))

async def help_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data
    mention = get_mention(update.effective_user)

    if data == "help_main":
        await query.edit_message_caption(caption=f"<b>📚 {BOT_NAME} Pᴇʀꜱᴏɴᴀʟ Hᴇʟᴩ</b>\n\nHᴇʏ {mention}, Select a module below! ✨", reply_markup=get_help_keyboard(), parse_mode=ParseMode.HTML)
    elif data == "help_rpg":
        await query.edit_message_caption(caption=f"<b>⚔️ RPG - Action</b>\n\n• /kill : Target someone\n• /protect : Save friend\n• /rob : Steal gold", reply_markup=get_help_keyboard(), parse_mode=ParseMode.HTML)
    elif data == "help_social":
        await query.edit_message_caption(caption=f"<b>💗 Social - Love</b>\n\n• /love : Match match\n• /couple : Daily pair\n• /marry : Propose", reply_markup=get_help_keyboard(), parse_mode=ParseMode.HTML)
    elif data == "start_return":
        await start(update, context)
    await query.answer()
