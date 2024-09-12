# bot/scheduler.py
import schedule
import time
from telegram import Bot
from .database import filter_new_jobs, store_job_history, cursor
from .scrapper import scrape_linkedin_jobs, get_jobs_from_jobs_api


# Schedule job notifications based on user preferences
def job_notifications(token):
    bot = Bot(token=token)

    cursor.execute("SELECT chat_id, filters FROM user_filters")
    users = cursor.fetchall()

    for chat_id, filters in users:
        linkedin_jobs = scrape_linkedin_jobs(filters)
        jobs_api_jobs = get_jobs_from_jobs_api(filters)
        all_jobs = linkedin_jobs + jobs_api_jobs

        new_jobs = filter_new_jobs(chat_id, all_jobs)

        if new_jobs:
            job_message = "\n\n".join([f"{job['title']} - {job['company']}\n{job['link']}" for job in new_jobs])
            bot.send_message(chat_id=chat_id, text=job_message)
            store_job_history(chat_id, new_jobs)


# Set up scheduled job alerts (daily alerts)
def schedule_daily_alerts():
    schedule.every().day.at("09:00").do(job_notifications)
    while True:
        schedule.run_pending()
        time.sleep(1)
