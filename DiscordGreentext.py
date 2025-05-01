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

        # Format as ANSI
        ansi_wrapped = f"```ansi\n\u001b[0;32m{greentext}\u001b[0m\n```"

        # Look for an existing webhook named "GreentextBot"
        webhooks = await message.channel.webhooks()
        webhook = next((w for w in webhooks if w.name == "GreentextBot"), None)

        if webhook is None:
            webhook = await message.channel.create_webhook(name="GreentextBot")

        # Send as the user via webhook
        await webhook.send(
            content=ansi_wrapped,
            username=message.author.display_name,
            avatar_url=message.author.avatar.url if message.author.avatar else None
        )

    await bot.process_commands(message)

bot.run(os.getenv("DISCORD_BOT_TOKEN"))
