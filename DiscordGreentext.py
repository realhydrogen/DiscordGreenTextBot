import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

GREEN_COLOR = 0x789922
WEBHOOK_NAME = "GreentextBot"

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if message.content.startswith(">"):
        text = message.content[1:].strip()
        if not text:
            return

        # Delete the original message
        await message.delete()

        # Get or create a webhook
        webhooks = await message.channel.webhooks()
        webhook = next((w for w in webhooks if w.name == WEBHOOK_NAME), None)

        if webhook is None:
            webhook = await message.channel.create_webhook(name=WEBHOOK_NAME)

        # Create one embed per character
        embeds = []
        for char in text:
            if char.isspace():
                continue  # Skip whitespace to prevent blank embeds
            embeds.append(
                discord.Embed(title=char, color=GREEN_COLOR)
            )

        # Send in batches of 10 (Discord limit)
        for i in range(0, len(embeds), 10):
            await webhook.send(
                username=message.author.display_name,
                avatar_url=message.author.avatar.url if message.author.avatar else None,
                embeds=embeds[i:i+10]
            )

    await bot.process_commands(message)

bot.run(os.getenv("DISCORD_BOT_TOKEN"))
