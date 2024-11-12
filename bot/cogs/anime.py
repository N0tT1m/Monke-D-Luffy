from discord import app_commands, Interaction
from discord.ext import commands
import logging
from typing import Dict, List, Optional

from .utils.base_cog import BaseAnimeCog
from .utils.handlers import create_character_info, CharacterInfo
from .utils.constants import CHARACTER_DESCRIPTIONS, CHARACTER_MAPPINGS
from .utils.logging import setup_logging

logger = setup_logging()


class AnimeCog(BaseAnimeCog):
    """Combined cog for all anime/game characters"""

    def __init__(self, bot: commands.Bot):
        super().__init__(bot, "./hentai/")
        logger.info("=== Initializing AnimeCog ===")
        self.characters = {}  # Using unique_id as key
        self.load_all_characters()
        self.character_group = app_commands.Group(
            name="character",
            description="Get character images"
        )
        self.register_slash_commands()
        logger.info("AnimeCog initialization complete")

    def load_all_characters(self):
        """Load all character mappings with their unique descriptions"""
        logger.info("Starting character loading")
        logger.debug(f"Available series in CHARACTER_DESCRIPTIONS: {list(CHARACTER_DESCRIPTIONS.keys())}")

        self.characters = {}
        total_characters = 0
        loaded_characters = 0

        for source, descriptions in CHARACTER_DESCRIPTIONS.items():
            mapping_data = CHARACTER_MAPPINGS[source]
            normalized_source = self.normalize_series_name(source)
            logger.info(f"Loading characters for {source} (normalized: {normalized_source})")

            # First collect all character IDs from both mappings and descriptions
            all_char_ids = set(descriptions.keys()) | set(mapping_data.keys())
            total_characters += len(all_char_ids)

            for char_id in all_char_ids:
                if char_id in descriptions and char_id in mapping_data:
                    char_info = create_character_info(
                        char_id=char_id,
                        source=source,
                        desc_data=descriptions[char_id],
                        mapping_data={char_id: mapping_data[char_id]}
                    )
                    if char_info:
                        # Store with normalized series name in unique ID
                        unique_id = f"{normalized_source}:{char_id.lower()}"
                        self.characters[unique_id] = char_info
                        loaded_characters += 1
                        logger.debug(f"Loaded character {unique_id} -> {char_info.title}")

        logger.info(f"Loaded {loaded_characters}/{total_characters} total characters")

    def normalize_series_name(self, series: str) -> str:
        """Normalize series name for consistent matching"""
        if not series:
            logger.warning("Attempted to normalize None or empty series name")
            return ""

        normalized = series.lower().replace(' ', '_').strip()
        logger.debug(f"Series name normalization: '{series}' -> '{normalized}'")
        return normalized

    def get_characters_for_series(self, series: str) -> List[CharacterInfo]:
        """Get all characters for a specific series"""
        if not series:
            logger.warning("Attempted to get characters for None or empty series")
            return []

        normalized_series = self.normalize_series_name(series)
        logger.info(f"Getting characters for '{series}' (normalized: '{normalized_series}')")

        series_chars = []
        for char_id, info in self.characters.items():
            series_from_id = char_id.split(':')[0]
            if series_from_id == normalized_series:
                series_chars.append(info)
                logger.debug(f"Added character '{info.title}' to series list")

        return series_chars

    def find_character(self, series: str, character_name: str) -> Optional[CharacterInfo]:
        """Find a specific character by series and name"""
        normalized_series = self.normalize_series_name(series)
        normalized_name = character_name.lower()

        # First try exact match with unique ID
        unique_id = f"{normalized_series}:{normalized_name}"
        if unique_id in self.characters:
            return self.characters[unique_id]

        # Then try matching by title
        series_chars = self.get_characters_for_series(series)
        for char in series_chars:
            if char.title.lower() == normalized_name:
                return char
            # Also check aliases
            if any(alias.lower() == normalized_name for alias in char.aliases):
                return char

        return None

    def register_slash_commands(self):
        """Register slash commands for all characters"""
        logger.info("=== Registering slash commands ===")

        # Create series choices
        series_choices = []
        for name in CHARACTER_DESCRIPTIONS.keys():
            display_name = name.replace('_', ' ').title()
            choice = app_commands.Choice(name=display_name, value=name)
            series_choices.append(choice)
            logger.debug(f"Created series choice: display='{display_name}' value='{name}'")

        @self.character_group.command(name="show")
        @app_commands.describe(
            series="Choose a series",
            character_name="Choose or type the character's name"
        )
        @app_commands.choices(series=series_choices)
        async def character_command(
                interaction: Interaction,
                series: str,
                character_name: str
        ):
            """Get a character image from a specific series"""
            try:
                logger.info(f"=== Character command called ===")
                logger.info(f"Series: '{series}'")
                logger.info(f"Character name: '{character_name}'")

                # Defer the response immediately
                await interaction.response.defer()

                # Find the character
                character = self.find_character(series, character_name)

                if character is None:
                    await interaction.followup.send(
                        f"Character '{character_name}' not found in {series}.",
                        ephemeral=True
                    )
                    return

                # Send the character image using the base cog method
                # Pass already_deferred=True since we already deferred the interaction
                await self.send_character_image(interaction, character, already_deferred=True)

            except Exception as e:
                logger.exception(f"Error in character command: {str(e)}")
                try:
                    await interaction.followup.send(
                        "An error occurred while processing your request.",
                        ephemeral=True
                    )
                except:
                    logger.error("Could not send error message - interaction may have expired")

        @character_command.autocomplete('character_name')
        async def character_autocomplete(
                interaction: Interaction,
                current: str,
        ) -> List[app_commands.Choice[str]]:
            try:
                logger.info("=== Character autocomplete called ===")
                logger.debug(f"Current input: '{current}'")

                # Get selected series from options
                selected_series = None

                # First try to get from namespace
                if interaction.namespace.series:
                    selected_series = interaction.namespace.series
                    logger.info(f"Found selected series from namespace: '{selected_series}'")

                # If not in namespace, try to get from raw options
                if not selected_series and hasattr(interaction, 'data'):
                    options = interaction.data.get('options', [])
                    logger.debug(f"Raw interaction options: {options}")

                    for option in options:
                        if isinstance(option, dict):
                            logger.debug(f"Processing option: {option}")
                            if option.get('name') == 'series':
                                selected_series = option.get('value')
                                logger.info(f"Found selected series from options: '{selected_series}'")
                                break

                if not selected_series:
                    logger.warning("No series selected in autocomplete")
                    return []

                # Get matching characters
                series_chars = self.get_characters_for_series(selected_series)
                logger.info(f"Found {len(series_chars)} characters for '{selected_series}'")

                choices = []
                for char in series_chars:
                    if not current or current.lower() in char.title.lower():
                        choice = app_commands.Choice(name=char.title, value=char.title)
                        choices.append(choice)
                        logger.debug(f"Added character choice: '{char.title}'")

                # Sort and return choices
                choices.sort(key=lambda x: x.name)
                result = choices[:25]
                logger.info(f"Returning {len(result)} character choices")
                return result

            except Exception as e:
                logger.exception(f"Error in character autocomplete: {str(e)}")
                return []


async def setup(bot: commands.Bot) -> None:
    """Setup function to add cog to bot"""
    logger.info("=== Setting up AnimeCog ===")
    try:
        cog = AnimeCog(bot)
        await bot.add_cog(cog)
        bot.tree.add_command(cog.character_group)
        logger.info("Successfully loaded anime cog")
    except Exception as e:
        logger.exception(f"Error loading anime cog: {str(e)}")
        raise