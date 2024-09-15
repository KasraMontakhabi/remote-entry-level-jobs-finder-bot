# bot/scheduler.py
import schedule
import time
import logging
from telegram import Bot
from .database import filter_new_jobs, store_job_history, cursor
from .scraper import scrape_linkedin_jobs, get_jobs_from_jobs_api

# Setup logging
logger = logging.getLogger(__name__)

notification_time = "09:00"


# Schedule job notifications based on user preferences
def job_notifications(token):
    bot = Bot(token=token)

    logger.info("Fetching user preferences for job notifications")
    cursor.execute("SELECT chat_id, filters FROM user_filters")
    users = cursor.fetchall()

    for chat_id, filters in users:
        logger.info(f"Scraping jobs for user {chat_id} with filters: {filters}")
        linkedin_jobs = scrape_linkedin_jobs(filters)
        jobs_api_jobs = get_jobs_from_jobs_api(filters)
        all_jobs = linkedin_jobs + jobs_api_jobs

        new_jobs = filter_new_jobs(chat_id, all_jobs)

        if new_jobs:
            logger.info(f"Sending {len(new_jobs)} new jobs to user {chat_id}")
            job_message = "\n\n".join([f"{job['title']} - {job['company']}\n{job['link']}" for job in new_jobs])
            bot.send_message(chat_id=chat_id, text=job_message)
            store_job_history(chat_id, new_jobs)
        else:
            logger.info(f"No new jobs found for user {chat_id}")


# Set up scheduled job alerts (daily alerts at 9 AM)
def schedule_daily_alerts():
    logger.info("Scheduling daily job alerts at 9:00 AM")
    schedule.every().day.at("09:00").do(job_notifications)
    while True:
        schedule.run_pending()
        time.sleep(1)


def adjust_schedule_time(new_time):
    global notification_time
    notification_time = new_time
    logger.info(f"Adjusting job notifications time to {notification_time}")

    # Clear any existing scheduled jobs
    schedule.clear('job_notifications')

    # Reschedule daily alerts at the new time
    try:
        schedule.every().day.at(notification_time).do(job_notifications).tag('job_notifications')
        logger.info(f"Rescheduled daily job notifications at {notification_time}")
    except Exception as e:
        logger.error(f"Failed to reschedule job notifications at {notification_time}. Error: {e}")
