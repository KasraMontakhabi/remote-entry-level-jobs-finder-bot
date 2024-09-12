# bot/scraper.py
import logging
import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


# Scrape jobs from LinkedIn (remote, entry-level, worldwide)
def scrape_linkedin_jobs(filters):
    query = filters.replace(' ', '%20')
    logger.info(f"LinkedIn query: {query}")
    url = f"https://www.linkedin.com/jobs/search/?f_E=2&f_TP=1&keywords={query}%20remote&location=Worldwide"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    jobs = []
    job_cards = soup.find_all('div', class_='job-search-card')
    for job_card in job_cards:
        title = job_card.find('h3', class_='base-search-card__title').text.strip()
        company = job_card.find('h4', class_='base-search-card__subtitle').text.strip()
        link = job_card.find('a', class_='base-card__full-link')['href']
        jobs.append({'title': title, 'company': company, 'link': link})
    return jobs[:5]


# Scrape jobs from a job API
def get_jobs_from_jobs_api(filters):
    query = filters.replace(' ', '%')
    url = f"https://jobs-api14.p.rapidapi.com/list"
    headers = {
        "x-rapidapi-key": "your-rapidapi-key-here",  # Load from environment variable
        "x-rapidapi-host": "jobs-api14.p.rapidapi.com",
        "Content-Type": "application/json"
    }
    params = {"query": query, "location": "world%20wide", "remoteOnly": True}

    response = requests.get(url, params=params, headers=headers)
    if response.status_code != 200:
        logger.error(f"Failed to retrieve jobs, status code: {response.status_code}")
        return []

    data = response.json()
    jobs = []
    for job in data.get('jobs', []):
        job_details = {
            'title': job['title'],
            'company': job['company'],
            'location': job['location'],
            'salary': job.get('salaryRange', 'Not specified'),
            'link': job['jobProviders'][0]['url'] if job['jobProviders'] else 'No URL'
        }
        jobs.append(job_details)
    return jobs
