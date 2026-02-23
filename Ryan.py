# Copyright (c) 2026 Telegram:- @WTF_Phantom <DevixOP>
# Final Master Main for ZEXX - Handlers Only Version

import os
os.environ["GIT_PYTHON_REFRESH"] = "quiet"

from threading import Thread
from flask import Flask
from telegram import Update, BotCommand
from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler,
    ChatMemberHandler, MessageHandler, filters
)
from telegram.request import HTTPXRequest

# --- INTERNAL UTILS ---
from baka.utils import track_group, log_to_channel, BOT_NAME
from baka.config import TOKEN, PORT

# --- ALL PLUGINS SYNCED ---
from baka.plugins import (
    start, economy, game, admin, broadcast, fun, events,
    welcome, ping, chatbot, riddle, social, ai_media,
    waifu, collection, shop, daily,
    mafia, wordseek, wishes, couple, love, battle
)

# ---------------- FLASK (Stay Alive) ----------------
app = Flask(__name__)
@app.route('/')
def health(): return f"{BOT_NAME} is Alive!"
def run_flask(): app.run(host='0.0.0.0', port=PORT, debug=False, use_reloader=False)

# ---------------- STARTUP LOGS & MENU SETTING ----------------
async def post_init(application):
    # Registration of ALL 35+ commands for the Telegram Menu
    bot_commands = [
        BotCommand("start", "Tᴀʟᴋᴇ Tᴏ Aɴɢᴇʟ"),
        BotCommand("ping", "Cʜᴇᴋ ʏᴏᴜʀ Aɴɢᴇʟ Sᴩᴇᴇᴅ"),
        BotCommand("help", "Aɴɢᴇʟ Hᴇʟᴩ Mᴇɴᴜ"),
        BotCommand("bal", "Yᴏᴜʀ Wᴀʟʟᴇᴛ"),
        BotCommand("daily", "Aɴɢᴇʟ Dᴀɪʟʏ Rᴇᴡᴀʀᴅ"),
        BotCommand("shop", "Aɴɢᴇʟ Sʜᴏᴩ Mᴇɴᴜ"),
        BotCommand("pay", "Sᴇɴᴅ Fʀɪᴇᴅꜱ Mᴏɴᴇʏ"),
        BotCommand("kill", "Kɪʟʟ Yᴏᴜʀ ᴀɴʏᴏɴᴇ"),
        BotCommand("rob", "Rᴏʙ To Soᴍᴇᴏɴᴇ"),
        BotCommand("dice", "Pʟᴀʏ Tʜᴇ Dɪᴄᴇ Gᴀᴍᴇ"),
        BotCommand("draw", "Dʀᴀᴡ Pɪᴄʜᴀʀ Iɴ Gʀᴏᴜᴩꜱ"),
        BotCommand("waifu", "Gᴇᴛ Yᴏᴜʀ Fᴠ Wᴀɪꜰᴜ"),
        BotCommand("chatbot", "Aɴɢᴇʟ Aɪ Sᴇᴛᴛɪɴɢꜱ"),
        BotCommand("ask", "Aꜱᴋ Aɴʏᴛʜɪᴋ"),
        BotCommand("welcome", "Wᴇʟᴄᴏᴍᴇ Oɴ/Oғғ"),
        BotCommand("truth", "Lᴏᴠᴇ Tʀᴜᴛʜ"),
        BotCommand("dare", "Lᴏᴠᴇ Dᴀʀᴇ"),
        BotCommand("quiz", "Lᴏᴠᴇ Qᴜɪᴢ"),
        BotCommand("battle", "Cʙ Gᴀᴍᴇꜱ"),
        BotCommand("battlelb", "Cʙ- Lᴇᴀᴅᴇʀʙᴏᴀʀᴅ"),
        BotCommand("marry", "Pʀᴏꜱᴇ ʏᴏᴜʀ ɢʀɪʀꜰʀɪᴇɴᴅ"),
        BotCommand("update", "Uᴩᴅᴀᴛᴇ Bᴏᴛ"),
        BotCommand("protect", "Pʀᴏᴛᴇᴄᴛ Yᴏᴜʀ ɪᴅ"),
        BotCommand("word", "Pʟᴀʏ Wᴏʀᴅꜱᴇᴇᴋ"),
        BotCommand("wleaderboard", "W-Gʟᴏʙᴀʟ ʟ-ʙᴏᴀʀᴅ"),
        BotCommand("top", "Gʟᴏʙᴀʟ Rᴀɴᴋɪɴɢ"),
        BotCommand("speak", "Sᴩᴇᴀᴋ Wɪᴛʜ Aɴɢʟ"),
        BotCommand("love", "Yᴏᴜʀ Lᴏᴠᴇ % Wɪᴛʜ Lᴏʏᴇʟᴛɪ Cʜᴇᴋ"),
        BotCommand("couple", "Cᴏᴜᴩʟᴇ Rᴏʟʟ Wɪᴛʜ Yᴏᴜʀ Lᴏᴠᴇ"),
        BotCommand("propose", "Pʀᴏᴩᴏꜱᴇ Yᴜʀ Gꜰ & Wɪꜰᴇ"),
        BotCommand("divorce", "Dɪᴠᴏʀꜱᴇ Wɪᴛʜ Gꜰ & Wɪꜰe"),
        BotCommand("create_team", "Cʀᴇᴀᴛ Yᴏᴜʀ Gᴀɴɢ"),
        BotCommand("join_team", "Jᴏɪɴ Yᴏᴜʀ Mᴀꜰɪᴀ Tᴇᴀᴍ"),
        BotCommand("mpromote", "Pʀᴏᴍɪᴛᴇ ᴍᴀꜰɪᴀ ᴍᴇᴍʙᴀʀ"),
        BotCommand("team_war", "Cʀᴇᴀᴛ Tᴇᴀᴍ & Aᴛᴀᴄᴋ"),
        BotCommand("mafialb", "M-Lᴇᴀᴅᴇʀʙᴏᴀʀᴅ"),
        BotCommand("riddle", "Rɪᴅᴅʟᴇ Wɪᴛʜ Fʀɪᴇɴᴅ"),
        BotCommand("arena", "Pʟᴀʏ ᴛʜᴇ Aʀᴇɴᴀ")
    ]
    await application.bot.set_my_commands(bot_commands)
    await log_to_channel(application.bot, "start")

# ---------------- THE MASTER MAIN ----------------
if __name__ == '__main__':
    Thread(target=run_flask, daemon=True).start()

    request = HTTPXRequest(connection_pool_size=20)
    app_bot = ApplicationBuilder().token(TOKEN).request(request).post_init(post_init).build()

    # ========= 1. CORE & ADMIN =========
    app_bot.add_handler(CommandHandler("start", start.start))
    app_bot.add_handler(CommandHandler("ping", ping.ping))
    app_bot.add_handler(CommandHandler("help", start.start))
    app_bot.add_handler(CommandHandler("update", admin.update_bot))
    app_bot.add_handler(CommandHandler("broadcast", broadcast.broadcast))

    # ========= 2. ECONOMY & REWARDS =========
    app_bot.add_handler(CommandHandler("bal", economy.balance))
    app_bot.add_handler(CommandHandler("top", economy.ranking))
    app_bot.add_handler(CommandHandler("daily", daily.daily))
    app_bot.add_handler(CommandHandler("pay", economy.give))
    app_bot.add_handler(CommandHandler("shop", shop.shop_menu))
    app_bot.add_handler(CommandHandler("buy", shop.buy))

    # ========= 3. RPG & BATTLE SYSTEM =========
    app_bot.add_handler(CommandHandler("battle", battle.battle_system))
    app_bot.add_handler(CommandHandler("battlelb", battle.battle_leaderboard))
    app_bot.add_handler(CommandHandler("arena", mafia.arena_fight))
    app_bot.add_handler(CommandHandler("kill", game.kill))
    app_bot.add_handler(CommandHandler("rob", game.rob))
    app_bot.add_handler(CommandHandler("protect", game.protect))

    # ========= 4. MAFIA TEAM SYSTEM =========
    app_bot.add_handler(CommandHandler("create_team", mafia.create_team))
    app_bot.add_handler(CommandHandler("join_team", mafia.join_team))
    app_bot.add_handler(CommandHandler("mpromote", mafia.promote_member))
    app_bot.add_handler(CommandHandler("team_war", mafia.team_war))
    app_bot.add_handler(CommandHandler("mafialb", mafia.leaderboard))

    # ========= 5. SOCIAL & WAIFU =========
    app_bot.add_handler(CommandHandler("marry", social.propose))
    app_bot.add_handler(CommandHandler("couple", couple.couple_roll))
    app_bot.add_handler(CommandHandler("love", love.love_command)) 
    app_bot.add_handler(CommandHandler("propose", social.propose))
    app_bot.add_handler(CommandHandler("divorce", social.divorce))
    app_bot.add_handler(CommandHandler("waifu", waifu.waifu_action))
    app_bot.add_handler(CommandHandler("truth", fun.truth))
    app_bot.add_handler(CommandHandler("dare", fun.dare))
    app_bot.add_handler(CommandHandler("quiz", fun.quiz))

    # ========= 6. AI & MEDIA =========
    app_bot.add_handler(CommandHandler("chatbot", chatbot.chatbot_toggle)) 
    app_bot.add_handler(CommandHandler("ask", chatbot.ask_ai))
    app_bot.add_handler(CommandHandler("speak", ai_media.speak_command))
    app_bot.add_handler(CommandHandler("draw", ai_media.draw_command))

    # ========= 7. GAMES & FUN =========
    app_bot.add_handler(CommandHandler("word", wordseek.start_game))
    app_bot.add_handler(CommandHandler("wleaderboard", wordseek.leaderboard))
    app_bot.add_handler(CommandHandler("riddle", riddle.riddle_command))
    app_bot.add_handler(CommandHandler("dice", fun.dice)) 
    app_bot.add_handler(CommandHandler("welcome", welcome.welcome_toggle))

    # ========= 8. CALLBACK HANDLERS (HELP BUTTON SUPPORT) =========
    app_bot.add_handler(CallbackQueryHandler(start.help_callback, pattern="^(start_|help_|return_|cb_|help_menu)"))
    app_bot.add_handler(CallbackQueryHandler(shop.shop_callback, pattern="^shop_"))
    app_bot.add_handler(CallbackQueryHandler(social.proposal_callback, pattern="^marry_"))

    # ========= 9. MESSAGE LISTENERS (PRIORITY GROUPS) =========
    app_bot.add_handler(MessageHandler(filters.TEXT & filters.ChatType.GROUPS & ~filters.COMMAND, wordseek.guess), group=0)
    app_bot.add_handler(MessageHandler(filters.ChatType.GROUPS, events.group_tracker), group=1)
    app_bot.add_handler(MessageHandler(filters.TEXT & filters.ChatType.GROUPS & ~filters.COMMAND, collection.check_drops), group=2)
    app_bot.add_handler(MessageHandler(filters.TEXT & filters.ChatType.GROUPS & ~filters.COMMAND, collection.collect_waifu), group=3)
    app_bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, riddle.check_riddle_answer), group=4)
    app_bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, wishes.wishes_handler), group=5)
    app_bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chatbot.ai_message_handler), group=6)

    # ========= 10. SYSTEM EVENTS =========
    app_bot.add_handler(ChatMemberHandler(events.chat_member_update))
    app_bot.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome.new_member))

    # Final Launch
    print(f"✅ {BOT_NAME} DEPLOYED WITH ALL COMMANDS & HELP MENU!")
    app_bot.run_polling(allowed_updates=Update.ALL_TYPES, drop_pending_updates=True)
