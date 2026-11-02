import os
import discord
from discord.ext import commands

BOT_NAME = "factory-bot"
BOT_TOKEN = ""
CLIENT_ID = ""
INVITE_URL = ""

intents = discord.Intents.default()
intents.guilds = True
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

@bot.event
async def on_ready():
    print(f"Generated bot online: {bot.user} | id={bot.user.id}")
    if INVITE_URL:
        print(f"Invito: {INVITE_URL}")


@bot.tree.command(name="ticket_001", description="TICKET AVANZATI command #1")
async def ticket_001(interaction: discord.Interaction):
    await interaction.response.send_message("✅ TICKET AVANZATI command #1 | bot: factory-bot")

@bot.tree.command(name="moderation_001", description="MODERAZIONE AVANZATA command #1")
async def moderation_001(interaction: discord.Interaction):
    await interaction.response.send_message("✅ MODERAZIONE AVANZATA command #1 | bot: factory-bot")

@bot.tree.command(name="configuration_001", description="CONFIGURAZIONE AVANZATA command #1")
async def configuration_001(interaction: discord.Interaction):
    await interaction.response.send_message("✅ CONFIGURAZIONE AVANZATA command #1 | bot: factory-bot")

@bot.tree.command(name="giveaway_001", description="GIVEAWAY ED ECONOMIA command #1")
async def giveaway_001(interaction: discord.Interaction):
    await interaction.response.send_message("✅ GIVEAWAY ED ECONOMIA command #1 | bot: factory-bot")

@bot.tree.command(name="music_001", description="MUSICA E FUN command #1")
async def music_001(interaction: discord.Interaction):
    await interaction.response.send_message("✅ MUSICA E FUN command #1 | bot: factory-bot")


async def main():
    token = os.getenv("DISCORD_TOKEN") or BOT_TOKEN
    await bot.start(token)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
