import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

YELLOWISH_GREEN = 0xADFF2F  # Hex color for Yellowish Green

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith('>'):
        content = message.content[1:].strip()

        embed = discord.Embed(
            title="Colored Message",
            description=content,
            color=YELLOWISH_GREEN
        )

        await message.channel.send(embed=embed)

import os
bot.run(os.getenv("DISCORD_BOT_TOKEN"))
