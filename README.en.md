# SIU Guaraní Tracker - UNLP

A Python automation script developed to monitor course availability in the SIU Guaraní system of the National University of La Plata (UNLP).

Originally created to track openings in the highly competitive Anatomy course (Chairs B and C), it sends real-time notifications via a Telegram bot as soon as the number of enrollees is less than the class capacity.

## Features

* **Persistent Session:** Logs in only once and keeps session cookies alive, avoiding overhead on the university's server.
* **Dynamic HTML Extraction:** Bypasses Toba/Guaraní limitations, which encapsulate response HTML within JavaScript functions, using Regular Expressions to extract and parse data.
* **Real-time Notifications:** Simple integration with the Telegram API for immediate delivery of the registration link when an opening is found.

## Prerequisites

* Python 3.x installed.
* A configured Telegram bot (obtain the Token via BotFather and your Chat ID).
* Active credentials in the SIU Guaraní UNLP system.

## Installation

1. Clone this repository to your local machine:
```bash
git clone https://github.com/arturvas/unlp_materias_watcher.git
cd unlp_materias_watcher
```

2. Set up the virtual environment:
```bash
python3 -m venv venv
```

3. Depending on your OS, run:
```bash
# macOS/Linux
source venv/bin/activate

# Windows
venv\Scripts\activate.bat

# PowerShell
venv\Scripts\Activate.ps1
```

4. Install requirements:
```bash
pip install -r requirements.txt
```

## Configuration

In the project root, make a copy of the environment variables example file:
```bash
cp .env.example .env
```

Open the newly created `.env` file and fill in your information:
```bash
TELEGRAM_BOT_TOKEN: The token provided by BotFather.
TELEGRAM_CHAT_ID: Your chat ID with the bot.
GUARANI_USER: Your access username.
GUARANI_PASS: Your password for the Guaraní UNLP site.
```

## Usage

```bash
python3 tracker.py
```

The terminal will show a countdown and the current status of the classes being monitored. To stop the script, press `Ctrl + C` in the terminal.
