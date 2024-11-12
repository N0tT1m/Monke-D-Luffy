# bot/cogs/gif.py

from discord import app_commands, Interaction
from discord.ext import commands
import logging

from .utils.base_cog import BaseAnimeCog
from .utils.handlers import CharacterInfo
from .utils.constants import CHARACTER_DESCRIPTIONS

logger = logging.getLogger('GifCogs')

class GifCog(BaseAnimeCog):
    """Cog for animated GIF images"""

    def __init__(self, bot: commands.Bot):
        super().__init__(bot, "./images/gifs/")
        self.load_gif_characters()
        self.gif_group = app_commands.Group(
            name="gif",
            description="Get character GIFs"
        )
        self.register_slash_commands()

    def load_gif_characters(self):
        """Load GIF versions of characters"""
        for source, characters in CHARACTER_DESCRIPTIONS.items():
            for char_name, (title, description) in characters.items():
                gif_name = f"{char_name}_gif"
                self.characters[gif_name] = CharacterInfo(
                    name=gif_name,
                    title=f"{title} Gif",
                    description=f"Animated GIF - {description}",
                    folder=f"{source}/gifs/{char_name}",
                    aliases=[f"gif_{char_name}", f"{char_name}-gif"],
                    source=source.replace('_', ' ').title()
                )

    def register_slash_commands(self):
        """Register slash commands for all GIF characters"""
        # Series choices
        series_choices = [
            app_commands.Choice(name=name.replace('_', ' ').title(), value=name)
            for name in CHARACTER_DESCRIPTIONS.keys()
        ]

        @self.gif_group.command(name="show")
        @app_commands.describe(
            series="Choose a series",
            character_name="Type the character's name"
        )
        @app_commands.choices(series=series_choices)
        async def gif_command(
            interaction: Interaction,
            series: str,
            character_name: str
        ):
            """Get a character GIF from a specific series"""
            # Get characters for the selected series
            search_name = character_name.lower()
            series_chars = {
                name: info for name, info in self.characters.items()
                if info.source.lower().replace(' ', '_') == series.lower()
            }

            # Find the closest matching character
            matched_char = None
            for name, info in series_chars.items():
                base_name = name.replace('_gif', '').lower()
                if (base_name == search_name or
                    search_name in base_name or
                    search_name in info.title.lower()):
                    matched_char = info
                    break

            if matched_char:
                await self.send_character_image(interaction, matched_char)
            else:
                # Get available characters for the error message
                available_chars = "\n".join(
                    f"• {info.title.replace(' Gif', '')}"
                    for info in series_chars.values()
                )
                await interaction.response.send_message(
                    f"Character '{character_name}' not found in {series.replace('_', ' ').title()}.\n\n"
                    f"Available characters:\n{available_chars}",
                    ephemeral=True
                )

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