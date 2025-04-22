# Archive.org Uploading Bot

This Discord bot allows users to upload files directly to [Archive.org](https://archive.org) (using the internetarchive python library) via a simple command in a Discord server or message, It handles file attachments, generates unique identifiers for uploads, automatically creates metadata for each uploaded file

---

## Features

- Upload files to Archive.org with a `/upload` command
- Supports multiple file attachments in a single command
- Automatically generates metadata for each upload, including:
  - A unique identifier
  - Descriptions based on the uploader's username and file names
- Cleans up uploaded files after uploads

---

## how to set up the bot

- clone this repo
- extract it in a safe folder
- install the requirements.txt (`pip install -r requirements.txt`)
- To set the archive.org account you want the bot to upload to, say "ia configure", it will prompt you to put in your Archive.org email and password
- Replace the bot token in "YOUR_DISCORD_BOT_TOKEN" to your actual bot token (Using a .env is more recommended)
- simply run the bot and it should work

---

## Requirements

Make sure you have the following installed before running the bot:

- Python 3.8 and up
- Required python packages (`requirements.txt`)

---

## Usage

- `/upload <file(s)>`
