# Create this file as bot/cogs/utils/handlers.py

from pathlib import Path
import random
import logging
from dataclasses import dataclass, field
from typing import List, Dict, Tuple

logger = logging.getLogger('AnimeHandlers')

@dataclass
class CharacterInfo:
    """Store character information"""
    name: str
    title: str
    description: str
    folder: str
    aliases: List[str] = field(default_factory=list)
    source: str = ""

class ImageHandler:
    """Handle image file operations"""

    def __init__(self, root_dir: str):
        self.root_dir = Path(root_dir)

    def get_random_image(self, subfolder: str) -> tuple[str, Path]:
        """Get a random image from specified subfolder"""
        dir_path = self.root_dir / subfolder

        try:
            files = [p for p in dir_path.iterdir() if p.is_file()]
            if not files:
                raise ValueError(f"No files found in {dir_path}")

            random_file = random.choice(files)
            return random_file.name, random_file

        except Exception as e:
            logger.error(f"Error accessing {dir_path}: {e}")
            raise

def create_character_info(name: str, source: str, desc_data: tuple, mapping_data: dict) -> CharacterInfo:
    """Helper function to create CharacterInfo objects from mapping data"""
    title, description = desc_data
    aliases = mapping_data.get(name, [])

    return CharacterInfo(
        name=name,
        title=title,
        description=description,
        folder=f"{source}/{name}",
        aliases=aliases,
        source=source.replace('_', ' ').title()
    )