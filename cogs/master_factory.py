import discord
from discord import app_commands
from discord.ext import commands

from bot_factory import (
    CATEGORY_CHOICES,
    CATEGORY_CONFIG,
    build_invite_url,
    compute_total_commands,
    create_generated_bot,
    load_registered_bots,
    normalize_categories,
)


class MasterFactory(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="crea-bot", description="Crea un bot Discord reale con comandi generati per categoria.")
    @app_commands.describe(
        token_bot="Token del bot Discord.",
        categoria_1="Categoria 1 (opzionale)",
        categoria_2="Categoria 2 (opzionale)",
        categoria_3="Categoria 3 (opzionale)",
        nome_bot="Nome del bot generato (opzionale)",
        client_id="Client ID dell'app Discord per creare l'invito (opzionale)",
    )
    async def crea_bot(
        self,
        interaction: discord.Interaction,
        token_bot: str,
        categoria_1: str = "",
        categoria_2: str = "",
        categoria_3: str = "",
        nome_bot: str = "",
        client_id: str = "",
    ) -> None:
        selected = normalize_categories(categoria_1, categoria_2, categoria_3)
        if not selected:
            await interaction.response.send_message(
                "❌ Nessuna categoria valida. Scegli tra: " + ", ".join(CATEGORY_CHOICES),
                ephemeral=True,
            )
            return

        total = compute_total_commands(selected)
        created = create_generated_bot(selected, token_bot, nome_bot or "factory-bot", client_id)

        lines = [
            "✅ Bot generato correttamente.",
            f"Categorie: {', '.join(selected)}",
            f"Totale comandi: {total}",
            f"Token salvato: `{token_bot[:8]}...`",
            f"File creato: `{created['script_path']}`",
        ]

        if client_id:
            lines.append(f"Invito: {created['invite_url'] or build_invite_url(client_id)}")
        else:
            lines.append(
                "⚠️ Nessun client_id inserito: non posso creare l'URL di invito fino a quando non lo aggiungi."
            )

        await interaction.response.send_message("\n".join(lines), ephemeral=False)

    @app_commands.command(name="categorie", description="Mostra tutte le categorie disponibili e i conteggi.")
    async def categorie(self, interaction: discord.Interaction) -> None:
        lines = [f"{name}: {info['count']} comandi" for name, info in CATEGORY_CONFIG.items() if name != "TUTTO"]
        lines.append(f"TUTTO: {CATEGORY_CONFIG['TUTTO']['count']} comandi")
        await interaction.response.send_message("\n".join(lines), ephemeral=True)

    @app_commands.command(name="lista-bot", description="Mostra i bot creati e presenti nel registro.")
    async def lista_bot(self, interaction: discord.Interaction) -> None:
        bots = load_registered_bots()
        if not bots:
            await interaction.response.send_message("Nessun bot registrato al momento.", ephemeral=True)
            return

        lines = []
        for bot_entry in bots:
            lines.append(
                f"- {bot_entry.get('name', 'bot')}: {bot_entry.get('total_commands', 0)} comandi | "
                f"categorie={', '.join(bot_entry.get('categories', []))}"
            )
        await interaction.response.send_message("\n".join(lines), ephemeral=True)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(MasterFactory(bot))
