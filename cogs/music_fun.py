import discord
from discord import app_commands
from discord.ext import commands


class MusicFun(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot


for idx in range(1, 201):
    name = f"music_{idx:03d}"

    async def generated(self, interaction: discord.Interaction, _name=name):
        await interaction.response.send_message(f"🎵 Music & fun command `{_name}` executed.")

    generated.__name__ = name
    setattr(MusicFun, name, app_commands.command(name=name, description=f"Music/fun command #{idx}")(generated))


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(MusicFun(bot))
