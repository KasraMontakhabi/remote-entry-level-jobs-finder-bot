# bot/commands.py
import logging
from telegram import Update
from telegram.ext import CommandHandler
from .database import get_user_filters, save_user_filters, filter_new_jobs, store_job_history
from .scrapper import scrape_linkedin_jobs, get_jobs_from_jobs_api

# Setup logging
logger = logging.getLogger(__name__)


# Command: /start
async def start(update: Update, context) -> None:
    """Send a welcome message when the command /start is issued."""
    logger.info(f"User {update.message.chat_id} sent /start")
    await update.message.reply_text(
        'Welcome to the Remote Entry-Level Job Finder Bot!\nUse /set_filters to configure your job title.'
    )


# Command: /set_filters (Allow users to set job title)
async def set_filters(update: Update, context) -> None:
    """Sets the job title filters."""
    chat_id = update.message.chat_id
    filters = ' '.join(context.args)

    logger.info(f"User {chat_id} set filters: {filters}")
    save_user_filters(chat_id, filters)
    await update.message.reply_text(f'Job title filters have been set to: {filters}')


# Command: /search (Scrape job listings and send them to the user)
async def search_jobs(update: Update, context) -> None:
    """Scrapes job listings based on the job title filter."""
    chat_id = update.message.chat_id
    logger.info(f"User {chat_id} initiated a job search")

    filters = get_user_filters(chat_id)
    if not filters:
        logger.info(f"User {chat_id} has no filters set")
        await update.message.reply_text('Please set your job title using /set_filters before searching for jobs.')
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
