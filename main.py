from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

import os

BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")

app = Flask(__name__)
bot_app = ApplicationBuilder().token(BOT_TOKEN).build()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! I'm your food tracking bot.")

bot_app.add_handler(CommandHandler("start", start))

@app.route("/", methods=["POST"])
async def webhook():
    update = Update.de_json(await request.get_json(force=True), bot_app.bot)
    # Initialize the bot app before first use if not initialized
    if not bot_app.is_running:
        await bot_app.initialize()
    await bot_app.process_update(update)
    return "ok"
