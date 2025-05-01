import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if message.content.startswith(">"):
        greentext = message.content.strip()

        # Delete the original message
        await message.delete()

        # Use ANSI escape codes to color entire message green
        ansi_wrapped = f"```ansi\n\u001b[0;32m{greentext}\u001b[0m\n```"

        await message.channel.send(ansi_wrapped)

    await bot.process_commands(message)

bot.run(os.getenv("DISCORD_BOT_TOKEN"))
