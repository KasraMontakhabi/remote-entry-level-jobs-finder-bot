# bot/commands.py
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import MessageHandler, filters
import schedule
from datetime import datetime
from .database import save_user_filters, get_user_filters, filter_new_jobs, store_job_history, clear_user_filters
from .scraper import scrape_linkedin_jobs, get_jobs_from_jobs_api
from .scheduler import adjust_schedule_time

logger = logging.getLogger(__name__)


# Handle incoming text messages and treat them as job filters
async def set_filter_from_message(update: Update, context) -> None:
    """Stores the user's message as a job filter."""
    chat_id = update.message.chat_id
    filters = update.message.text.strip()

    # Store the user's input as the job filter
    logger.info(f"User {chat_id} set filters: {filters}")
    save_user_filters(chat_id, filters)
    await update.message.reply_text(f"Job filter has been set to: {filters}. Use /search to search for jobs.")


# Command: /start
async def start(update: Update, context) -> None:
    """Send a welcome message when the command /start is issued."""
    start_text = """
    Welcome to the Remote Entry-Level Job Finder Bot!

    How to use:
    1. Type the job title you are looking for (e.g., "Backend Developer").
    2. Use /search to search for remote jobs based on your filter.

    Other commands:
    - /menu: Access an interactive menu for job searching options.
    - /set_time <HH:MM>: Set the daily notification time (24-hour format, e.g., 08:00).

    You will receive daily job notifications at the set time based on your filter.
    """
    await update.message.reply_text(start_text)


# Command: /set_time (Set the notification time)
async def set_time(update: Update, context) -> None:
    """Set the time for daily notifications."""
    chat_id = update.message.chat_id
    logger.info(f"User {chat_id} triggered /set_time with args: {context.args}")

    if len(context.args) != 1:
        await update.message.reply_text("Please use the format: /set_time <HH:MM> (e.g., /set_time 09:00).")
        return

    time_str = context.args[0]

    try:
        # Validate and parse the time
        adjust_schedule_time(time_str)  # Ensure this function is called
        await update.message.reply_text(
            f"Notification time has been set to {time_str}. You will receive daily notifications at this time.")
        logger.info(f"User {chat_id} set notification time to {time_str}")
    except ValueError as e:
        await update.message.reply_text("Invalid time format. Please use HH:MM (e.g., 09:00).")
        logger.error(f"Invalid time format by user {chat_id}: {time_str}. Error: {e}")


# Function to display an inline menu
async def show_menu(update: Update, context) -> None:
    """Show an interactive menu with options."""
    keyboard = [
        [InlineKeyboardButton("Search Jobs", callback_data='search_jobs')],
        [InlineKeyboardButton("Set Notification Time", callback_data='set_time')],
        [InlineKeyboardButton("Clear Filters", callback_data='clear_filters')],
        [InlineKeyboardButton("Remove Notification Timer", callback_data='remove_timer')]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Choose an option:', reply_markup=reply_markup)


# Handle button clicks from the inline menu
async def button_handler(update: Update, context) -> None:
    """Handle button click events from the inline menu."""
    query = update.callback_query
    await query.answer()

    if query.data == 'search_jobs':
        await query.edit_message_text(text="Searching for jobs... Type a job title and then use /search command.")
    elif query.data == 'set_time':
        await query.edit_message_text(text="To set the notification time, use the /set_time <HH:MM> command.")
    elif query.data == 'clear_filters':
        await clear_filters(update, context)  # Call the clear filters command
    elif query.data == 'remove_timer':
        await remove_timer(update, context)


    # Command: /search (Scrape job listings and send them to the user)
async def search_jobs(update: Update, context) -> None:
    """Scrapes job listings based on the job title filter."""
    chat_id = update.message.chat_id
    logger.info(f"User {chat_id} initiated a job search")

    filters = get_user_filters(chat_id)
    if not filters:
        logger.info(f"User {chat_id} has no filters set")
        await update.message.reply_text('Please type the job title you are looking for before searching for jobs.')
        return

    # Scrape jobs from multiple sites
    linkedin_jobs = scrape_linkedin_jobs(filters)
    jobs_api_jobs = get_jobs_from_jobs_api(filters)
    all_jobs = linkedin_jobs + jobs_api_jobs

    # Filter out jobs already sent to the user
    new_jobs = filter_new_jobs(chat_id, all_jobs)
    if new_jobs:
        logger.info(f"User {chat_id} found {len(new_jobs)} new jobs")
        job_message = "\n\n".join([f"{job['title']} - {job['company']}\n{job['link']}" for job in new_jobs])
        await update.message.reply_text(job_message)
        store_job_history(chat_id, new_jobs)
    else:
        logger.info(f"No new jobs found for user {chat_id}")
        await update.message.reply_text('No new remote entry-level jobs found based on your filters.')


async def clear_filters(update: Update, context) -> None:
    """Clears all job filters for the user."""
    if update.callback_query:
        chat_id = update.callback_query.message.chat_id  # Triggered by inline button
        await update.callback_query.edit_message_text(
            "All filters have been cleared. You can set new filters by typing a job title.")
    else:
        chat_id = update.message.chat_id  # Triggered by direct command
        await update.message.reply_text("All filters have been cleared. You can set new filters by typing a job title.")

    clear_user_filters(chat_id)  # Use the database method to clear filters
    logger.info(f"User {chat_id} cleared all filters.")


# Command: /remove_timer (Stop daily notifications for the user)
async def remove_timer(update: Update, context) -> None:
    """Removes the daily notification timer for the user."""
    if update.callback_query:
        chat_id = update.callback_query.message.chat_id  # Triggered by inline button
        await update.callback_query.edit_message_text(
            "Your daily job notifications have been removed. Use /set_time to set it again.")
    else:
        chat_id = update.message.chat_id  # Triggered by direct command
        await update.message.reply_text(
            "Your daily job notifications have been removed. Use /set_time to set it again.")

    schedule.clear('job_notifications')  # Clears all scheduled notifications
    logger.info(f"User {chat_id} removed the notification timer.")
