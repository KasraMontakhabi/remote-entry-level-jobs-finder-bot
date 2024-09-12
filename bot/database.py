# bot/database.py
import sqlite3

# SQLite database connection
conn = sqlite3.connect('job_finder_bot.db', check_same_thread=False)
cursor = conn.cursor()


# Create tables to store user preferences and job history
def create_tables():
    cursor.execute('''CREATE TABLE IF NOT EXISTS user_filters (
                        chat_id INTEGER PRIMARY KEY, 
                        filters TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS job_history (
                        id INTEGER PRIMARY KEY AUTOINCREMENT, 
                        chat_id INTEGER, 
                        job_title TEXT, 
                        company TEXT, 
                        job_link TEXT, 
                        UNIQUE(chat_id, job_title, company))''')
    conn.commit()


# Save user filters in the database
def save_user_filters(chat_id, filters):
    cursor.execute("INSERT OR REPLACE INTO user_filters (chat_id, filters) VALUES (?, ?)", (chat_id, filters))
    conn.commit()


# Get user filters from the database
def get_user_filters(chat_id):
    cursor.execute("SELECT filters FROM user_filters WHERE chat_id = ?", (chat_id,))
    row = cursor.fetchone()
    return row[0] if row else None


# Filter out jobs already sent to the user
def filter_new_jobs(chat_id, jobs):
    new_jobs = []
    for job in jobs:
        cursor.execute("SELECT 1 FROM job_history WHERE chat_id = ? AND job_title = ? AND company = ?",
                       (chat_id, job['title'], job['company']))
        if not cursor.fetchone():
            new_jobs.append(job)
    return new_jobs


# Store job postings in the job history table
def store_job_history(chat_id, jobs):
    for job in jobs:
        cursor.execute("INSERT OR IGNORE INTO job_history (chat_id, job_title, company, job_link) VALUES (?, ?, ?, ?)",
                       (chat_id, job['title'], job['company'], job['link']))
    conn.commit()
