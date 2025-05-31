import discord
from discord.ext import commands
from discord import app_commands
import os
import re
from datetime import datetime
from internetarchive import upload, get_item
import asyncio
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the Discord bot token from the .env environment variable
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")

# Make sure that the token exists
if not DISCORD_BOT_TOKEN:
    raise ValueError("Missing DISCORD_BOT_TOKEN in .env file")

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix="/", intents=intents)

# Set up the bot with an activity status (Optional)
activity = discord.Activity(
    name="github.com/Andres9890/ia-uploading-Discord-Bot",
    type=discord.ActivityType.playing,
)
bot.activity = activity

def generate_unique_id(base_id):
    """Generate a unique identifier using the base ID and timestamp."""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    return f"{base_id}-{timestamp}"

async def check_item_exists(item_id):
    """Check if an item with the given identifier already exists on Archive.org"""
    try:
        item = await asyncio.to_thread(get_item, item_id)
        # If the item exists, it will have metadata
        return item.exists
    except Exception:
        # If there's an error, the item doesn't exist
        return False

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Your bot is online.")

@bot.tree.command(name="upload", description="Upload up to 10 files to Archive.org")
@app_commands.describe(
    file1="Required file (up to 100MB)",
    file2="Optional file (up to 100MB)",
    file3="Optional file (up to 100MB)",
    file4="Optional file (up to 100MB)",
    file5="Optional file (up to 100MB)",
    file6="Optional file (up to 100MB)",
    file7="Optional file (up to 100MB)",
    file8="Optional file (up to 100MB)",
    file9="Optional file (up to 100MB)",
    file10="Optional file (up to 100MB)",
)
async def upload_files(
    interaction: discord.Interaction,
    file1: discord.Attachment,
    file2: Optional[discord.Attachment] = None,
    file3: Optional[discord.Attachment] = None,
    file4: Optional[discord.Attachment] = None,
    file5: Optional[discord.Attachment] = None,
    file6: Optional[discord.Attachment] = None,
    file7: Optional[discord.Attachment] = None,
    file8: Optional[discord.Attachment] = None,
    file9: Optional[discord.Attachment] = None,
    file10: Optional[discord.Attachment] = None
):
    """
    Slash command that uploads up to 10 attachments to Archive.org
    The first file is required, the other 9 are optional
    """

    # Defer the interaction since uploading can take time
    await interaction.response.defer()

    # Gather all provided (non-None) attachments
    all_files = [file1, file2, file3, file4, file5, file6, file7, file8, file9, file10]
    attachments = [f for f in all_files if f is not None]

    # Check if the bot actually have any attachments (should always have at least one file)
    if not attachments:
        await interaction.followup.send("No files attached. Please provide at least one file.")
        return

    # Check each attachment's size and save them locally (You can change the size)
    file_paths = []
    for attachment in attachments:
        if attachment.size > 100 * 1024 * 1024:
            await interaction.followup.send(f"File `{attachment.filename}` exceeds the 100MB limit.")
            return

        file_path = f"./{attachment.filename}"
        await attachment.save(file_path)
        file_paths.append(file_path)

    file_count = len(file_paths)
    await interaction.followup.send(f"Uploading {file_count} file(s) to Archive.org...")

    # Generate an item identifier
    #  If only one file, use the sanitized filename as the base
    #  If multiple, use a "discord-upload-{username}" style base
    if file_count == 1:
        base_item_id = re.sub(r'[^a-z0-9._-]', '_', attachments[0].filename.lower())
    else:
        base_item_id = f"discord-upload-{interaction.user.name.replace(' ', '_')}".lower()

    # First try using the base ID without a timestamp to make sure
    item_id = base_item_id
    
    # Check if the item already exists
    if await check_item_exists(item_id):
        # If it exists, then add the timestamp
        item_id = generate_unique_id(base_item_id)
        await interaction.followup.send(f"Identifier `{base_item_id}` already exists, using `{item_id}` instead.")

    # Prepare the metadata (You can change it to whatever you want)
    file_list_str = "\n".join([os.path.basename(fp) for fp in file_paths])
    metadata = {
        "scanner": "Discord Bot",
        "collection": "opensource_media",
    }

    if file_count == 1:
        # for Single files use the filename in the title/description
        metadata.update({
            "title": attachments[0].filename,
            "description": f"Uploaded via Discord bot by {interaction.user.name}: {attachments[0].filename}",
        })
    else:
        # for Multiple files, use a generic title, and include a list in description
        metadata.update({
            "title": f"Files uploaded by {interaction.user.name}",
            "description": (
                f"Uploaded via Discord bot by {interaction.user.name}.\n\n"
                f"Uploaded files:\n{file_list_str}"
            ),
        })

    # Run the upload in a separate thread to prevent Rate-limiting
    def do_upload():
        upload(identifier=item_id, files=file_paths, metadata=metadata)

    try:
        await asyncio.to_thread(do_upload)
        # Notify user with success
        if file_count == 1:
            await interaction.followup.send(
                f"File successfully uploaded to Archive.org! [View it here](https://archive.org/details/{item_id})"
            )
        else:
            await interaction.followup.send(
                f"Files successfully uploaded to Archive.org! [View them here](https://archive.org/details/{item_id})"
            )
    except Exception as e:
        await interaction.followup.send(f"An error occurred during upload: {e}")
    finally:
        # Clean up the saved files after it's done
        for path in file_paths:
            if os.path.exists(path):
                os.remove(path)

# Test the bot's response time
@bot.tree.command(name="ping", description="Test the bot's reflexes")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f"Pong! `{round(bot.latency*1000)}ms`", ephemeral=False)

bot.run(DISCORD_BOT_TOKEN)
