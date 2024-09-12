# main.py
import os
from dotenv import load_dotenv
from bot.commands import start, set_filters, search_jobs
from bot.database import create_tables
from bot.scheduler import schedule_daily_alerts
from telegram.ext import Application, CommandHandler

# Load environment variables from .env
load_dotenv()

# Get API keys from environment variables
TOKEN = os.getenv("TELEGRAM_API_KEY")


def main() -> None:
    """Run the bot."""
    create_tables()

    # Create the Application instance and pass it your bot token
    application = Application.builder().token(TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("set_filters", set_filters))
    application.add_handler(CommandHandler("search", search_jobs))

    # Start polling for messages
    application.run_polling()

    # Schedule daily job notifications
    schedule_daily_alerts()


if __name__ == '__main__':
    main()
