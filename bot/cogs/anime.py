from pathlib import Path
from typing import List, Optional, Dict
import random
import logging
from dataclasses import dataclass

import discord
from discord.ext import commands

# Configure logging
logger = logging.getLogger('AnimeCogs')


@dataclass
class CharacterInfo:
    """Store character information"""
    name: str
    title: str
    description: str
    folder: str
    aliases: List[str] = None

    def __post_init__(self):
        if self.aliases is None:
            self.aliases = []


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


class BaseAnimeCog(commands.Cog):
    """Base cog for anime image commands"""

    def __init__(self, bot: commands.Bot, root_dir: str):
        self.bot = bot
        self.image_handler = ImageHandler(root_dir)
        self.characters: Dict[str, CharacterInfo] = {}

    async def cog_check(self, ctx: commands.Context) -> bool:
        """Prevent DM usage"""
        if isinstance(ctx.channel, discord.DMChannel):
            await ctx.send("These commands are not available in DMs.")
            return False
        return True

    async def send_character_image(
            self,
            ctx: commands.Context,
            character: CharacterInfo
    ) -> None:
        """Send an embed with random character image"""
        try:
            filename, file_path = self.image_handler.get_random_image(character.folder)

            embed = discord.Embed(
                title=character.title,
                description=character.description
            )

            file = discord.File(
                file_path,
                filename=filename
            )

            embed.set_image(url=f"attachment://{filename}")
            await ctx.send(file=file, embed=embed)

        except Exception as e:
            logger.error(f"Error sending image for {character.name}: {e}")
            await ctx.send(f"Error retrieving image for {character.name}")

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

            # Add command to the cog
            self.__cog_commands__ = self.__cog_commands__ + (character_command,)


class OnePieceCog(BaseAnimeCog):
    """Cog for One Piece character images"""

    def __init__(self, bot: commands.Bot):
        super().__init__(bot, "./hentai/one_piece/")

        # Define character info
        self.characters = {
            "nami": CharacterInfo(
                name="nami",
                title="Nami",
                description="The Cat Burglar",
                folder="nami",
                aliases=["cat-burglar"]
            ),
            "robin": CharacterInfo(
                name="robin",
                title="Robin",
                description="The Archaeologist",
                folder="robin",
                aliases=["archaeologist"]
            ),
            "hancock": CharacterInfo(
                name="hancock",
                title="Boa Hancock",
                description="The Snake Princess",
                folder="hancock",
                aliases=["boa", "snake-princess"]
            ),
            # Add other One Piece characters...
            "yamato": CharacterInfo(
                name="yamato",
                title="Yamato",
                description="Kaido's Son",
                folder="yamato",
                aliases=["kaido-son"]
            )
        }

        self.register_character_commands()


class NarutoCog(BaseAnimeCog):
    """Cog for Naruto character images"""

    def __init__(self, bot: commands.Bot):
        super().__init__(bot, "./hentai/naruto/")

        self.characters = {
            "hinata": CharacterInfo(
                name="hinata",
                title="Hinata",
                description="Wife of Naruto",
                folder="hinata",
                aliases=["hyuga"]
            ),
            "sakura": CharacterInfo(
                name="sakura",
                title="Sakura",
                description="The Medical Ninja",
                folder="sakura",
                aliases=["medical-ninja"]
            ),
            "tsunade": CharacterInfo(
                name="tsunade",
                title="Tsunade",
                description="The Fifth Hokage",
                folder="tsunade",
                aliases=["fifth-hokage", "hokage"]
            ),
            # Add other Naruto characters...
        }

        self.register_character_commands()


class GifCog(BaseAnimeCog):
    """Cog for animated GIF images"""

    def __init__(self, bot: commands.Bot):
        super().__init__(bot, "./hentai/")

        self.characters = {
            "namig": CharacterInfo(
                name="namig",
                title="Nami Gif",
                description="Nami The Cat Burglar",
                folder="_nami_gif",
                aliases=["ng", "gif-nami"]
            ),
            "hancockg": CharacterInfo(
                name="hancockg",
                title="Hancock Gif",
                description="Hancock The Snake Princess",
                folder="_hancock_gif",
                aliases=["hancock-gif", "gif-hancock"]
            ),
            "robing": CharacterInfo(
                name="robing",
                title="Robin Gif",
                description="Robin The Archaeologist",
                folder="_robin_gif",
                aliases=["rog", "gif-robin"]
            ),
            # Add other GIF entries...
        }

        self.register_character_commands()


async def setup(bot: commands.Bot):
    """Setup function to add cogs to bot"""
    try:
        await bot.add_cog(OnePieceCog(bot))
        await bot.add_cog(NarutoCog(bot))
        await bot.add_cog(GifCog(bot))
        logger.info("Successfully loaded anime cogs")
    except Exception as e:
        logger.error(f"Error loading anime cogs: {e}")
        raise