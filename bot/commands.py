# bot/commands.py
import logging
from telegram import Update
from telegram.ext import CommandHandler
from .database import get_user_filters, save_user_filters, filter_new_jobs, store_job_history
from .scrapper import scrape_linkedin_jobs, get_jobs_from_jobs_api

logger = logging.getLogger(__name__)


# Command: /start
async def start(update: Update, context) -> None:
    """Send a welcome message when the command /start is issued."""
    await update.message.reply_text(
        'Welcome to the Remote Entry-Level Job Finder Bot!\nUse /set_filters to configure your job title.'
    )


# Command: /set_filters (Allow users to set job title)
async def set_filters(update: Update, context) -> None:
    """Sets the job title filters."""
    chat_id = update.message.chat_id
    filters = ' '.join(context.args)

    save_user_filters(chat_id, filters)
    await update.message.reply_text(f'Job title filters have been set to: {filters}')


# Command: /search (Scrape job listings and send them to the user)
async def search_jobs(update: Update, context) -> None:
    """Scrapes job listings based on the job title filter."""
    chat_id = update.message.chat_id

    filters = get_user_filters(chat_id)
    if not filters:
        await update.message.reply_text('Please set your job title using /set_filters before searching for jobs.')
        return

    # Scrape jobs from multiple sites
    linkedin_jobs = scrape_linkedin_jobs(filters)
    jobs_api_jobs = get_jobs_from_jobs_api(filters)
    all_jobs = linkedin_jobs + jobs_api_jobs

    # Filter out jobs already sent to the user
    new_jobs = filter_new_jobs(chat_id, all_jobs)
    if new_jobs:
        job_message = "\n\n".join([f"{job['title']} - {job['company']}\n{job['link']}" for job in new_jobs])
        await update.message.reply_text(job_message)
        store_job_history(chat_id, new_jobs)
    else:
        await update.message.reply_text('No new remote entry-level jobs found based on your filters.')
