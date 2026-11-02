import asyncio
import os
from pathlib import Path

from dotenv import load_dotenv

from bot_factory import FactoryMasterBot

BASE_DIR = Path(__file__).resolve().parent


def load_runtime_env() -> None:
    """Load variables from a local .env file when the host does not inject them."""
    load_dotenv(dotenv_path=BASE_DIR / ".env", override=False)
    load_dotenv(override=False)


def resolve_token() -> str:
    """Support common naming conventions used by different Python hosts."""
    return (
        os.getenv("DISCORD_TOKEN")
        or os.getenv("BOT_TOKEN")
        or os.getenv("TOKEN")
        or ""
    ).strip()


async def main() -> None:
    load_runtime_env()
    token = resolve_token()
    if not token:
        raise RuntimeError(
            "DISCORD_TOKEN non impostato. Imposta la variabile nel pannello del host oppure crea un .env con "
            "DISCORD_TOKEN=... (funziona anche su Bothosting, Fizzalo, VPS, Render, Railway e simili)."
        )

    bot = FactoryMasterBot()
    await bot.start(token)


if __name__ == "__main__":
    asyncio.run(main())
