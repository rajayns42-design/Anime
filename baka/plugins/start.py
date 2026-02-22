# Copyright (c) 2026 Telegram:- @WTF_Phantom <DevixOP>
# Professional Multi-Module Dashboard for ZEXX

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from baka.config import BOT_NAME, START_IMG_URL, OWNER_LINK
from baka.utils import get_mention, ensure_user_exists

# --- ⌨️ KEYBOARDS ---

def get_start_keyboard(bot_username):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("⌯ ᴀᴅᴅ ᴍᴇ ʙᴀʙʏ ⌯", url=f"https://t.me/{bot_username}?startgroup=true")],
        [
            InlineKeyboardButton("🥀 Bσσк", callback_data="help_main"), 
            InlineKeyboardButton("⦗ ⌯ 𝐇𝐀𝐑𝐈 ⌯ ⦘", url=OWNER_LINK)
        ],
        [
            InlineKeyboardButton("📩 Uᴩᴅᴀᴛᴇ", url="https://t.me/Love_bot_143"), 
            InlineKeyboardButton("📩 Sᴜᴩᴩᴏʀᴛ", url="https://t.me/Love_Ki_Duniyaa")
        ]
    ])

def get_21_bold_keyboard():
    # Grid of 21 Bold Buttons (3 per row)
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("❍ 𝐁𝐀𝐋 ❍", callback_data="cb_bal"),
            InlineKeyboardButton("❍ 𝐃𝐀𝐈𝐋𝐘 ❍", callback_data="cb_daily"),
            InlineKeyboardButton("❍ 𝐒𝐇𝐎𝐏 ❍", callback_data="cb_shop")
        ],
        [
            InlineKeyboardButton("❍ 𝐊𝐈𝐋𝐋 ❍", callback_data="cb_kill"),
            InlineKeyboardButton("❍ 𝐑𝐎𝐁 ❍", callback_data="cb_rob"),
            InlineKeyboardButton("❍ 𝐀𝐑𝐄𝐍𝐀 ❍", callback_data="cb_arena")
        ],
        [
            InlineKeyboardButton("❍ 𝐌𝐀𝐑𝐑𝐘 ❍", callback_data="cb_marry"),
            InlineKeyboardButton("❍ 𝐋𝐎𝐕𝐄 ❍", callback_data="cb_love"),
            InlineKeyboardButton("❍ 𝐂𝐎𝐔𝐏𝐋𝐄 ❍", callback_data="cb_couple")
        ],
        [
            InlineKeyboardButton("❍ 𝐂𝐇𝐀𝐓 ❍", callback_data="cb_chat"),
            InlineKeyboardButton("❍ 𝐃𝐑𝐀𝐖 ❍", callback_data="cb_draw"),
            InlineKeyboardButton("❍ 𝐒𝐏𝐄𝐀𝐊 ❍", callback_data="cb_speak")
        ],
        [
            InlineKeyboardButton("❍ 𝐖𝐎𝐑𝐃 ❍", callback_data="cb_word"),
            InlineKeyboardButton("❍ 𝐑𝐈𝐃𝐃𝐋𝐄 ❍", callback_data="cb_riddle"),
            InlineKeyboardButton("❍ 𝐒𝐋𝐎𝐓𝐒 ❍", callback_data="cb_slots")
        ],
        [
            InlineKeyboardButton("❍ 𝐏𝐈𝐍𝐆 ❍", callback_data="cb_ping"),
            InlineKeyboardButton("❍ 𝐒𝐓𝐀𝐓𝐒 ❍", callback_data="cb_stats"),
            InlineKeyboardButton("❍ 𝐖𝐄𝐋 ❍", callback_data="cb_wel")
        ],
        [
            InlineKeyboardButton("❍ 𝐆𝐈𝐕𝐄 ❍", callback_data="cb_give"),
            InlineKeyboardButton("❍ 𝐂𝐋𝐀𝐈𝐌 ❍", callback_data="cb_claim"),
            InlineKeyboardButton("❍ 𝐁𝐑𝐎𝐀𝐃 ❍", callback_data="cb_broad")
        ],
        [InlineKeyboardButton("⬅️ 𝐁𝐚𝐜𝐤", callback_data="start_return")]
    ])

# --- 🚀 START LOGIC ---

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
        f"❖ 𝐇𝐞𝐲 {get_mention(user)}\n"
        f"𝐈 𝐀𝐦 <b>{BOT_NAME}</b>\n"
        f"𝐓𝐡𝐞 𝐀𝐞𝐬𝐭𝐡𝐞𝐭𝐢𝐜 𝐀𝐈 𝐑𝐩𝐠 𝐆𝐚𝐦𝐞'𝐬 𝐁𝐨𝐭\n"
        f"━━━━━━━━━━━━━━━\n"
        f"🎮 <b>𝐅𝐞𝐚𝐭𝐮𝐫𝐞𝐬</b>\n"
        f"⚔️ 𝐑𝐩𝐠 : Kɪʟʟ • Rᴏʙ • Pʀᴏᴛᴇᴄᴛ\n"
        f"💞 𝐒𝐨𝐜𝐢𝐚𝐥 : Mᴀʀʀʏ • Wɪsʜᴇs • Lᴏᴠᴇ\n"
        f"💰 𝐄𝐜𝐨𝐧𝐨𝐦𝐲 : Sʜᴏᴘ • Dᴀɪʟʏ • Gɪ𝐯𝐞 • ᴄʟᴀɪᴍ\n"
        f"🤖 𝐀𝐈 : Cʜᴀᴛʙᴏᴛ • Aꜱᴋ Aɴʏᴛʜɪᴋ  • TTS\n"
        f"━━━━━━━━━━━━━━━\n"
        f"</blockquote>"
    )

    if update.callback_query:
        await update.callback_query.message.edit_caption(
            caption=caption, 
            reply_markup=get_start_keyboard(context.bot.username), 
            parse_mode=ParseMode.HTML
        )
    else:
        await update.message.reply_photo(
            photo=display_photo, caption=caption, 
            parse_mode=ParseMode.HTML, 
            reply_markup=get_start_keyboard(context.bot.username)
        )

# --- 🛠️ HELP CALLBACK LOGIC ---

async def help_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data

    # Aesthetic Bold Header
    header = (
        "<b>✶ <u>𝐇𝐄𝐋𝐏 𝐌𝐄𝐍𝐔</u> ✶</b>\n"
        "━━━━━━━━━━━━━━━\n"
        "<b>✶ 𝐂𝐇𝐎𝐎𝐒𝐄 𝐓𝐇𝐄 𝐁𝐔𝐓𝐓𝐎𝐍 𝐓𝐎 𝐒𝐄𝐄 𝐃𝐄𝐓𝐀𝐈𝐋𝐒.</b>\n\n"
        "<b>𝐀𝐋𝐋 𝐂𝐎𝐌𝐌𝐀𝐍𝐃𝐒 𝐖𝐎𝐑𝐊 𝐖𝐈𝐓𝐇 : /</b>"
    )

    # Dictionary for Alert Popups
    responses = {
        "cb_bal": "💰 𝐁𝐀𝐋: 𝐂𝐡𝐞𝐜𝐤 𝐲𝐨𝐮𝐫 𝐰𝐚𝐥𝐥𝐞𝐭 𝐚𝐧𝐝 𝐛𝐚𝐧𝐤 𝐛𝐚𝐥𝐚𝐧𝐜𝐞.",
        "cb_daily": "🎁 𝐃𝐀𝐈𝐋𝐘: 𝐂𝐥𝐚𝐢𝐦 𝐲𝐨𝐮𝐫 𝐝𝐚𝐢𝐥𝐲 𝐫𝐞𝐰𝐚𝐫𝐝 𝐜𝐨𝐢𝐧𝐬.",
        "cb_shop": "🛒 𝐒𝐇𝐎𝐏: 𝐁𝐮𝐲 𝐰𝐞𝐚𝐩𝐨𝐧𝐬, 𝐚𝐫𝐦𝐨𝐫, 𝐚𝐧𝐝 𝐠𝐞𝐚𝐫.",
        "cb_kill": "⚔️ 𝐊𝐈𝐋𝐋: 𝐀𝐭𝐭𝐚𝐜𝐤 𝐚 𝐮𝐬𝐞𝐫 𝐭𝐨 𝐰𝐢𝐧 𝐭𝐡𝐞𝐢𝐫 𝐥𝐨𝐨𝐭.",
        "cb_rob": "💸 𝐑𝐎𝐁: 𝐓𝐫𝐲 𝐭𝐨 𝐬𝐭𝐞𝐚𝐥 𝐦𝐨𝐧𝐞𝐲 𝐟𝐫𝐨𝐦 𝐨𝐭𝐡𝐞𝐫𝐬.",
        "cb_arena": "🏟️ 𝐀𝐑𝐄𝐍𝐀: 𝟏𝐯𝐬𝟏 𝐛𝐞𝐭𝐭𝐢𝐧𝐠 𝐟𝐢𝐠𝐡𝐭 𝐢𝐧 𝐭𝐡𝐞 𝐟𝐢𝐞𝐥𝐝.",
        "cb_marry": "💍 𝐌𝐀𝐑𝐑𝐘: 𝐏𝐫𝐨𝐩𝐨𝐬𝐞 𝐚𝐧𝐝 𝐥𝐢𝐧𝐤 𝐰𝐢𝐭𝐡 𝐚 𝐩𝐚𝐫𝐭𝐧𝐞𝐫.",
        "cb_love": "💖 𝐋𝐎𝐕𝐄: 𝐂𝐚𝐥𝐜𝐮𝐥𝐚𝐭𝐞 𝐧𝐚𝐦𝐞 𝐜𝐨𝐦𝐩𝐚𝐭𝐢𝐛𝐢𝐥𝐢𝐭𝐲 %.",
        "cb_couple": "👩‍❤️‍👨 𝐂𝐎𝐔𝐏𝐋𝐄: 𝐅𝐢𝐧𝐝 𝐭𝐡𝐞 𝐥𝐮𝐜𝐤𝐲 𝐦𝐚𝐭𝐜𝐡 𝐨𝐟 𝐭𝐡𝐞 𝐝𝐚𝐲.",
        "cb_chat": "🤖 𝐂𝐇𝐀𝐓: 𝐓𝐚𝐥𝐤 𝐭𝐨 𝐭𝐡𝐞 𝐬𝐦𝐚𝐫𝐭 𝐀𝐈 𝐜𝐡𝐚𝐭𝐛𝐨𝐭.",
        "cb_draw": "🎨 𝐃𝐑𝐀𝐖: 𝐆𝐞𝐧𝐞𝐫𝐚𝐭𝐞 𝐀𝐈 𝐢𝐦𝐚𝐠𝐞𝐬 𝐮𝐬𝐢𝐧𝐠 𝐅𝐥𝐮𝐱.",
        "cb_speak": "🎙️ 𝐒𝐏𝐄𝐀𝐊: 𝐂𝐨𝐧𝐯𝐞𝐫𝐭 𝐭𝐞𝐱𝐭 𝐢𝐧𝐭𝐨 𝐡𝐢𝐠𝐡-𝐪𝐮𝐚𝐥𝐢𝐭𝐲 𝐚𝐮𝐝𝐢𝐨.",
        "cb_word": "🧩 𝐖𝐎𝐑𝐃: 𝐏𝐥𝐚𝐲 𝐖𝐨𝐫𝐝𝐒𝐞𝐞𝐤 𝐠𝐚𝐦𝐞.",
        "cb_riddle": "🤔 𝐑𝐈𝐃𝐃𝐋𝐄: 𝐒𝐨𝐥𝐯𝐞 𝐩𝐮𝐳𝐳𝐥𝐞𝐬 𝐭𝐨 𝐞𝐚𝐫𝐧 𝐫𝐞𝐰𝐚𝐫𝐝𝐬.",
        "cb_slots": "🎰 𝐒𝐋𝐎𝐓𝐒: 𝐓𝐞𝐬𝐭 𝐲𝐨𝐮𝐫 𝐥𝐮𝐜𝐤 𝐨𝐧 𝐭𝐡𝐞 𝐬𝐩𝐢𝐧 𝐦𝐚𝐜𝐡𝐢𝐧𝐞.",
        "cb_ping": "📶 𝐏𝐈𝐍𝐆: 𝐂𝐡𝐞𝐜𝐤 𝐛𝐨𝐭 𝐫𝐞𝐬𝐩𝐨𝐧𝐬𝐞 𝐬𝐩𝐞𝐞𝐝.",
        "cb_stats": "📊 𝐒𝐓𝐀𝐓𝐒: 𝐒𝐞𝐞 𝐠𝐥𝐨𝐛𝐚𝐥 𝐛𝐨𝐭 𝐚𝐧𝐝 𝐮𝐬𝐞𝐫 𝐬𝐭𝐚𝐭𝐢𝐬𝐭𝐢𝐜𝐬.",
        "cb_wel": "👋 𝐖𝐄𝐋𝐂𝐎𝐌𝐄: 𝐌𝐚𝐧𝐚𝐠𝐞 𝐠𝐫𝐨𝐮𝐩 𝐠𝐫𝐞𝐞𝐭𝐢𝐧𝐠 𝐬𝐞𝐭𝐭𝐢𝐧𝐠𝐬.",
        "cb_give": "🤝 𝐆𝐈𝐕𝐄: 𝐓𝐫𝐚𝐧𝐬𝐟𝐞𝐫 𝐠𝐨𝐥𝐝 𝐭𝐨 𝐚𝐧𝐨𝐭𝐡𝐞𝐫 𝐮𝐬𝐞𝐫.",
        "cb_claim": "💎 𝐂𝐋𝐀𝐈𝐌: 𝐆𝐞𝐭 𝐲𝐨𝐮𝐫 𝐟𝐢𝐫𝐬𝐭-𝐭𝐢𝐦𝐞 𝐣𝐨𝐢𝐧 𝐛𝐨𝐧𝐮𝐬.",
        "cb_broad": "📢 𝐁𝐑𝐎𝐀𝐃: 𝐒𝐞𝐧𝐝 𝐚 𝐠𝐥𝐨𝐛𝐚𝐥 𝐦𝐞𝐬𝐬𝐚𝐠𝐞 (𝐀𝐝𝐦𝐢𝐧)."
    }

    if data == "help_main":
        await query.message.edit_caption(
            caption=header, reply_markup=get_21_bold_keyboard(), 
            parse_mode=ParseMode.HTML
        )
    elif data in responses:
        await query.answer(responses[data], show_alert=True)
    elif data == "start_return":
        await start(update, context)

    await query.answer()
