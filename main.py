# main.py
import os
import logging
from dotenv import load_dotenv
from bot.commands import start, search_jobs, set_filter_from_message, show_menu, button_handler
from bot.database import create_tables
from bot.scheduler import schedule_daily_alerts
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler

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

    # Add command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("search", search_jobs))
    application.add_handler(CommandHandler("menu", show_menu))  # Menu command
    application.add_handler(CallbackQueryHandler(button_handler))  # Handle button clicks

    # Add a handler to detect plain text messages and treat them as job filters
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, set_filter_from_message))

    # Start polling for messages
    logger.info("Bot is now polling for messages")
    application.run_polling()

    # Schedule daily job notifications
    logger.info("Setting up daily job notifications")
    schedule_daily_alerts()


if __name__ == '__main__':
    main()
