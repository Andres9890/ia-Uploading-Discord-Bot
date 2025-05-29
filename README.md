[License Button]: https://img.shields.io/badge/License-MIT-blue
[License Link]: https://github.com/Andres9890/ia-Uploading-Discord-Bot/blob/main/LICENSE 'MIT License.'


# Archive.org Uploading Discord Bot

[![License Button]][License Link]

This Discord bot allows users to upload files directly to [Archive.org](https://archive.org) (using the internetarchive python library) via a simple command in a Discord server or message, It handles file attachments, generates unique identifiers for uploads, automatically creates metadata for each uploaded file

---

## Features

- Upload files to Archive.org with a `/upload` command
- Supports multiple file attachments in a single command
- Automatically generates metadata for each upload, including:
  - A unique identifier
  - Descriptions based on the uploader's username and file names
- Cleans up uploaded files after uploads
- Uses environment variables for secure credential management

---

## What to install

### Installing Git

**Windows:**
1. Download the Git installer from [git-scm.com](https://git-scm.com/download/win)
2. Run the installer and follow the prompts

**macOS:**
1. Install using Homebrew:
   ```
   brew install git
   ```
   Or download the installer from [git-scm.com](https://git-scm.com/download/mac)

**Linux (Ubuntu/Debian):**
```
sudo apt update
sudo apt install git
```

### Installing Python

**Windows:**
1. Download the latest Python installer from [python.org](https://www.python.org/downloads/)
2. Run the installer, check "Add Python to PATH"

**macOS:**
1. Install using Homebrew:
   ```
   brew install python
   ```
   Or download from [python.org](https://www.python.org/downloads/)

**Linux (Ubuntu/Debian):**
```
sudo apt update
sudo apt install python3 python3-pip
```

---

## How to Set Up the Bot

1. Clone this repo:
   ```
   git clone https://github.com/Andres9890/ia-Uploading-Discord-Bot.git
   cd Archive.org-Uploading-Discord-Bot
   ```
3. Install the requirements.txt (`pip install -r requirements.txt`)
4. Configure your Archive.org account:
   - Run `ia configure` in your terminal
   - It will prompt you to enter your Archive.org email and password
5. Set up your Discord bot token:
   - Create a `.env` file in the same directory as the bot.py file
   - Add your Discord bot token to the file like this:
     ```
     DISCORD_BOT_TOKEN=your_actual_discord_token_here
     ```
   - Make sure to keep your `.env` file private and don't share it
6. Run the bot with `python bot.py`

---

## Requirements

Make sure you have the following installed before running the bot:

- Python 3.8 and up
- Required python packages (`requirements.txt`)

---

## Usage

- `/upload <file(s)>` - Upload up to 10 files to ia
- `/ping` - Test the bot's response time

---

## Security Note

- Keep your tokens and credentials secure and private
