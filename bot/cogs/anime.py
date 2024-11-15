import random

import discord
from discord import app_commands, Interaction
from discord.ext import commands
import logging
from typing import Dict, List, Optional
from pathlib import Path

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
        self.root_dir = Path("./hentai/")
        self.characters = {}  # Using unique_id as key
        self.load_all_characters()
        self.character_group = app_commands.Group(
            name="character",
            description="Get character images"
        )
        self.register_slash_commands()
        self.setup_random_command()
        logger.info("AnimeCog initialization complete")

    def load_all_characters(self):
        """Load all character mappings with their unique descriptions"""
        logger.info("Starting character loading")

        # Debug print the available data
        logger.debug(f"CHARACTER_MAPPINGS keys: {list(CHARACTER_MAPPINGS.keys())}")
        logger.debug(f"CHARACTER_DESCRIPTIONS keys: {list(CHARACTER_DESCRIPTIONS.keys())}")

        self.characters = {}
        total_characters = 0
        loaded_characters = 0

        # First validate data structures
        if not CHARACTER_DESCRIPTIONS or not CHARACTER_MAPPINGS:
            logger.error("CHARACTER_DESCRIPTIONS or CHARACTER_MAPPINGS is empty")
            return

        # Try loading Dota 2 specifically first
        dota_source = 'dota2'
        logger.debug(f"Looking for Dota 2 in mappings: {dota_source in CHARACTER_MAPPINGS}")
        logger.debug(f"Looking for Dota 2 in descriptions: {dota_source in CHARACTER_DESCRIPTIONS}")

        if dota_source in CHARACTER_MAPPINGS:
            dota_chars = CHARACTER_MAPPINGS[dota_source]
            logger.debug(f"Found Dota 2 characters in mappings: {list(dota_chars.keys())}")

        for source, descriptions in CHARACTER_DESCRIPTIONS.items():
            normalized_source = self.normalize_series_name(source)
            logger.info(f"Loading characters for {source} (normalized: {normalized_source})")

            # Get mapping data using both original and normalized source
            mapping_data = CHARACTER_MAPPINGS.get(normalized_source, CHARACTER_MAPPINGS.get(source, {}))

            if not mapping_data:
                logger.warning(f"No mapping data found for {source} or {normalized_source}, skipping")
                continue

            # Log specific info for Dota 2
            if normalized_source == 'dota2' or source == 'dota2':
                logger.debug(f"Processing Dota 2 - source: {source}")
                logger.debug(f"Descriptions: {list(descriptions.keys())}")
                logger.debug(f"Mapping data: {list(mapping_data.keys())}")

            # Collect all unique character IDs
            all_char_ids = set(descriptions.keys()) | set(mapping_data.keys())
            total_characters += len(all_char_ids)

            for char_id in all_char_ids:
                try:
                    # Get description data with fallback
                    desc_data = descriptions.get(char_id)
                    if not desc_data:
                        if char_id in mapping_data:
                            desc_data = (char_id.title(), f"Character from {source}")
                            logger.debug(f"Created fallback description for {char_id}")
                        else:
                            continue

                    # Get mapping data with fallback
                    char_mapping = {char_id: mapping_data.get(char_id, [char_id])}

                    char_info = create_character_info(
                        char_id=char_id,
                        source=normalized_source,
                        desc_data=desc_data,
                        mapping_data=char_mapping
                    )

                    if char_info:
                        unique_id = f"{normalized_source}:{char_id.lower()}"
                        self.characters[unique_id] = char_info
                        loaded_characters += 1
                        if normalized_source == 'dota2':
                            logger.debug(f"Successfully loaded Dota 2 character: {unique_id}")
                    else:
                        logger.warning(f"Failed to create character info for {char_id} from {source}")

                except Exception as e:
                    logger.error(f"Error loading character {char_id} from {source}: {e}")
                    continue

        logger.info(f"Loaded {loaded_characters}/{total_characters} total characters")

        # Debug print final loaded characters
        loaded_series = set(unique_id.split(':')[0] for unique_id in self.characters.keys())
        logger.debug(f"Loaded series: {loaded_series}")

        # Print specifically which Dota 2 characters were loaded
        dota_chars = [char_info for uid, char_info in self.characters.items() if uid.startswith('dota2:')]
        logger.debug(f"Loaded Dota 2 characters: {[char.title for char in dota_chars]}")

        # Debug print final loaded characters
        loaded_series = set(unique_id.split(':')[0] for unique_id in self.characters.keys())
        logger.debug(f"Loaded series: {loaded_series}")

        # Print specifically which Dota 2 characters were loaded
        dota_chars = [char_info for uid, char_info in self.characters.items() if uid.startswith('dota2:')]
        logger.debug(f"Loaded Dota 2 characters: {[char.title for char in dota_chars]}")
    def normalize_series_name(self, series: str) -> str:
        """Normalize series name for consistent matching"""
        if not series:
            logger.warning("Attempted to normalize None or empty series name")
            return ""

        # Handle special case for dota2
        if series.lower() in ['dota2', 'dota 2', 'dota_2']:
            return 'dota2'

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

    def setup_random_command(self):
        """Setup command for random character images"""

        @self.bot.tree.command(
            name="random",
            description="Get a random character image from any series"
        )
        @app_commands.describe(
            series_name="Optional: Specify a series to get random character from (leave empty for any series)"
        )
        @app_commands.choices(series_name=[
            app_commands.Choice(name="One Piece", value="one_piece"),
            app_commands.Choice(name="Naruto", value="naruto"),
            app_commands.Choice(name="Fairy Tail", value="fairy_tail"),
            app_commands.Choice(name="Dragon Ball", value="dragon_ball"),
            app_commands.Choice(name="Attack on Titan", value="attack_on_titan"),
            app_commands.Choice(name="Demon Slayer", value="demon_slayer"),
            app_commands.Choice(name="Jujutsu Kaisen", value="jujutsu_kaisen"),
            app_commands.Choice(name="Cowboy Bebop", value="cowboy_bebop"),
            app_commands.Choice(name="Spy x Family", value="spy_x_family"),
            app_commands.Choice(name="One Punch Man", value="one_punch_man"),
            app_commands.Choice(name="Hunter x Hunter", value="hunter_x_hunter"),
            app_commands.Choice(name="Fullmetal Alchemist", value="fullmetal_alchemist"),
            app_commands.Choice(name="My Hero Academia", value="my_hero_academia"),
            app_commands.Choice(name="JoJo's Bizarre Adventure", value="jojos_bizarre_adventure"),
            app_commands.Choice(name="Pokemon", value="pokemon"),
            app_commands.Choice(name="Hatsune Miku", value="hatsune_miku"),
            app_commands.Choice(name="League of Legends", value="league_of_legends"),
            app_commands.Choice(name="Dota 2", value="dota2")
        ])
        async def random_character(interaction: discord.Interaction, series_name: str = None):
            """Get a random character image"""
            try:
                await interaction.response.defer()

                if series_name:
                    # Get random character from specific series
                    chars = CHARACTER_MAPPINGS.get(series_name, {})
                    if not chars:
                        await interaction.followup.send(f"No characters found for {series_name}")
                        return

                    char_id = random.choice(list(chars.keys()))
                    name, description = CHARACTER_DESCRIPTIONS[series_name][char_id]
                    series_display_name = series_name.replace('_', ' ').title()

                else:
                    # Get random character from any series
                    all_series = list(CHARACTER_MAPPINGS.keys())
                    random_series = random.choice(all_series)
                    chars = CHARACTER_MAPPINGS[random_series]
                    char_id = random.choice(list(chars.keys()))
                    name, description = CHARACTER_DESCRIPTIONS[random_series][char_id]
                    series_display_name = random_series.replace('_', ' ').title()

                # Create character info for image handling
                char_info = CharacterInfo(
                    name=char_id,
                    title=name,
                    description=description,
                    folder=f"{random_series}/{char_id}",
                    source=series_display_name,
                    aliases=chars[char_id]
                )

                # Reuse existing image sending logic
                await self.send_character_image(interaction, char_info, already_deferred=True)

            except Exception as e:
                logger.error(f"Error in random character command: {e}", exc_info=True)
                try:
                    await interaction.followup.send(
                        "Error getting random character image",
                        ephemeral=True
                    )
                except discord.NotFound:
                    pass

    def register_slash_commands(self):
        """Register slash commands for all characters"""
        logger.info("=== Registering slash commands ===")

        # Create series choices with proper display names
        series_choices = []
        for name in CHARACTER_MAPPINGS.keys():  # Changed from CHARACTER_DESCRIPTIONS to CHARACTER_MAPPINGS
            # Handle Dota 2 specially
            if name.lower() == 'dota2':
                display_name = 'Dota 2'
                value = 'dota2'
            else:
                display_name = name.replace('_', ' ').title()
                value = name

            choice = app_commands.Choice(name=display_name, value=value)
            series_choices.append(choice)
            logger.debug(f"Created series choice: display='{display_name}' value='{value}'")

        @self.character_group.command(name="show")
        @app_commands.describe(
            series="Choose a series",
            character_name="Choose or type the character's name"
        )
        @app_commands.choices(series=sorted(series_choices, key=lambda x: x.name))  # Sort choices alphabetically
        async def character_command(
                interaction: Interaction,
                series: str,
                character_name: str
        ):
            try:
                logger.info(f"=== Character command called ===")
                logger.info(f"Series: '{series}'")
                logger.info(f"Character name: '{character_name}'")

                await interaction.response.defer()
                character = self.find_character(series, character_name)

                if character is None:
                    await interaction.followup.send(
                        f"Character '{character_name}' not found in {series}.",
                        ephemeral=True
                    )
                    return

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