import os
import random
from datetime import datetime
from PIL import Image, ImageDraw, ImageOps
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from io import BytesIO

# --- 🛠️ UTILS: Photo ko Gol (Circle) Katne Ke Liye ---
def make_circle(img):
    size = (300, 300)
    mask = Image.new('L', size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + size, fill=255)
    output = ImageOps.fit(img, size, centering=(0.5, 0.5))
    output.putalpha(mask)
    return output

# --- 💘 MAIN COMMAND: /couple ---
async def couple_roll(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.effective_message
    user1 = update.effective_user
    
    # Check if reply exists
    if not msg.reply_to_message:
        return await msg.reply_text("<b>Abe akele jodi banaoge?</b> 😂\nKisi ke message pe <code>/couple</code> reply karo!", parse_mode=ParseMode.HTML)

    user2 = msg.reply_to_message.from_user
    if user1.id == user2.id:
        return await msg.reply_text("Apne aap se hi ishq? Itne bure din aa gaye kya? 💀")

    sent_msg = await msg.reply_text("📸 <b>Dono ki profile photos frame mein set kar rahi hoon... ❤️</b>", parse_mode=ParseMode.HTML)

    try:
        # Photos Download Karo
        p1 = await context.bot.get_user_profile_photos(user1.id)
        p2 = await context.bot.get_user_profile_photos(user2.id)

        async def download_pic(photos):
            if photos.total_count > 0:
                file = await context.bot.get_file(photos.photos[0][-1].file_id)
                b = await file.download_as_bytearray()
                return Image.open(BytesIO(b))
            # Default Gray Image if no DP
            return Image.new('RGB', (300, 300), color=(200, 200, 200))

        img1 = make_circle(await download_pic(p1))
        img2 = make_circle(await download_pic(p2))

        # Canvas Design (Transparent Background)
        canvas = Image.new('RGBA', (800, 400), (0, 0, 0, 0))
        canvas.paste(img1, (50, 50), img1)
        canvas.paste(img2, (450, 50), img2)

        output = BytesIO()
        canvas.save(output, format='PNG')
        output.seek(0)

        # Matching Logic
        perc = random.randint(1, 100)
        if perc > 90: status = "Heer-Ranjha Level! ❤️✨"
        elif perc > 75: status = "Chat-Pati Jodi! 🔥"
        elif perc > 50: status = "Nibba-Nibbi Vibes! 🤡"
        elif perc > 25: status = "Zabardasti ki Jodi! 😂"
        else: status = "Kattne wala hai tera! 💀"

        # Buttons
        keyboard = [[InlineKeyboardButton("Shadi Karo 💍", callback_data=f"marry_{user1.id}_{user2.id}")]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        caption = (
            f"<b>💞 ZEXX JODI FINDER 💞</b>\n"
            f"<code>━━━━━━━━━━━━━━━━━━</code>\n"
            f"🤵 <b>{user1.first_name}</b>\n"
            f"      <b>✖️</b>\n"
            f"👰 <b>{user2.first_name}</b>\n\n"
            f"📊 <b>Matching:</b> <code>{perc}%</code>\n"
            f"✨ <b>Verdict:</b> <i>{status}</i>\n"
            f"<code>━━━━━━━━━━━━━━━━━━</code>\n"
            f"👉 <i>Neeche button dabao shadi fix karne ke liye!</i>"
        )

        await msg.reply_photo(photo=output, caption=caption, reply_markup=reply_markup, parse_mode=ParseMode.HTML)
        await sent_msg.delete()

    except Exception as e:
        await sent_msg.edit_text(f"Galti ho gayi: {e}")

# --- 💍 CALLBACK: Marriage System ---
async def marriage_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data.split("_")
    u1_id, u2_id = int(data[1]), int(data[2])
    
    # Check if only the couple clicks
    if query.from_user.id not in [u1_id, u2_id]:
        return await query.answer("Abe tumhari shaadi nahi ho rahi, beech mein mat bolo! 🤫", show_alert=True)

    date = datetime.now().strftime("%d %B, %Y")
    
    certificate_text = (
        f"<b>📜 REGISTRAR OF  LOVERS 📜</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"<b>Gawahon ki maujoodgi mein ye elaan kiya jata hai:</b>\n\n"
        f"🤵 <b>Dulha:</b> <a href='tg://user?id={u1_id}'>Pati Dev</a>\n"
        f"👰 <b>Dulhan:</b> <a href='tg://user?id={u2_id}'>Patni Devi</a>\n\n"
        f"Aaj tareekh <b>{date}</b> ko in dono ne ek dusre ko kabool kiya. ✨\n\n"
        f"<b>📝 Shartein (Rules):</b>\n"
        f"• Roz 'GM/GN Babu' bolna zaroori hai.\n"
        f"• Ladai hone par ladka hi sorry bolega.\n"
        f"• Dusri waifu dekhna sakht mana hai! 🚫\n\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"🎊 <b>MUBARAK HO! SHAADI PAKKI!</b> 🎊"
    )

    await query.message.edit_caption(caption=certificate_text, parse_mode=ParseMode.HTML, reply_markup=None)
    await query.answer("Mubarak Ho! Shaadi ho gayi! 💍🎉")
