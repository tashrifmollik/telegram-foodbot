from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")


# Load environment variables
BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")

app = Flask(__name__)
bot_app = ApplicationBuilder().token(BOT_TOKEN).build()

# Define a command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! I'm your food tracking bot.")

# Add handler to the bot app
bot_app.add_handler(CommandHandler("start", start))

# Webhook endpoint
@app.route("/", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot_app.bot)
    bot_app.process_update(update)
    return "ok"

if __name__ == "__main__":
    app.run(debug=True)
