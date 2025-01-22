import discord
from discord.ext import commands
import os
import re
from datetime import datetime
from internetarchive import upload
import asyncio

DISCORD_BOT_TOKEN = "YOUR_DISCORD_BOT_TOKEN"

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Set up the bot with an activity status
activity = discord.Activity(
    name="with the Internet Archive",
    type=discord.ActivityType.playing,
)
bot.activity = activity

def generate_unique_id(base_id):
    """Generate a unique identifier using the base ID and timestamp."""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    return f"{base_id}-{timestamp}"

@bot.command(name="upload", description="Upload files to Archive.org")
async def upload_files(ctx):
    try:
        if not ctx.message.attachments:
            await ctx.send("Please attach a file to upload.")
            return

        # Save all attached files locally
        files = []
        for attachment in ctx.message.attachments:
            if attachment.size > 10 * 1024 * 1024:
                await ctx.send(f"File {attachment.filename} exceeds the 10MB limit.")
                return
            file_path = f"./{attachment.filename}"
            await attachment.save(file_path)
            files.append(file_path)

        file_count = len(files)
        await ctx.send(f"Uploading {file_count} file(s) to Archive.org...")

        # Generate the identifier
        if file_count == 1:
            # Single file: Use the file name with extension as the base identifier
            file_name_with_extension = os.path.basename(files[0])  # File name with extension
            base_item_id = re.sub(r'[^a-z0-9._-]', '_', file_name_with_extension.lower())  # Sanitize file name
        else:
            # Multiple files: Use the username as the base identifier
            base_item_id = f"discord-upload-{ctx.author.name.replace(' ', '_')}".lower()

        # Generate a unique identifier
        item_id = generate_unique_id(base_item_id)

        # Prepare the file names for the description
        file_list_str = "\n".join([os.path.basename(file) for file in files])  # List of all file names

        # Upload files
        def do_upload():
            metadata = {
                "scanner": "Discord Bot Upload",  # Adding scanner metadata
                "collection": "opensource_media",
            }
            if file_count == 1:
                metadata.update({
                    "title": os.path.basename(files[0]),  # File name as title
                    "description": f"Uploaded via Discord bot by {ctx.author.name}: {os.path.basename(files[0])}",
                })
                upload(identifier=item_id, files=files[0], metadata=metadata)
            else:
                metadata.update({
                    "title": f"Files uploaded by {ctx.author.name}",
                    "description": (
                        f"Uploaded via Discord bot by {ctx.author.name}.\n\n"
                        f"Uploaded files:\n{file_list_str}"
                    ),
                })
                upload(identifier=item_id, files=files, metadata=metadata)

        await asyncio.to_thread(do_upload)

        # Notify success
        if file_count == 1:
            await ctx.send(
                f"File successfully uploaded to Archive.org! [View it here](https://archive.org/details/{item_id})"
            )
        else:
            await ctx.send(
                f"Files successfully uploaded to Archive.org! [View them here](https://archive.org/details/{item_id})"
            )
    except Exception as e:
        await ctx.send(f"An error occurred: {str(e)}")
    finally:
        # Clean up saved files
        for file in files:
            if os.path.exists(file):
                os.remove(file)


bot.run(DISCORD_BOT_TOKEN)
