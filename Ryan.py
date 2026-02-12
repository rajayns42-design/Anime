import os
# --- CRITICAL FIX: MUST BE AT THE VERY TOP ---
os.environ["GIT_PYTHON_REFRESH"] = "quiet"
# ---------------------------------------------

from threading import Thread
from flask import Flask
from telegram import Update 
from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler, 
    ChatMemberHandler, MessageHandler, filters
)
from telegram.request import HTTPXRequest

# --- INTERNAL IMPORTS ---
from baka.utils import track_group, log_to_channel, BOT_NAME
from baka.config import TOKEN, PORT

# --- IMPORT ALL PLUGINS ---
from baka.plugins import (
    start, economy, game, admin, broadcast, fun, events, 
    welcome, ping, chatbot, riddle, social, ai_media, 
    waifu, collection, shop, daily, 
    mafia, wordseek 
)

# --- FLASK SERVER (Health Check) ---
app = Flask(__name__)

@app.route('/')
def health(): 
    return "Alive"

def run_flask(): 
    app.run(host='0.0.0.0', port=PORT, debug=False, use_reloader=False)

# --- STARTUP LOGIC ---
async def post_init(application):
    """Runs immediately after bot connects to Telegram."""
    print("✅ Bot connected! Setting menu commands...")

    await application.bot.set_my_commands([
        ("start", "🌸 Main Menu"), 
        ("word", "🎯 Start WordSeek"),
        ("hint", "💡 Get Hint (2/week)"),
        ("leaderboard", "🏆 WordSeek Ranking"),
        ("bal", "👛 Check Wallet"), 
        ("create_team", "🏢 Create Your Team"), 
        ("team_war", "⚔️ Start Team War"),
        ("team_leaderboard", "🏆 Top Mafia Teams"),
        ("ranking", "🏆 Global Leaderboard"), 
        ("daily", "📅 Daily Reward"),
        ("shop", "🛒 Item Shop"),
        ("ping", "📶 Status"),
        ("update", "🔄 Update Bot"),
    ])

    try:
        bot_info = await application.bot.get_me()
        print(f"✅ Logged in as {bot_info.username}")
    except Exception as e:
        print(f"⚠️ Startup Log Failed: {e}")

# --- MAIN EXECUTION ---
if __name__ == '__main__':
    flask_thread = Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()

    if not TOKEN:
        print("CRITICAL: BOT_TOKEN is missing.")
    else:
        t_request = HTTPXRequest(connection_pool_size=16, connect_timeout=60.0, read_timeout=60.0)
        app_bot = ApplicationBuilder().token(TOKEN).request(t_request).post_init(post_init).build()

        # ================= REGISTER HANDLERS =================

        # --- 1. Basics & Admin ---
        app_bot.add_handler(CommandHandler("start", start.start))
        app_bot.add_handler(CommandHandler("ping", ping.ping))
        app_bot.add_handler(CommandHandler("broadcast", broadcast.broadcast))
        app_bot.add_handler(CommandHandler("update", admin.update_bot))

        # --- 2. WordSeek Game (Commands) ---
        app_bot.add_handler(CommandHandler("word", wordseek.start_game))
        app_bot.add_handler(CommandHandler("hint", wordseek.get_hint))
        app_bot.add_handler(CommandHandler("leaderboard", wordseek.leaderboard))

        # --- 3. Economy & RPG ---
        app_bot.add_handler(CommandHandler("bal", economy.balance))
        app_bot.add_handler(CommandHandler("daily", daily.daily))
        app_bot.add_handler(CommandHandler("shop", shop.shop_menu))
        app_bot.add_handler(CommandHandler("kill", game.kill))

        # --- 4. 🕶️ MAFIA / TEAM SYSTEM (Added Missing Handlers) ---
        app_bot.add_handler(CommandHandler("create_team", mafia.create_team))
        app_bot.add_handler(CommandHandler("join_team", mafia.join_team))
        app_bot.add_handler(CommandHandler("promote_member", mafia.promote_member))
        app_bot.add_handler(CommandHandler("kick_member", mafia.kick_member))
        app_bot.add_handler(CommandHandler("leave_team", mafia.leave_team))
        app_bot.add_handler(CommandHandler("t_deposit", mafia.team_deposit))
        app_bot.add_handler(CommandHandler("t_withdraw", mafia.team_withdraw))
        app_bot.add_handler(CommandHandler("team_war", mafia.team_war))
        app_bot.add_handler(CommandHandler("arena", mafia.arena_fight))
        app_bot.add_handler(CommandHandler("team_leaderboard", mafia.team_leaderboard))

        # --- 5. LISTENERS & MESSAGE HANDLERS ---

        # Priority Group 0: WordSeek Guesses (High Priority)
        app_bot.add_handler(MessageHandler(
            filters.TEXT & filters.ChatType.GROUPS & ~filters.COMMAND, 
            wordseek.guess
        ), group=0)

        # Priority Group 1: Waifu Collection
        app_bot.add_handler(MessageHandler(
            filters.TEXT & filters.ChatType.GROUPS & ~filters.COMMAND, 
            collection.collect_waifu
        ), group=1)

        # Priority Group 4: Chatbot AI (Low Priority)
        app_bot.add_handler(MessageHandler(
            (filters.TEXT | filters.Sticker.ALL) & ~filters.COMMAND, 
            chatbot.ai_message_handler
        ), group=4)

        # Status Updates & Events
        app_bot.add_handler(ChatMemberHandler(events.chat_member_update, ChatMemberHandler.MY_CHAT_MEMBER))
        app_bot.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome.new_member))
        app_bot.add_handler(MessageHandler(filters.ChatType.GROUPS, events.group_tracker), group=5)

        print(f"🚀 {BOT_NAME} is LIVE with Mafia & WordSeek!")
        app_bot.run_polling(allowed_updates=Update.ALL_TYPES, drop_pending_updates=True)
