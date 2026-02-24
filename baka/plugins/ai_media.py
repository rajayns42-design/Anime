# Copyright (c) 2026 Telegram:- @WTF_Phantom <DevixOP>
import os
import random
import asyncio
import io
import urllib.parse
import httpx
from gtts import gTTS
from langdetect import detect
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from telegram.constants import ParseMode, ChatAction
from baka.utils import ensure_user_exists, get_mention

# --- IMAGE SETTINGS ---
MODEL = "flux-anime"

# Help Button Generator
def get_help_keyboard():
    keyboard = [[InlineKeyboardButton("❓ Help Menu", callback_data="help_menu")]]
    return InlineKeyboardMarkup(keyboard)

async def draw_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Generates AI Images and sends as a file to fix 'Wrong Type' error."""
    user = ensure_user_exists(update.effective_user)
    
    if not context.args:
        return await update.message.reply_text(
            "🎨 <b>Usage:</b> <code>/draw a cute cat girl</code>", 
            parse_mode=ParseMode.HTML,
            reply_markup=get_help_keyboard()
        )
    
    user_prompt = " ".join(context.args)
    base_prompt = f"{user_prompt}, anime style, masterpiece, best quality, ultra detailed, 8k, vibrant colors"
    encoded_prompt = urllib.parse.quote(base_prompt)
    
    msg = await update.message.reply_text("🎨 <b>Painting...</b>", parse_mode=ParseMode.HTML)
    
    try:
        seed = random.randint(0, 1000000)
        image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&seed={seed}&model={MODEL}&nologo=true"
        
        # Download image to memory (BytesIO)
        async with httpx.AsyncClient() as client:
            response = await client.get(image_url, timeout=40.0)
            if response.status_code != 200:
                raise Exception("AI Provider busy. Try again later.")
            
            image_data = io.BytesIO(response.content)
            image_data.name = "art.jpg"

        # Sending photo as a file buffer
        await context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=image_data,
            caption=f"🖼️ <b>Art by Angel</b>\n👤 {get_mention(user)}\n✨ <i>{user_prompt}</i>",
            parse_mode=ParseMode.HTML,
            reply_markup=get_help_keyboard()
        )
        await msg.delete()
        
    except Exception as e:
        # Error fix: added disable_web_page_preview to error messages
        await msg.edit_text(
            f"❌ <b>Error:</b> Generation failed.\n<code>{e}</code>", 
            parse_mode=ParseMode.HTML
        )

# --- TTS ENGINE ---
def _generate_audio_sync(text):
    try:
        lang_code = detect(text)
    except:
        lang_code = 'en'

    if lang_code == 'hi' or any(x in text.lower() for x in ['kaise', 'kya', 'hai', 'nhi', 'haan', 'bol', 'sun']):
        selected_lang, tld, voice_name = 'hi', 'co.in', "Indian Girl"
    elif lang_code == 'ja':
        selected_lang, tld, voice_name = 'ja', 'co.jp', "Anime Girl"
    else:
        selected_lang, tld, voice_name = 'en', 'us', "English Girl"

    audio_fp = io.BytesIO()
    tts = gTTS(text=text, lang=selected_lang, tld=tld, slow=False)
    tts.write_to_fp(audio_fp)
    audio_fp.seek(0)
    return audio_fp, voice_name

async def speak_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = " ".join(context.args)
    if not text and update.message.reply_to_message:
        text = update.message.reply_to_message.text or update.message.reply_to_message.caption
        
    if not text:
        return await update.message.reply_text(
            "🗣️ <b>Usage:</b> <code>/speak Hello</code>", 
            parse_mode=ParseMode.HTML,
            reply_markup=get_help_keyboard()
        )

    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.RECORD_VOICE)

    try:
        loop = asyncio.get_running_loop()
        audio_bio, voice_name = await loop.run_in_executor(None, _generate_audio_sync, text)
        
        await context.bot.send_voice(
            chat_id=update.effective_chat.id,
            voice=audio_bio,
            caption=f"🗣️ <b>Voice:</b> {voice_name}\n📝 <i>{text[:50]}...</i>",
            parse_mode=ParseMode.HTML,
            reply_markup=get_help_keyboard()
        )
    except Exception as e:
        await update.message.reply_text(f"❌ <b>Audio Error:</b> <code>{e}</code>", parse_mode=ParseMode.HTML)
