# Copyright (c) 2026 Telegram:- @WTF_Phantom <DevixOP>
# Professional Multi-Module Dashboard for ZEXX - Full Help Integrated

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
            InlineKeyboardButton("⌯ 𝐇𝐀𝐑𝐈 ⌯", url=OWNER_LINK)
        ],
        [
            InlineKeyboardButton("📩 Uᴩᴅᴀᴛᴇ", url="https://t.me/Love_bot_143"), 
            InlineKeyboardButton("📩 Sᴜᴩᴩᴏʀᴛ", url="https://t.me/Love_Ki_Duniyaa")
        ]
    ])

def get_21_bold_keyboard():
    # Grid of 24 Buttons (Including Battle & Leaderboard)
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
            InlineKeyboardButton("⚔️ 𝐁𝐀𝐓𝐓𝐋𝐄 ⚔️", callback_data="cb_battle"),
            InlineKeyboardButton("🏆 𝐓𝐎𝐏 🏆", callback_data="cb_battlelb"),
            InlineKeyboardButton("❍ 𝐂𝐎𝐔𝐏𝐋𝐄 ❍", callback_data="cb_couple")
        ],
        [
            InlineKeyboardButton("❍ 𝐌𝐀𝐑𝐑𝐘 ❍", callback_data="cb_marry"),
            InlineKeyboardButton("❍ 𝐋𝐎𝐕𝐄 ❍", callback_data="cb_love"),
            InlineKeyboardButton("❍ 𝐂𝐇𝐀𝐓 ❍", callback_data="cb_chat")
        ],
        [
            InlineKeyboardButton("❍ 𝐃𝐑𝐀𝐖 ❍", callback_data="cb_draw"),
            InlineKeyboardButton("❍ 𝐒𝐏𝐄𝐀𝐊 ❍", callback_data="cb_speak"),
            InlineKeyboardButton("❍ 𝐖𝐎𝐑𝐃 ❍", callback_data="cb_word")
        ],
        [
            InlineKeyboardButton("❍ 𝐑𝐈𝐃𝐃𝐋𝐄 ❍", callback_data="cb_riddle"),
            InlineKeyboardButton("❍ 𝐒𝐋𝐎𝐓𝐒 ❍", callback_data="cb_slots"),
            InlineKeyboardButton("❍ 𝐏𝐈𝐍𝐆 ❍", callback_data="cb_ping")
        ],
        [
            InlineKeyboardButton("❍ 𝐒𝐓𝐀𝐓𝐒 ❍", callback_data="cb_stats"),
            InlineKeyboardButton("❍ 𝐖𝐄𝐋 ❍", callback_data="cb_wel"),
            InlineKeyboardButton("❍ 𝐆𝐈𝐕𝐄 ❍", callback_data="cb_give")
        ],
        [
            InlineKeyboardButton("❍ 𝐂𝐋𝐀𝐈𝐌 ❍", callback_data="cb_claim"),
            InlineKeyboardButton("❍ 𝐁𝐑𝐎𝐀𝐃 ❍", callback_data="cb_broad"),
            InlineKeyboardButton("🆘 𝐇𝐄𝐋𝐏", callback_data="cb_help_guide")
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
        f"⚔️ 𝐑𝐩𝐠 : Kɪʟʟ • Rᴏʙ • Bᴀᴛᴛʟᴇ\n"
        f"💞 𝐒𝐨𝐜𝐢𝐚𝐥 : Mᴀʀʀʏ • Lᴏᴠᴇ • Cᴏᴜᴘʟᴇ\n"
        f"💰 𝐄𝐜𝐨𝐧𝐨𝐦𝐲 : Sʜᴏᴘ • Dᴀɪʟ𝐲 • Gɪ𝐯𝐞\n"
        f"🤖 𝐀𝐈 : Cʜᴀᴛʙᴏᴛ • Dʀᴀᴡ • Sᴘᴇᴀᴋ\n"
        f"━━━━━━━━━━━━━━━\n"
        f"💭 Pʀᴇꜱʜ Tᴏ Hᴇʟᴩ Bᴜᴛᴛᴏɴ\n"
f"Aɴᴅ Sᴇᴇ Aʟʟ Fᴇᴀᴛᴜʀᴇ & Uꜱᴇ Wɪᴛʜ ./\n"
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

    header = (
        "<b>✶ <u>𝐇𝐄𝐋𝐏 𝐌𝐄𝐍𝐔</u> ✶</b>\n"
        "━━━━━━━━━━━━━━━\n"
        "<b>✶ 𝐂𝐇𝐎𝐎𝐒𝐄 𝐀 𝐁𝐔𝐓𝐓𝐎𝐍 𝐅𝐎𝐑 𝐂𝐎𝐌𝐌𝐀𝐍𝐃 𝐈𝐍𝐅𝐎.</b>\n\n"
        "<b>𝐀𝐋𝐋 𝐂𝐎𝐌𝐌𝐀𝐍𝐃𝐒 𝐖𝐎𝐑𝐊 𝐖𝐈𝐓𝐇 : /</b>"
    )

    responses = {
        "cb_bal": "💰 𝐁𝐀𝐋: Check your wallet and bank balance.",
        "cb_daily": "🎁 𝐃𝐀𝐈𝐋𝐘: Claim your daily reward coins.",
        "cb_shop": "🛒 𝐒𝐇𝐎𝐏: Buy weapons, armor, and gear.",
        "cb_kill": "⚔️ 𝐊𝐈𝐋𝐋: Attack a user to win their loot.",
        "cb_rob": "💸 𝐑𝐎𝐁: Try to steal money from others.",
        "cb_arena": "🏟️ 𝐀𝐑𝐄𝐍𝐀: 1vs1 betting fight in the field.",
        "cb_battle": "🤺 𝐁𝐀𝐓𝐓𝐋𝐄: Unlimited 1vs1 fight with a reply.",
        "cb_battlelb": "🏆 𝐓𝐎𝐏: See the global battle leaderboard.",
        "cb_marry": "💍 𝐌𝐀𝐑𝐑𝐘: Propose and link with a partner.",
        "cb_love": "💖 𝐋𝐎𝐕𝐄: Calculate name compatibility %.",
        "cb_couple": "👩‍❤️‍👨 𝐂𝐎𝐔𝐏𝐋𝐄: Find the lucky match of the day.",
        "cb_chat": "🤖 𝐂𝐇𝐀𝐓: Talk to the smart AI chatbot.",
        "cb_draw": "🎨 𝐃𝐑𝐀𝐖: Generate AI images using Flux.",
        "cb_speak": "🎙️ 𝐒𝐏𝐄𝐀𝐊: Convert text into audio.",
        "cb_word": "🧩 𝐖𝐎𝐑𝐃: Play WordSeek game in group.",
        "cb_riddle": "🤔 𝐑𝐈𝐃𝐃𝐋𝐄: Solve puzzles for rewards.",
        "cb_slots": "🎰 𝐒𝐋𝐎𝐓𝐒: Test your luck on the machine.",
        "cb_ping": "📶 𝐏𝐈𝐍𝐆: Check bot response speed.",
        "cb_stats": "📊 𝐒𝐓𝐀𝐓𝐒: See global bot statistics.",
        "cb_wel": "👋 𝐖𝐄𝐋𝐂𝐎𝐌𝐄: Manage group greeting settings.",
        "cb_give": "🤝 𝐆𝐈𝐕𝐄: Transfer gold to another user.",
        "cb_claim": "💎 𝐂𝐋𝐀𝐈𝐌: Get your first-time join bonus.",
        "cb_broad": "📢 𝐁𝐑𝐎𝐀𝐃: Send global message (Admin).",
        "cb_help_guide": "🆘 𝐆𝐔𝐈𝐃𝐄: Use /help for this menu anytime!"
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

    try: await query.answer()
    except: pass
