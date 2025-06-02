import os
import openai
from telegram.ext import Application, CommandHandler, MessageHandler, filters

openai.api_key = os.getenv("OPENAI_API_KEY")

daily_log = []

async def start(update, context):
    await update.message.reply_text("Hi! I'm your food log bot. Send me what you ate!")

async def log_food(update, context):
    entry = update.message.text
    daily_log.append(entry)

    # Call OpenAI API for nutrition info
    response = await get_nutrition_info(entry)
    await update.message.reply_text(response)

async def get_nutrition_info(food_text):
    prompt = (
        f"You are a helpful nutrition assistant. "
        f"Given this food description, return a short summary of its estimated calories and protein:\n\n"
        f"{food_text}\n\n"
        f"Format your answer like: 'Calories: xxx kcal, Protein: xx g'"
    )
    completion = await openai.ChatCompletion.acreate(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=60,
        temperature=0.5,
    )
    return completion.choices[0].message.content

async def show_log(update, context):
    if daily_log:
        log_text = "\n".join(daily_log)
    else:
        log_text = "No food logged today."
    await update.message.reply_text(log_text)

def main():
    TOKEN = os.environ.get("BOT_TOKEN")
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("log", show_log))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, log_food))

    app.run_polling()

if __name__ == "__main__":
    main()
    