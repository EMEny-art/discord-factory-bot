import os
from dotenv import load_dotenv

# 1. Carica il .env automaticamente (per BotHosting/Fizzalo)
load_dotenv()

# 2. Supporta tutti i nomi comuni di token che usano gli hosting
TOKEN = (
    os.getenv("DISCORD_TOKEN") or
    os.getenv("BOT_TOKEN") or
    os.getenv("DISCORD_BOT_TOKEN") or
    os.getenv("TOKEN") or
    os.getenv("FACTORY_TOKEN")
)

if not TOKEN:
    print("ERRORE: Nessun token trovato! Controlla le Variabili d'Ambiente nel pannello.")
else:
    print("Token trovato, avvio...")
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

import discord
from discord.ext import commands

BASE_DIR = Path(__file__).resolve().parent
REGISTRY_FILE = BASE_DIR / "bots.json"
GENERATED_DIR = BASE_DIR / "generated_bots"

CATEGORY_CONFIG: dict[str, dict[str, Any]] = {
    "TICKET AVANZATI": {"slug": "ticket", "count": 200},
    "MODERAZIONE AVANZATA": {"slug": "moderation", "count": 200},
    "CONFIGURAZIONE AVANZATA": {"slug": "configuration", "count": 150},
    "GIVEAWAY ED ECONOMIA": {"slug": "giveaway", "count": 150},
    "MUSICA E FUN": {"slug": "music", "count": 200},
    "TUTTO": {"slug": "all", "count": 900},
}

CATEGORY_CHOICES = list(CATEGORY_CONFIG.keys())

CATEGORY_ALIASES = {
    "TICKET": "TICKET AVANZATI",
    "MODERAZIONE": "MODERAZIONE AVANZATA",
    "CONFIG": "CONFIGURAZIONE AVANZATA",
    "CONFIGURAZIONE": "CONFIGURAZIONE AVANZATA",
    "GIVEAWAY": "GIVEAWAY ED ECONOMIA",
    "ECONOMIA": "GIVEAWAY ED ECONOMIA",
    "MUSICA": "MUSICA E FUN",
    "FUN": "MUSICA E FUN",
    "ALL": "TUTTO",
    "TUTTI": "TUTTO",
}


class FactoryMasterBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.guilds = True
        intents.members = True
        intents.message_content = True
        super().__init__(command_prefix="!", intents=intents, help_command=None)

    async def setup_hook(self) -> None:
        await self.load_extension("cogs.master_factory")
        try:
            await self.tree.sync()
        except Exception:
            pass

    async def on_ready(self) -> None:
        print(f"Master bot online: {self.user} ({self.user.id})")
        start_generated_bots()


def normalize_category(value: str | None) -> str:
    if value is None:
        return ""
    cleaned = " ".join(str(value).strip().split()).upper()
    if not cleaned:
        return ""
    return CATEGORY_ALIASES.get(cleaned, cleaned)


def normalize_categories(*values: str | None) -> list[str]:
    selected: list[str] = []
    seen: set[str] = set()

    for value in values:
        category = normalize_category(value)
        if not category:
            continue
        if category == "TUTTO":
            for item in [
                "TICKET AVANZATI",
                "MODERAZIONE AVANZATA",
                "CONFIGURAZIONE AVANZATA",
                "GIVEAWAY ED ECONOMIA",
                "MUSICA E FUN",
            ]:
                if item not in seen:
                    selected.append(item)
                    seen.add(item)
            continue
        if category in CATEGORY_CONFIG and category not in seen:
            selected.append(category)
            seen.add(category)

    return selected


def compute_total_commands(categories: list[str]) -> int:
    return sum(CATEGORY_CONFIG.get(category, {}).get("count", 0) for category in categories)


def ensure_registry_exists() -> None:
    REGISTRY_FILE.parent.mkdir(parents=True, exist_ok=True)
    if not REGISTRY_FILE.exists():
        REGISTRY_FILE.write_text("[]\n", encoding="utf-8")


def load_registered_bots() -> list[dict[str, Any]]:
    ensure_registry_exists()
    try:
        with REGISTRY_FILE.open("r", encoding="utf-8") as fh:
            data = json.load(fh)
        if isinstance(data, list):
            return data
    except json.JSONDecodeError:
        pass
    return []


def write_registry(data: list[dict[str, Any]]) -> None:
    with REGISTRY_FILE.open("w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)
        fh.write("\n")


def build_invite_url(client_id: str, permissions: int = 8) -> str:
    client_id = str(client_id or "").strip()
    if not client_id:
        return ""
    return (
        "https://discord.com/api/oauth2/authorize"
        f"?client_id={client_id}&permissions={permissions}&scope=bot%20applications.commands"
    )


def sanitize_name(value: str) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9_-]+", "_", str(value or "factory_bot").strip())
    cleaned = cleaned.strip("_") or "factory_bot"
    return cleaned.lower()


def make_command_name(category_slug: str, index: int) -> str:
    return f"{category_slug}_{index:03d}"


def render_generated_bot_source(categories: list[str], bot_name: str, token: str, client_id: str) -> str:
    command_blocks: list[str] = []
    for category in categories:
        info = CATEGORY_CONFIG.get(category)
        if not info:
            continue
        slug = str(info["slug"])
        count = int(info["count"])
        for idx in range(1, count + 1):
            command_name = make_command_name(slug, idx)
            description = f"{category} command #{idx}"
            command_blocks.append(
                f'''
@bot.command(name="{command_name}", help="{description}")
async def {command_name}(ctx):
    await ctx.send(f"✅ {description} | bot: {{bot_name}}")
'''.strip()
            )

    block = "\n\n".join(command_blocks)
    invite_url = build_invite_url(client_id)
    return f'''import os
import discord
from discord.ext import commands

BOT_NAME = {bot_name!r}
BOT_TOKEN = {token!r}
CLIENT_ID = {client_id!r}
INVITE_URL = {invite_url!r}

intents = discord.Intents.default()
intents.guilds = True
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

@bot.event
async def on_ready():
    print(f"Generated bot online: {{bot.user}} | id={{bot.user.id}}")
    if INVITE_URL:
        print(f"Invito: {{INVITE_URL}}")

{block}

bot.run(os.getenv("DISCORD_TOKEN") or BOT_TOKEN)
'''


def create_generated_bot(categories: list[str], token: str, bot_name: str, client_id: str = "") -> dict[str, Any]:
    ensure_registry_exists()
    generated_dir = GENERATED_DIR
    generated_dir.mkdir(parents=True, exist_ok=True)

    safe_name = sanitize_name(bot_name) if bot_name else f"bot_{len(load_registered_bots()) + 1}"
    bot_dir = generated_dir / safe_name
    bot_dir.mkdir(parents=True, exist_ok=True)
    script_path = bot_dir / "bot.py"
    script_path.write_text(
        render_generated_bot_source(categories, bot_name or safe_name, token, client_id),
        encoding="utf-8",
    )

    result = {
        "name": bot_name or safe_name,
        "token": token,
        "categories": categories,
        "total_commands": compute_total_commands(categories),
        "client_id": client_id,
        "invite_url": build_invite_url(client_id),
        "script_path": str(script_path),
        "created": True,
    }

    registry = load_registered_bots()
    existing_index = next((idx for idx, item in enumerate(registry) if item.get("token") == token), None)
    if existing_index is not None:
        registry[existing_index] = result
    else:
        registry.append(result)
    write_registry(registry)
    return result


def launch_generated_bot(entry: dict[str, Any]) -> subprocess.Popen[str] | None:
    script_path = entry.get("script_path")
    if not script_path:
        return None
    path = Path(script_path)
    if not path.exists():
        return None

    env = os.environ.copy()
    env["DISCORD_TOKEN"] = str(entry.get("token", ""))
    return subprocess.Popen(
        [sys.executable, str(path)],
        cwd=str(BASE_DIR),
        env=env,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        text=True,
    )


def start_generated_bots() -> list[subprocess.Popen[str]]:
    processes: list[subprocess.Popen[str]] = []
    for entry in load_registered_bots():
        proc = launch_generated_bot(entry)
        if proc is not None:
            processes.append(proc)
    return processes


if __name__ == "__main__":
    print("Factory bot utilities loaded.")
    print("Available categories:", CATEGORY_CHOICES)
bot.run(TOKEN)
