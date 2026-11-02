import asyncio
import os

from bot_factory import build_master_bot


async def main() -> None:
    token = os.getenv("DISCORD_TOKEN")
    if not token:
        raise RuntimeError("DISCORD_TOKEN non impostato. Impostalo nel tuo host (Bothosting, Render, ecc.)")

    bot = build_master_bot()
    await bot.start(token)


if __name__ == "__main__":
    asyncio.run(main())
