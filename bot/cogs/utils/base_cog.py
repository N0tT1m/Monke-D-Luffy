import discord
from discord.ext import commands
import logging
from typing import Dict, Optional

from .handlers import CharacterInfo, ImageHandler

logger = logging.getLogger('AnimeBaseCog')


class BaseAnimeCog(commands.Cog):
    """Base cog for anime image commands"""

    def __init__(self, bot: commands.Bot, root_dir: str):
        self.bot = bot
        self.image_handler = ImageHandler(root_dir)
        self.characters: Dict[str, CharacterInfo] = {}

    async def send_character_image(self, interaction: discord.Interaction, character: CharacterInfo,
                                   already_deferred: bool = False):
        """Send an embed with random character image"""
        try:
            # Only defer if not already deferred
            if not already_deferred:
                await interaction.response.defer()

            filename, file_path = self.image_handler.get_random_image(character.folder)

            if not filename or not file_path:
                await interaction.followup.send(
                    f"No images found for {character.title}",
                    ephemeral=True
                )
                return

            embed = discord.Embed(
                title=f"{character.title} ({character.source})",
                description=character.description
            )

            file = discord.File(
                file_path,
                filename=filename
            )

            try:
                # Try to send the image
                await interaction.followup.send(file=file, embed=embed)
            except discord.HTTPException as e:
                if e.code == 20009:  # Content filtering error
                    # Try sending without the image
                    await interaction.followup.send(
                        f"Unable to send image for {character.title} due to content restrictions.\n"
                        f"Description: {character.description}",
                        ephemeral=True
                    )
                else:
                    # For other HTTP errors, raise to be caught by outer try block
                    raise

        except discord.NotFound:
            # Interaction already timed out or was handled
            logger.error(f"Interaction not found when sending image for {character.name}")
            return

        except Exception as e:
            logger.error(f"Error sending image for {character.name}: {e}", exc_info=True)
            try:
                await interaction.followup.send(
                    f"Error retrieving image for {character.title}",
                    ephemeral=True
                )
            except discord.NotFound:
                # If we can't send the error message, just log it
                logger.error("Could not send error message - interaction expired")

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
                interaction = await ctx.interaction
                if interaction:
                    await self.send_character_image(interaction, char_info)
                else:
                    # Fallback for text commands
                    embed = discord.Embed(
                        title=f"{char_info.title} ({char_info.source})",
                        description=char_info.description
                    )
                    try:
                        filename, file_path = self.image_handler.get_random_image(char_info.folder)
                        file = discord.File(file_path, filename=filename)
                        await ctx.send(file=file, embed=embed)
                    except Exception as e:
                        await ctx.send(f"Error retrieving image for {char_info.title}")

            self.__cog_commands__ = self.__cog_commands__ + (character_command,)