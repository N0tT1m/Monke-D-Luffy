# Create this file as bot/cogs/utils/base_cog.py

import discord
from discord.ext import commands
import logging
from typing import Dict

from .handlers import CharacterInfo, ImageHandler

logger = logging.getLogger('AnimeBaseCog')

# Create this file as bot/cogs/utils/base_cog.py

import discord
from discord.ext import commands
import logging
from typing import Dict

from .handlers import CharacterInfo, ImageHandler

logger = logging.getLogger('AnimeBaseCog')

class BaseAnimeCog(commands.Cog):
    """Base cog for anime image commands"""

    def __init__(self, bot: commands.Bot, root_dir: str):
        self.bot = bot
        self.image_handler = ImageHandler(root_dir)
        self.characters: Dict[str, CharacterInfo] = {}

    async def send_character_image(self, interaction: discord.Interaction, character: CharacterInfo):
        """Send an embed with random character image"""
        try:
            filename, file_path = self.image_handler.get_random_image(character.folder)

            embed = discord.Embed(
                title=f"{character.title} ({character.source})",
                description=character.description
            )

            file = discord.File(
                file_path,
                filename=filename
            )

            embed.set_image(url=f"attachment://{filename}")
            await interaction.response.send_message(file=file, embed=embed)

        except Exception as e:
            logger.error(f"Error sending image for {character.name}: {e}")
            await interaction.response.send_message(
                f"Error retrieving image for {character.name}",
                ephemeral=True
            )

    def register_character_commands(self):
        """Register commands for all characters"""
        for char_info in self.characters.values():
            @commands.command(
                name=char_info.name.lower(),
                aliases=char_info.aliases
            )
            async def character_command(
                    self,
                    ctx: commands.Context,
                    char_info=char_info
            ):
                await self.send_character_image(ctx, char_info)

            self.__cog_commands__ = self.__cog_commands__ + (character_command,)