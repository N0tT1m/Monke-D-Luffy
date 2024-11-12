# bot/cogs/base_cog.py

import discord
from discord.ext import commands
import logging
from typing import Dict

from .utils.handlers import CharacterInfo, ImageHandler, CharacterManager
from .utils.constants import CHARACTER_MAPPINGS, CHARACTER_DESCRIPTIONS

logger = logging.getLogger('AnimeBaseCog')

class BaseAnimeCog(commands.Cog):
    """Base cog for anime image commands"""

    def __init__(self, bot: commands.Bot, root_dir: str):
        self.bot = bot
        self.image_handler = ImageHandler(root_dir)
        self.character_manager = CharacterManager(CHARACTER_MAPPINGS, CHARACTER_DESCRIPTIONS)

    async def send_character_image(self, interaction: discord.Interaction, character: CharacterInfo):
        """Send an embed with random character image"""
        try:
            filename, file_path = self.image_handler.get_random_image(character.folder)

            embed = discord.Embed(
                title=f"{character.title} ({character.source})",
                description=character.description,
                color=discord.Color.random()
            )

            file = discord.File(
                file_path,
                filename=filename
            )

            embed.set_image(url=f"attachment://{filename}")
            await interaction.response.send_message(file=file, embed=embed)

        except FileNotFoundError:
            await interaction.response.send_message(
                f"No images found for {character.title}",
                ephemeral=True
            )
        except Exception as e:
            logger.error(f"Error sending image for {character.name}: {e}")
            await interaction.response.send_message(
                f"Error retrieving image for {character.title}",
                ephemeral=True
            )

    def get_character_list(self, series: str) -> str:
        """Get formatted list of available characters for a series"""
        characters = self.character_manager.get_characters_by_series(series)
        if not characters:
            return "No characters found for this series."

        return "\n".join(
            f"• {char.title} - {char.description.split('.')[0]}"
            for char in sorted(characters, key=lambda x: x.title)
        )
