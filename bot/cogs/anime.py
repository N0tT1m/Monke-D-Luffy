# bot/cogs/anime.py

from discord import app_commands, Interaction
from discord.ext import commands
import logging

from .utils.base_cog import BaseAnimeCog
from .utils.handlers import create_character_info
from .utils.constants import CHARACTER_DESCRIPTIONS, CHARACTER_MAPPINGS

logger = logging.getLogger('AnimeCogs')

class AnimeCog(BaseAnimeCog):
    """Combined cog for all anime/game characters"""

    def __init__(self, bot: commands.Bot):
        super().__init__(bot, "./images/")
        self.load_all_characters()
        self.character_group = app_commands.Group(
            name="character",
            description="Get character images"
        )
        self.register_slash_commands()

    def load_all_characters(self):
        """Load all character mappings with their unique descriptions"""
        for source, characters in CHARACTER_DESCRIPTIONS.items():
            for char_name, desc_data in characters.items():
                mapping_data = CHARACTER_MAPPINGS[source]
                char_info = create_character_info(char_name, source, desc_data, mapping_data)
                self.characters[char_name] = char_info

    def register_slash_commands(self):
        """Register slash commands for all characters"""
        # Series choices
        series_choices = [
            app_commands.Choice(name=name.replace('_', ' ').title(), value=name)
            for name in CHARACTER_DESCRIPTIONS.keys()
        ]

        @self.character_group.command(name="show")
        @app_commands.describe(
            series="Choose a series",
            character_name="Type the character's name"
        )
        @app_commands.choices(series=series_choices)
        async def character_command(
            interaction: Interaction,
            series: str,
            character_name: str
        ):
            """Get a character image from a specific series"""
            # Get characters for the selected series
            series_chars = {
                name: info for name, info in self.characters.items()
                if info.source.lower().replace(' ', '_') == series.lower()
            }

            # Find the closest matching character
            matched_char = None
            search_name = character_name.lower()
            for name, info in series_chars.items():
                if (name.lower() == search_name or
                    info.title.lower() == search_name or
                    search_name in name.lower() or
                    search_name in info.title.lower()):
                    matched_char = info
                    break

            if matched_char:
                await self.send_character_image(interaction, matched_char)
            else:
                # Get available characters for the error message
                available_chars = "\n".join(f"• {info.title}" for info in series_chars.values())
                await interaction.response.send_message(
                    f"Character '{character_name}' not found in {series.replace('_', ' ').title()}.\n\n"
                    f"Available characters:\n{available_chars}",
                    ephemeral=True
                )

async def setup(bot: commands.Bot) -> None:
    """Setup function to add cog to bot"""
    try:
        cog = AnimeCog(bot)
        await bot.add_cog(cog)
        bot.tree.add_command(cog.character_group)
        logger.info("Successfully loaded anime cog")
    except Exception as e:
        logger.error(f"Error loading anime cog: {e}")
        raise