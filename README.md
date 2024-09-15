# Remote Entry-Level Job Finder Bot

## Overview

The **Remote Entry-Level Job Finder Bot** is a Telegram bot that helps users find remote, entry-level jobs from all around the world. With features like custom job filters, daily notifications, and an easy-to-use interface, users can effortlessly discover job opportunities across various industries.


## Features

- 🌍 **Worldwide Job Search**: Find remote, entry-level positions across industries.
- 🔍 **Custom Filters**: Type a job title (e.g., "Backend Developer") to set filters.
- 📅 **Automated Notifications**: Set a daily time for job updates, and get notified with the latest job postings.
- 🧹 **Clear Filters**: Reset your job filters with ease.
- ⏰ **Remove Notifications**: Stop receiving daily job alerts whenever you like.
- 🛠 **Interactive Menu**: Use `/menu` to access features like searching for jobs, setting notification times, clearing filters, and removing job notifications.

## How to Use

1. **Start the Bot**: Send `/start` to begin.
2. **Set Job Filters**: Type the job title you're looking for (e.g., "Frontend Developer") to set your filter.
3. **Search Jobs**: Use `/search` to find jobs based on your filters.
4. **Manage Notifications**: 
   - Use `/set_time <HH:MM>` to set your preferred daily notification time.
   - Use `/remove_timer` to stop daily job notifications.
5. **Clear Filters**: Use `/clear_filters` to reset your filters.
6. **Use the Interactive Menu**: Type `/menu` to see all options for managing your job preferences.

## Getting Started

### Prerequisites

- Python 3.9 or later
- A Telegram bot token from [BotFather](https://core.telegram.org/bots#botfather)
- (Optional) RapidAPI key for enhanced job API search

### Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/your-username/remote-entry-level-jobs-finder-bot.git
    cd remote-entry-level-jobs-finder-bot
    ```

2. Set up a virtual environment and install dependencies:

    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    ```

3. Create a `.env` file in the root directory and add your API keys:

    ```bash
    TELEGRAM_API_KEY=your-telegram-bot-api-key
    RAPIDAPI_KEY=your-rapidapi-key (optional)
    ```

4. Initialize the database:

    ```bash
    python3 main.py
    ```

5. Run the bot:

    ```bash
    python3 main.py
    ```

## Bot Commands

- `/start`: Start the bot and receive a welcome message.
- `/menu`: Access the interactive menu for job search, notifications, and filter management.
- `/search`: Search for jobs based on your filters.
- `/set_time <HH:MM>`: Set the daily notification time.
- `/clear_filters`: Clear all filters.
- `/remove_timer`: Stop receiving daily job notifications.

## Development

### Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature-name`).
3. Commit your changes (`git commit -m "Add a new feature"`).
4. Push to the branch (`git push origin feature-name`).
5. Open a pull request.

### Testing

To test the bot's features, you can modify the schedule interval to run more frequently. For example, instead of daily notifications, you can run tests every minute for development purposes.

### Logging

Logs are configured to capture INFO level and above, so you can monitor the bot's operations. Logs will help in debugging any issues with job searches or notification schedules.

---

Developed with ❤️ by **KasraMontakhabi**
