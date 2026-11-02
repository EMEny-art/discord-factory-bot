import asyncio
import os

from bot_factory import FactoryMasterBot


async def main() -> None:
    token = os.getenv("DISCORD_TOKEN")
    if not token:
        raise RuntimeError(
            "DISCORD_TOKEN non impostato. Impostalo nel tuo host (Bothosting, VPS, Render, Railway, ecc.)"
        )

    bot = FactoryMasterBot()
    await bot.start(token)


if __name__ == "__main__":
    asyncio.run(main())
