# main.py
import os
import logging
from dotenv import load_dotenv
from bot.commands import start, set_filters, search_jobs
from bot.database import create_tables
from bot.scheduler import schedule_daily_alerts
from telegram.ext import Application, CommandHandler

# Setup logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables from .env
load_dotenv()

# Get API keys from environment variables
TOKEN = os.getenv("TELEGRAM_API_KEY")


def main() -> None:
    """Run the bot."""
    logger.info("Starting bot and creating database tables")
    create_tables()

    # Create the Application instance and pass it your bot token
    application = Application.builder().token(TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("set_filters", set_filters))
    application.add_handler(CommandHandler("search", search_jobs))

    # Start polling for messages
    logger.info("Bot is now polling for messages")
    application.run_polling()

    # Schedule daily job notifications
    logger.info("Setting up daily job notifications")
    schedule_daily_alerts()


if __name__ == '__main__':
    main()
