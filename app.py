from __future__ import annotations

import os
from pathlib import Path

import discord
from discord.ext import commands

from bot_factory import load_registered_bots


class FactoryBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.guilds = True
        intents.members = True
        super().__init__(
            command_prefix="!",
            intents=intents,
            help_command=None,
        )

    async def setup_hook(self) -> None:
        for cog_name in [
            "master_factory",
            "ticket_advanced",
            "moderation_advanced",
            "configuration_advanced",
            "giveaway_economia",
            "music_fun",
        ]:
            try:
                await self.load_extension(f"cogs.{cog_name}")
            except Exception as exc:  # pragma: no cover
                print(f"Errore durante il caricamento di {cog_name}: {exc}")

        try:
            await self.tree.sync()
        except Exception:  # pragma: no cover
            pass

        registry = load_registered_bots()
        for bot_info in registry:
            print(f"Bot registrato: {bot_info['token'][:8]}... | categorie={bot_info['categories']}")


async def main() -> None:
    token = os.getenv("DISCORD_TOKEN")
    if not token:
        raise RuntimeError("DISCORD_TOKEN non impostato. Usa .env o le variabili d'ambiente di Render.")

    bot = FactoryBot()
    await bot.start(token)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
