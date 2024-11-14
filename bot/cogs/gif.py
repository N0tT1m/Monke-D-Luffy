# bot/cogs/gif.py
from typing import List

import discord
from discord import app_commands, Interaction
from discord.ext import commands
import logging

from .utils.base_cog import BaseAnimeCog
from .utils.handlers import create_character_info
from .utils.constants import CHARACTER_DESCRIPTIONS, CHARACTER_MAPPINGS

logger = logging.getLogger('GifCogs')


class GifCog(BaseAnimeCog):
    """Cog for animated GIF images"""

    def __init__(self, bot: commands.Bot):
        super().__init__(bot, "./hentai/gifs/")
        self.load_gif_characters()
        self.gif_group = app_commands.Group(
            name="gif",
            description="Get character GIFs"
        )
        self.register_slash_commands()

    def load_gif_characters(self):
        """Load GIF versions of characters"""
        for source, descriptions in CHARACTER_DESCRIPTIONS.items():
            mapping_data = CHARACTER_MAPPINGS[source]
            for char_id, desc_data in descriptions.items():
                # Verify the character exists in both mappings and descriptions
                if char_id in mapping_data:
                    display_name, description = desc_data
                    # Create GIF-specific description data
                    gif_desc_data = (f"{display_name} GIF", f"Animated GIF - {description}")

                    char_info = create_character_info(
                        char_id=char_id,
                        source=source,
                        desc_data=gif_desc_data,
                        mapping_data={
                            char_id: [  # Create GIF-specific aliases
                                f"gif_{char_id}",
                                f"{char_id}-gif",
                                *[f"{alias}_gif" for alias in mapping_data[char_id]]
                            ]
                        }
                    )
                    # Override the folder to use the gifs subdirectory
                    char_info.folder = f"{source}/gifs/{char_id}"
                    self.characters[char_id] = char_info
                else:
                    logger.warning(f"Character {char_id} found in descriptions but not in mappings for {source}")

    def register_slash_commands(self):
        """Register slash commands for all GIF characters"""
        series_choices = [
            app_commands.Choice(name=name.replace('_', ' ').title(), value=name)
            for name in CHARACTER_DESCRIPTIONS.keys()
        ]

        @self.gif_group.command(name="show")
        @app_commands.describe(
            series="Choose a series",
            character_name="Choose or type the character's name"
        )
        @app_commands.choices(series=series_choices)
        async def gif_command(
                interaction: Interaction,
                series: str,
                character_name: str
        ):
            """Get a character GIF from a specific series"""
            # Rest of the command implementation remains the same...
            # [Previous implementation]

        # Fixed autocomplete implementation
        @gif_command.autocomplete('character_name')
        async def character_autocomplete(
                interaction: Interaction,
                current: str,
        ) -> List[app_commands.Choice[str]]:
            try:
                # Correctly access the options from interaction data
                options = interaction.data.get('options', [])
                selected_series = None

                # Iterate through options to find series
                for option in options:
                    if isinstance(option, dict) and option.get('name') == 'series':
                        selected_series = option.get('value')
                        break

                if not selected_series:
                    return []

                return await self.get_character_autocomplete(interaction, current, selected_series)

            except Exception as e:
                logger.error(f"Error in character autocomplete: {e}")
                return []

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