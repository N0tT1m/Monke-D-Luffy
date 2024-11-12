# bot/cogs/gif.py

import discord
from discord import app_commands
from discord.ext import commands
import logging

from .base_cog import BaseAnimeCog
from .utils.constants import VALID_SERIES, get_series_display_name

logger = logging.getLogger('GifCogs')


class GifCog(BaseAnimeCog):
    """Cog for animated character GIFs"""

    def __init__(self, bot: commands.Bot):
        super().__init__(bot, "./hentai/gifs/")
        self.gif_group = app_commands.Group(
            name="gif",
            description="Get character GIFs"
        )
        self.register_slash_commands()

    def register_slash_commands(self):
        """Register slash commands for GIFs"""
        # Series choices
        series_choices = [
            app_commands.Choice(name=get_series_display_name(name), value=name)
            for name in sorted(VALID_SERIES)
        ]

        @self.gif_group.command(name="show")
        @app_commands.describe(
            series="Choose a series",
            character_name="Type the character's name"
        )
        @app_commands.choices(series=series_choices)
        async def gif_command(
                interaction: discord.Interaction,
                series: str,
                character_name: str
        ):
            """Get a character GIF from a specific series"""
            # Identify character
            series_name, char_key = self.character_manager.identify_character(character_name)

            # If character not found in specified series
            if not char_key or series_name != series:
                await interaction.response.send_message(
                    f"Character '{character_name}' not found in {get_series_display_name(series)}.\n\n"
                    f"Available characters:\n{self.get_character_list(series)}",
                    ephemeral=True
                )
                return

            # Get character info and send GIF
            char_info = self.character_manager.get_character(char_key)
            if char_info:
                # Modify folder path to point to GIFs subfolder
                char_info.folder = f"gifs/{series}/{char_key}"
                await self.send_character_image(interaction, char_info)
            else:
                await interaction.response.send_message(
                    f"Error retrieving character information.",
                    ephemeral=True
                )

        @self.gif_group.command(name="list")
        @app_commands.describe(series="Choose a series to list characters from")
        @app_commands.choices(series=series_choices)
        async def list_command(
                interaction: discord.Interaction,
                series: str
        ):
            """List all available characters with GIFs in a series"""
            embed = discord.Embed(
                title=f"Characters with GIFs from {get_series_display_name(series)}",
                description=self.get_character_list(series),
                color=discord.Color.blue()
            )
            await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot) -> None:
    """Setup function to add cog to bot"""
    try:
        cog = GifCog(bot)
        await bot.add_cog(cog)
        bot.tree.add_command(cog.gif_group)
        logger.info("Successfully loaded gif cog")
    except Exception as e:
        logger.error(f"Error loading gif cog: {e}")
        raise