import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

FIXED_COLOR = 0x789922  # Yellowish green
WEBHOOK_NAME = "GreenTextBot"

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.event
async def on_message(message):
    if message.author == bot.user or not message.content.startswith('>'):
        return

    text = message.content[1:].strip()
    if not text:
        return

    # Delete the original message
    await message.delete()

    # Get the webhook, or create one if it doesn't exist
    webhooks = await message.channel.webhooks()
    webhook = next((w for w in webhooks if w.name == WEBHOOK_NAME), None)

    if webhook is None:
        webhook = await message.channel.create_webhook(name=WEBHOOK_NAME)

    # Build embed per character (like Rebane)
    embeds = []
    for char in text:
        if char == ' ':
            continue  # skip spaces (webhook messages with space-only embeds can bug out)

        embed = discord.Embed(
            title=char,
            color=FIXED_COLOR
        )
        embeds.append(embed)

    # Split into batches of 10 embeds (Discord max)
    for i in range(0, len(embeds), 10):
        await webhook.send(
            username=message.author.display_name,
            avatar_url=message.author.avatar.url if message.author.avatar else None,
            embeds=embeds[i:i+10]
        )

    # Done!

bot.run(os.getenv("DISCORD_BOT_TOKEN"))
