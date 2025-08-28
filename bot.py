import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

# Enable logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# Define the formula function
def calculate_hatch_weight(current_weight, current_age):
    hatch_weight = (current_weight * 11) / (current_age + 10)
    return round(hatch_weight, 2)

# Start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Welcome to the Pet Weight Calculator Bot! 🐾\n"
        "Send /calculate to compute hatch weight or visit our web calculator: https://yourwebsite.com/calculator.html"
    )

# Calculate command handler
async def calculate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Please enter your pet's current weight (kg) and age (1-100) separated by a space.\n"
        "Example: `4.38 28`", parse_mode='Markdown'
    )

# Handle user input
async def handle_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        text = update.message.text.split()
        if len(text) != 2:
            await update.message.reply_text("Please enter two numbers: weight and age.")
            return

        current_weight = float(text[0])
        current_age = int(text[1])

        if current_age < 1 or current_age > 100:
            await update.message.reply_text("Age must be between 1 and 100.")
            return

        hatch_weight = calculate_hatch_weight(current_weight, current_age)
        await update.message.reply_text(
            f"✅ Hatch Weight: *{hatch_weight} kg*\n"
            f"Current Weight: {current_weight} kg\n"
            f"Age: {current_age}", parse_mode='Markdown'
        )
    except ValueError:
        await update.message.reply_text("Please enter valid numbers.")

def main():
    application = Application.builder().token("YOUR_BOT_TOKEN").build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("calculate", calculate))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_input))

    application.run_polling()

if __name__ == "__main__":
    main()
