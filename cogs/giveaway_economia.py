import discord
from discord import app_commands
from discord.ext import commands


class GiveawayEconomia(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot


for idx in range(1, 151):
    name = f"giveaway_{idx:03d}"

    async def generated(self, interaction: discord.Interaction, _name=name):
        await interaction.response.send_message(f"💰 Giveaway & economy command `{_name}` executed.")

    generated.__name__ = name
    setattr(GiveawayEconomia, name, app_commands.command(name=name, description=f"Giveaway/economy command #{idx}")(generated))


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(GiveawayEconomia(bot))
