# Copyright (c) 2026 Telegram:- @WTF_Phantom <DevixOP>
# Professional Multi-Module Dashboard for ZEXX (Final Version)

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from baka.config import BOT_NAME, START_IMG_URL, OWNER_LINK
from baka.utils import get_mention, ensure_user_exists

# --- ⌨️ KEYBOARDS ---

def get_start_keyboard(bot_username):
    # Image jaisa layout setup
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("➕ 𝐀𝐝𝐝 𝐌𝐞 𝐁𝐚𝐛𝐲 ➕", url=f"https://t.me/{bot_username}?startgroup=true")],
        [
            InlineKeyboardButton("🥀 𝐁𝐨𝐨𝐤", callback_data="help_main"), 
            InlineKeyboardButton("⦗ 𝐇𝐚𝐫𝐢 ⦘", url=OWNER_LINK)
        ],
        [
            InlineKeyboardButton("📩 𝐔𝐩𝐝𝐚𝐭𝐞", url="https://t.me/ZexxUpdates"), 
            InlineKeyboardButton("📩 𝐒𝐮𝐩𝐩𝐨𝐫𝐭", url="https://t.me/ZexxSupport")
        ]
    ])

def get_help_keyboard():
    # 21 files ka data in 6 categories mein distribute kiya gaya hai
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("⚔️ RPG & Mᴀꜰɪᴀ", callback_data="h_rpg"), 
            InlineKeyboardButton("💰 Eᴄᴏɴᴏᴍʏ", callback_data="h_eco")
        ],
        [
            InlineKeyboardButton("💞 Sᴏᴄɪᴀʟ", callback_data="h_soc"), 
            InlineKeyboardButton("🤖 AI & Cʜᴀᴛ", callback_data="h_ai")
        ],
        [
            InlineKeyboardButton("🎮 Gᴀᴍᴇꜱ", callback_data="h_gam"), 
            InlineKeyboardButton("🛡️ Sʏꜱᴛᴇᴍ", callback_data="h_sys")
        ],
        [InlineKeyboardButton("⬅️ Bᴀᴄᴋ Tᴏ Hᴏᴍᴇ", callback_data="start_return")]
    ])

# --- 🚀 START COMMAND ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    ensure_user_exists(user)
    
    # User ki DP lene ki koshish, warna config image
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
        f"💰 𝐄𝐜𝐨𝐧𝐨𝐦𝐲 : Sʜᴏᴘ • Dᴀɪʟʏ • Gɪᴠᴇ\n"
        f"🤖 𝐀𝐈 : Cʜᴀᴛʙᴏᴛ • Dʀᴀᴡ • TTS\n"
        f"━━━━━━━━━━━━━━━\n"
        f"💭 𝐏𝐫𝐞𝐬𝐬 𝐇𝐞𝐥𝐩 𝐁𝐮𝐭𝐭𝐨𝐧\n"
        f"𝐒𝐞𝐞 𝐀𝐥𝐥 𝐅𝐞𝐚𝐭𝐮𝐫𝐞𝐬 & 𝐔𝐬𝐞 𝐖𝐢𝐭𝐡 ./\n"
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
            photo=display_photo, 
            caption=caption, 
            parse_mode=ParseMode.HTML, 
            reply_markup=get_start_keyboard(context.bot.username)
        )

# --- 🛠️ HELP CALLBACKS (All 21 Plugins Data) ---

async def help_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data
    
    # Har section ke liye detailed command list
    help_texts = {
        "help_main": (
            f"<b>📚 {BOT_NAME} Hᴇʟᴩ Gᴜɪᴅᴇ</b>\n\n"
            f"Hᴇʏ {get_mention(query.from_user)}, niche di gayi categories se meri sari 21 commands seekhein! ✨"
        ),
        "h_rpg": (
            f"<b>⚔️ RPG & Mᴀꜰɪᴀ Sʏꜱᴛᴇᴍ</b>\n\n"
            f"• <code>/create_team</code> : Start gang.\n"
            f"• <code>/team_war</code> : Battle other teams.\n"
            f"• <code>/kill</code> : Eliminate target.\n"
            f"• <code>/rob</code> : Steal target's balance.\n"
            f"• <code>/protect</code> : Buy 1D/2D shield.\n"
            f"• <code>/arena</code> : 1vs1 Betting fight."
        ),
        "h_eco": (
            f"<b>💰 Eᴄᴏɴᴏᴍʏ & Sʜᴏᴩ</b>\n\n"
            f"• <code>/bal</code> : View wallet & bank.\n"
            f"• <code>/daily</code> : Daily reward streak.\n"
            f"• <code>/shop</code> : Buy weapons & armor.\n"
            f"• <code>/buy [id]</code> : Fast item purchase.\n"
            f"• <code>/give</code> : Transfer coins to user.\n"
            f"• <code>/claim</code> : First time group bonus."
        ),
        "h_soc": (
            f"<b>💞 Sᴏᴄɪᴀʟ & Rᴏᴍᴀɴᴄᴇ</b>\n\n"
            f"• <code>/propose</code> : Marry a user.\n"
            f"• <code>/divorce</code> : End relationship.\n"
            f"• <code>/couple</code> : Match of the day.\n"
            f"• <code>/love</code> : Name compatibility.\n"
            f"• <code>hug, kiss, slap</code> : 30+ Social actions.\n"
            f"• <code>gm, gn, ilu</code> : Auto wishes support."
        ),
        "h_ai": (
            f"<b>🤖 AI & Cʜᴀᴛʙᴏᴛ</b>\n\n"
            f"• <b>Smart Chat</b> : Direct message replies.\n"
            f"• <code>/draw</code> : Generate AI images (Flux).\n"
            f"• <code>/speak</code> : High quality Text-to-Speech.\n"
            f"• <b>Mistral Brain</b> : Lifetime memory AI."
        ),
        "h_gam": (
            f"<b>🎮 Gᴀᴍᴇꜱ & Pᴜᴢᴢʟᴇꜱ</b>\n\n"
            f"• <code>/word</code> : WordSeek (Wordle style).\n"
            f"• <code>/riddle</code> : Tricky puzzles for rewards.\n"
            f"• <code>/dice</code> : Native betting game.\n"
            f"• <code>/slots</code> : Classic slot machine.\n"
            f"• <code>/wlb</code> : WordSeek leaderboard."
        ),
        "h_sys": (
            f"<b>🛡️ Sʏꜱᴛᴇᴍ & Mᴀɴᴀɢᴇᴍᴇɴᴛ</b>\n\n"
            f"• <code>/ping</code> : Latency & Server health.\n"
            f"• <code>/stats</code> : Global user database stats.\n"
            f"• <code>/welcome</code> : Enable/Disable greetings.\n"
            f"• <code>/broadcast</code> : Owner only global alert.\n"
            f"• <b>Watcher</b> : Log join/leave events."
        )
    }

    if data == "start_return":
        await start(update, context)
    elif data in help_texts:
        await query.message.edit_caption(
            caption=help_texts[data], 
            reply_markup=get_help_keyboard(), 
            parse_mode=ParseMode.HTML
        )
    
    await query.answer()
