# Copyright (c) 2026 Telegram:- @WTF_Phantom <DevixOP>
# Edited for Malik: ZEXX (Profile Photo Edition)

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto
from telegram.ext import ContextTypes
from telegram.constants import ParseMode, ChatType
from baka.config import BOT_NAME, START_IMG_URL, SUPPORT_GROUP, SUPPORT_CHANNEL, OWNER_LINK
from baka.utils import ensure_user_exists, get_mention, track_group, log_to_channel

# --- ⌨️ KEYBOARD ---

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

# --- 🚀 START COMMAND ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat = update.effective_chat
    
    # User database entry
    ensure_user_exists(user)
    track_group(chat, user)
    
    # 📸 User Profile Photo Logic
    # Default image agar DP fetch na ho sake
    display_photo = START_IMG_URL 
    
    try:
        # User ki profile photos mangwao (limit 1 for speed)
        photos = await context.bot.get_user_profile_photos(user.id, limit=1)
        if photos.total_count > 0:
            # Latest photo ki file_id extract karo
            display_photo = photos.photos[0][-1].file_id
    except Exception as e:
        # Agar privacy settings ki wajah se photo na mile
        print(f"Error fetching DP: {e}")

    # ✨ Stylish Caption
    caption = (
        f"❖ Hʏ {get_mention(user)}\n\n"
        f"I Aᴍ <b>{BOT_NAME}</b>\n"
        f"Tʜᴇ Aᴇꜱᴛʜᴇᴛɪᴄ AI Rᴩɢ & Uʟᴛɪᴍᴀᴛᴇ Gᴀᴍᴇ'ꜱ Bᴏᴛ\n\n"
        f"━━━━━━━━━━━━━━━\n"
        f"🎮 Fᴇᴀᴛᴜʀᴇꜱ\n\n"
        f"⚔️ Rᴩɢ : Kɪʟʟ•Pʀᴏᴛᴇᴄᴛ•Rᴇᴠɪᴠᴇ\n"
        f"💗 Sᴏᴄɪᴀʟ : Mᴀʀʀʏ•Cᴏᴜᴩʟᴇ• Wᴀɪꜰᴜ\n"
        f"💰 Eᴄᴏɴᴏᴍʏ : Cᴀʟɪᴍ•Gɪᴠᴇ Sʜᴏᴩ•Dᴀɪʟʏ\n"
        f"🤖 AI : Sᴍᴀʀᴛ Cʜᴀᴛʙᴏᴛ•Aꜱᴋ Aɴʏᴛʜɪɴᴋ\n"
        f"━━━━━━━━━━━━━━━\n"
        f"💭 Pʀᴇꜱꜱ Tᴏ Hᴇʟᴩ Bᴜᴛᴛᴏɴ\n"
        f"Sᴇᴇ Aʟʟ Fᴇᴀᴛᴜʀᴇ & Uꜱᴇ Wɪᴛʜ ./\n\n"
    )

    kb = get_start_keyboard(context.bot.username)

    # 🔄 Callback handle (Edit message when returning to start)
    if update.callback_query:
        try:
            await update.callback_query.message.edit_media(
                media=InputMediaPhoto(media=display_photo, caption=caption, parse_mode=ParseMode.HTML), 
                reply_markup=kb
            )
        except:
            await update.callback_query.message.edit_caption(
                caption=caption, 
                parse_mode=ParseMode.HTML, 
                reply_markup=kb
            )
    
    # 📩 Fresh Start (Send New Photo)
    else:
        try:
            await update.message.reply_photo(
                photo=display_photo, 
                caption=caption, 
                parse_mode=ParseMode.HTML, 
                reply_markup=kb
            )
        except:
            # Fallback if photo sending fails
            await update.message.reply_text(
                caption, 
                parse_mode=ParseMode.HTML, 
                reply_markup=kb
            )

    # Log task
    if chat.type == ChatType.PRIVATE and not update.callback_query:
        await log_to_channel(context.bot, "command", {
            "user": f"{get_mention(user)} (`{user.id}`)", 
            "action": "Started Bot", 
            "chat": "Private"
        })
