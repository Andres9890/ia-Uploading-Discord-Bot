[License Button]: https://img.shields.io/badge/License-MIT-black
[License Link]: https://github.com/Andres9890/ia-Uploading-Discord-Bot/blob/main/LICENSE 'MIT License.'


# IA Uploading Discord Bot
[![License Button]][License Link]
[![Discord](https://img.shields.io/discord/1330184232894595072.svg?label=&logo=discord&logoColor=ffffff&color=7389D8&labelColor=6A7EC2)](https://discord.gg/ZrpCUxzEUk)

This is a Discord bot that allows users to upload files directly to [Archive.org](https://archive.org) (using the internetarchive python library) via a simple command in Discord, It handles file attachments, generates unique identifiers for uploads, and also creates metadata for each uploaded file

---

## Features

- Uploads files to Archive.org with a `/upload` command
- Supports 10 file attachments in a single command
- Automatically makes metadata for each upload, including:
  - A unique identifier
  - Descriptions based on the uploader's username and file names
- Cleans up uploaded files after uploads

---

## What to install

### Installing Git

**Windows:**
1. Download the Git installer from [git-scm.com](https://git-scm.com/download/win)
2. Run the installer and follow the prompts
- Note: make sure to install it in PATH

**macOS:**
1. Install using Homebrew:
   ```
   brew install git
   ```
- Or download the installer from [git-scm.com](https://git-scm.com/download/mac)

**Linux (Ubuntu/Debian):**
```
sudo apt update
sudo apt install git
```

### Installing Python

**Windows:**
1. Download the latest Python installer from [python.org](https://www.python.org/downloads/)
2. Run the installer
- Note: make sure to install it in PATH

**macOS:**
1. Install using Homebrew:
   ```
   brew install python
   ```
- Or download from [python.org](https://www.python.org/downloads/)

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
   cd ia-Uploading-Discord-Bot
   ```
3. Install the required packages (`pip install -r requirements.txt`)
4. Configure your IA account:
   - Run `ia configure` in your terminal
   - It will prompt you to enter your Archive.org email and password
5. Set up your Discord bot token:
   - Create a `.env` file in the same directory as the bot.py file
   - Add your Discord bot token to the file like this:
     ```
     DISCORD_BOT_TOKEN=discord token here
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

- `/upload <file(s)>` - Upload up to 10 files to IA
- `/ping` - Test the bot's response time
