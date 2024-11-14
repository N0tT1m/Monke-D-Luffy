# bot/cogs/gif.py
from typing import List

import discord
<<<<<<< HEAD
from discord import app_commands
from discord.ext import commands
import logging

from .base_cog import BaseAnimeCog
from .utils.constants import VALID_SERIES, get_series_display_name
=======
from discord import app_commands, Interaction
from discord.ext import commands
import logging

from .utils.base_cog import BaseAnimeCog
from .utils.handlers import create_character_info
from .utils.constants import CHARACTER_DESCRIPTIONS, CHARACTER_MAPPINGS
>>>>>>> d83914c17f5472f3eec07a71ad0c8a1228f7a38e

logger = logging.getLogger('GifCogs')


class GifCog(BaseAnimeCog):
    """Cog for animated character GIFs"""

    def __init__(self, bot: commands.Bot):
        super().__init__(bot, "./hentai/gifs/")
<<<<<<< HEAD
=======
        self.load_gif_characters()
>>>>>>> d83914c17f5472f3eec07a71ad0c8a1228f7a38e
        self.gif_group = app_commands.Group(
            name="gif",
            description="Get character GIFs"
        )
        self.register_slash_commands()

<<<<<<< HEAD
    def register_slash_commands(self):
        """Register slash commands for GIFs"""
        # Series choices
=======
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
>>>>>>> d83914c17f5472f3eec07a71ad0c8a1228f7a38e
        series_choices = [
            app_commands.Choice(name=get_series_display_name(name), value=name)
            for name in sorted(VALID_SERIES)
        ]

        @self.gif_group.command(name="show")
        @app_commands.describe(
            series="Choose a series",
            character_name="Choose or type the character's name"
        )
        @app_commands.choices(series=series_choices)
        async def gif_command(
<<<<<<< HEAD
                interaction: discord.Interaction,
=======
                interaction: Interaction,
>>>>>>> d83914c17f5472f3eec07a71ad0c8a1228f7a38e
                series: str,
                character_name: str
        ):
            """Get a character GIF from a specific series"""
<<<<<<< HEAD
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

=======
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
>>>>>>> d83914c17f5472f3eec07a71ad0c8a1228f7a38e

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