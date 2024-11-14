
from dataclasses import dataclass
from typing import List, Optional, Tuple, Dict
import random
import logging
from pathlib import Path

logger = logging.getLogger('AnimeHandlers')


@dataclass
class CharacterInfo:
    """Character information class"""
    name: str  # Character's internal name/ID
    title: str  # Display name
    description: str  # Character description
    folder: str  # Image folder path
    source: str  # Series name
    aliases: List[str]  # Alternative names/spellings


class ImageHandler:
    """Handle image file operations"""

    def __init__(self, root_dir: str):
        self.root_dir = Path(root_dir)
        if not self.root_dir.exists():
            logger.error(f"Root directory does not exist: {root_dir}")
            raise FileNotFoundError(f"Directory not found: {root_dir}")

    def get_random_image(self, subfolder: str) -> Tuple[str, Path]:
        """Get a random image from specified subfolder"""
        dir_path = self.root_dir / subfolder

        if not dir_path.exists():
            logger.error(f"Subfolder does not exist: {dir_path}")
            raise FileNotFoundError(f"Directory not found: {dir_path}")

        try:
            valid_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}
            files = [
                p for p in dir_path.iterdir()
                if (p.is_file() and
                    p.suffix.lower() in valid_extensions and
                    not p.name.startswith('.'))  # Filter out hidden files
            ]

            if not files:
                logger.error(f"No valid image files found in {dir_path}")
                raise ValueError(f"No image files found in {dir_path}")

            random_file = random.choice(files)
            logger.debug(f"Selected random file: {random_file}")
            return random_file.name, random_file

        except Exception as e:
            logger.error(f"Error accessing {dir_path}: {str(e)}", exc_info=True)
            raise

def normalize_character_id(char_id: str) -> str:
    """Normalize character ID to handle edge cases"""
    return char_id.lower().strip().replace(' ', '_')


def create_character_info(
        char_id: str,
        source: str,
        desc_data: Tuple[str, str],
        mapping_data: Dict[str, List[str]]
) -> Optional[CharacterInfo]:
    """
    Create a CharacterInfo object with all necessary data

    Args:
        char_id: The character's identifier
        source: The series name
        desc_data: Tuple of (display_name, description)
        mapping_data: Dictionary of character mappings for the series

    Returns:
        CharacterInfo object if successful, None if data is invalid
    """
    try:
        # Normalize character ID
        normalized_id = normalize_character_id(char_id)

        # Handle empty or invalid input
        if not all([char_id, source, desc_data]):
            logger.error(f"Missing required data for character {char_id} in {source}")
            return None

        # Special handling for edge cases like 'nami'
        if normalized_id == 'nami':
            logger.debug(f"Special handling for character: {char_id}")
            # Ensure we have valid desc_data
            if not desc_data:
                desc_data = ("Nami", "Navigator of the Straw Hat Pirates")  # Default description

        # Validate and unpack description data
        if not isinstance(desc_data, (tuple, list)) or len(desc_data) != 2:
            logger.error(f"Invalid desc_data format for {char_id}: {desc_data}")
            # Try to recover with available data
            if isinstance(desc_data, str):
                display_name = desc_data
                description = "Character description unavailable"
            else:
                return None
        else:
            display_name, description = desc_data

        # Get aliases with fallback
        aliases = []
        if isinstance(mapping_data, dict):
            # Try both original and normalized ID
            aliases = mapping_data.get(char_id, mapping_data.get(normalized_id, []))
        if not aliases:
            logger.warning(f"No aliases found for character {char_id} in {source}, using default")
            aliases = [char_id, normalized_id, display_name.lower()]

        # Create the folder path with normalization
        folder = f"{source}/{normalized_id}"

        # Create character info object
        char_info = CharacterInfo(
            name=normalized_id,
            title=display_name,
            description=description,
            folder=folder,
            source=source.replace('_', ' ').title(),
            aliases=list(set(aliases))  # Remove duplicates
        )

        logger.debug(f"Successfully created CharacterInfo for {char_id} in {source}")
        return char_info

    except Exception as e:
        logger.error(
            f"Failed to create CharacterInfo for {char_id} in {source}: {str(e)}",
            exc_info=True
        )
        return None


def merge_character_data(descriptions: dict, mappings: dict) -> Dict[str, Tuple[dict, dict]]:
    """
    Merge character descriptions and mappings, handling edge cases

    Args:
        descriptions: Character descriptions dictionary
        mappings: Character mappings dictionary

    Returns:
        Dictionary of merged character data
    """
    all_chars = {}

    # Normalize all keys
    norm_desc = {normalize_character_id(k): v for k, v in descriptions.items()}
    norm_map = {normalize_character_id(k): v for k, v in mappings.items()}

    # Merge data
    all_char_ids = set(norm_desc.keys()) | set(norm_map.keys())
    for char_id in all_char_ids:
        desc = norm_desc.get(char_id)
        mapping = norm_map.get(char_id)

        if desc or mapping:  # Include if either exists
            all_chars[char_id] = (desc, mapping)

    return all_chars


def merge_character_data(descriptions: dict, mappings: dict) -> Dict[str, Tuple[dict, dict]]:
    """
    Merge character descriptions and mappings, handling edge cases

    Args:
        descriptions: Character descriptions dictionary
        mappings: Character mappings dictionary

    Returns:
        Dictionary of merged character data
    """
    all_chars = {}

    # Normalize all keys
    norm_desc = {normalize_character_id(k): v for k, v in descriptions.items()}
    norm_map = {normalize_character_id(k): v for k, v in mappings.items()}

    # Merge data
    all_char_ids = set(norm_desc.keys()) | set(norm_map.keys())
    for char_id in all_char_ids:
        desc = norm_desc.get(char_id)
        mapping = norm_map.get(char_id)

        if desc or mapping:  # Include if either exists
            all_chars[char_id] = (desc, mapping)

    return all_chars
