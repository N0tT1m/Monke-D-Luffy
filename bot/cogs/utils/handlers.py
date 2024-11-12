# bot/cogs/utils/handlers.py

from pathlib import Path
import random
import logging
from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional

logger = logging.getLogger('AnimeHandlers')


@dataclass
class CharacterInfo:
    """Store character information"""
    name: str
    title: str
    description: str
    folder: str
    source: str
    aliases: List[str] = field(default_factory=list)


def create_character_info(name: str, source: str, title: str, description: str, folder: str = None) -> CharacterInfo:
    """Create a CharacterInfo object with proper defaults"""
    if folder is None:
        folder = f"{source}/{name}"

    # Clean up the source name for display
    clean_source = source.replace('_', ' ').title()

    return CharacterInfo(
        name=name,
        title=title,
        description=description,
        folder=folder,
        source=clean_source,
        aliases=[f"{name}-{source}", f"{source}-{name}"]
    )


class ImageHandler:
    """Handle image file operations"""

    VALID_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif'}

    def __init__(self, root_dir: str):
        self.root_dir = Path(root_dir)
        if not self.root_dir.exists():
            self.root_dir.mkdir(parents=True, exist_ok=True)

    def get_random_image(self, subfolder: str) -> Tuple[str, Path]:
        """Get random image from specified subfolder"""
        folder = self.root_dir / subfolder
        try:
            if not folder.exists():
                raise FileNotFoundError(f"Folder not found: {folder}")

            image_files = [
                f for f in folder.glob("*")
                if f.suffix.lower() in self.VALID_EXTENSIONS
            ]

            if not image_files:
                raise ValueError(f"No images found in {folder}")

            chosen_file = random.choice(image_files)
            return chosen_file.name, chosen_file

        except Exception as e:
            logger.error(f"Error getting random image from {subfolder}: {e}")
            raise


class CharacterManager:
    """Manage character data and mappings"""

    def __init__(self, mappings: Dict, descriptions: Dict):
        self.mappings = mappings
        self.descriptions = descriptions
        self._characters: Dict[str, CharacterInfo] = {}
        self._load_characters()

    def _load_characters(self):
        """Load all characters from mappings and descriptions"""
        for series, chars in self.descriptions.items():
            for char_name, (title, desc) in chars.items():
                aliases = self.mappings[series].get(char_name, [])
                char_info = CharacterInfo(
                    name=char_name,
                    title=title,
                    description=desc,
                    folder=f"{series}/{char_name}",
                    source=series.replace('_', ' ').title(),
                    aliases=aliases
                )
                self._characters[char_name] = char_info

    def get_character(self, name: str) -> Optional[CharacterInfo]:
        """Get character info by name"""
        return self._characters.get(name)

    def get_characters_by_series(self, series: str) -> List[CharacterInfo]:
        """Get all characters from a specific series"""
        return [
            char for char in self._characters.values()
            if char.source.lower() == series.replace('_', ' ').lower()
        ]

    def identify_character(self, search_term: str) -> Tuple[Optional[str], Optional[str]]:
        """Identify series and character from search term"""
        search_term = search_term.lower()

        for series, characters in self.mappings.items():
            for char_key, aliases in characters.items():
                if any(alias in search_term for alias in aliases):
                    return series, char_key

        return None, None