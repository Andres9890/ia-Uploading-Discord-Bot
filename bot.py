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
import platform

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

def get_file_creation_date(file_path):
    """
    Get the creation date of a file and return it in YYYY-MM-DD format.
    On Unix systems, this returns the last modification time as creation time may not be available.
    """
    try:
        # Try to get creation time (works on Windows)
        if platform.system() == 'Windows':
            timestamp = os.path.getctime(file_path)
        else:
            # On Unix, use modification time as creation time might not be reliable
            stat = os.stat(file_path)
            # Try to get birth time (macOS) or fall back to modification time
            timestamp = getattr(stat, 'st_birthtime', stat.st_mtime)
        
        # Convert timestamp to datetime and format as YYYY-MM-DD
        date = datetime.fromtimestamp(timestamp)
        return date.strftime("%Y-%m-%d")
    except Exception:
        # If there's an error, return None
        return None

def get_oldest_file_date(file_paths):
    """
    Get the creation date of the oldest file from a list of file paths.
    Returns the date in YYYY-MM-DD format.
    """
    oldest_date = None
    oldest_timestamp = None
    
    for file_path in file_paths:
        try:
            if platform.system() == 'Windows':
                timestamp = os.path.getctime(file_path)
            else:
                stat = os.stat(file_path)
                timestamp = getattr(stat, 'st_birthtime', stat.st_mtime)
            
            if oldest_timestamp is None or timestamp < oldest_timestamp:
                oldest_timestamp = timestamp
                oldest_date = datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d")
        except Exception:
            continue
    
    return oldest_date

def parse_custom_metadata(metadata_string):
    """
    Parse comma-separated key=value pairs into a dictionary.
    Example: "creator=John Doe,subject=Python,collection=opensource"
    Returns: {"creator": "John Doe", "subject": "Python", "collection": "opensource"}
    """
    if not metadata_string:
        return {}
    
    metadata = {}
    # Split by comma
    pairs = metadata_string.split(',')
    
    for pair in pairs:
        pair = pair.strip()
        if '=' not in pair:
            continue
        
        # Split by first equals sign only
        key, value = pair.split('=', 1)
        key = key.strip()
        value = value.strip()
        
        if key and value:
            # Handle multiple values for the same key (create a list)
            if key in metadata:
                if isinstance(metadata[key], list):
                    metadata[key].append(value)
                else:
                    metadata[key] = [metadata[key], value]
            else:
                metadata[key] = value
    
    return metadata

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
    custom_metadata="Optional custom metadata (format: meta=data,meta=data)"
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
    file10: Optional[discord.Attachment] = None,
    custom_metadata: Optional[str] = None
):
    """
    Slash command that uploads up to 10 attachments to Archive.org
    The first file is required, the other 9 are optional
    Custom metadata can be provided in meta=data format, separated by commas
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
        base_item_id = re.sub(r'[^a-zA-Z0-9._-]', '_', attachments[0].filename)
    else:
        base_item_id = f"discord-upload-{interaction.user.name.replace(' ', '_')}"

    # First try using the base ID without a timestamp to make sure
    item_id = base_item_id
    
    # Check if the item already exists
    if await check_item_exists(item_id):
        # If it exists, then add the timestamp
        item_id = generate_unique_id(base_item_id)
        await interaction.followup.send(f"Identifier `{base_item_id}` already exists, using `{item_id}` instead.")

    # Parse custom metadata if provided
    custom_meta = {}
    if custom_metadata:
        try:
            custom_meta = parse_custom_metadata(custom_metadata)
            if custom_meta:
                await interaction.followup.send(f"Custom metadata parsed: {', '.join([f'{k}={v}' for k, v in custom_meta.items()])}")
        except Exception as e:
            await interaction.followup.send(f"Error parsing custom metadata: {e}")

    # Get file creation date(s)
    file_date = None
    if file_count == 1:
        # For single file, get its creation date
        file_date = get_file_creation_date(file_paths[0])
    else:
        # For multiple files, get the oldest file's creation date
        file_date = get_oldest_file_date(file_paths)

    # Prepare the metadata
    file_list_str = "\n".join([os.path.basename(fp) for fp in file_paths])
    metadata = {
        "scanner": "Internet Archive Discord Bot Uploader",
        "collection": "opensource_media",
    }

    # Add the date metadata if successfully retrieved
    if file_date:
        metadata["date"] = file_date

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

    # Merge custom metadata into the default metadata
    metadata.update(custom_meta)

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