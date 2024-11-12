import discord
from discord import app_commands
from discord.ext import commands
from typing import Dict, List, Tuple
import logging
from .utils.constants import CHARACTER_DESCRIPTIONS, CHARACTER_MAPPINGS

logger = logging.getLogger('HelpCog')

CHARS_PER_PAGE = 6


class CharacterHelpCog(commands.Cog, name="Help Commands"):
    """Help commands for character listings"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.series_group = app_commands.Group(
            name="series",
            description="Show available series and characters"
        )
        self.setup_series_commands()

    def setup_series_commands(self):
        """Setup all series-related commands"""

        @self.series_group.command(name="list")
        async def series_list(interaction: discord.Interaction):
            """List all available series and their commands"""
            await self._send_series_list(interaction)

        @self.series_group.command(name="show")
        @app_commands.describe(
            series_name="The name of the series to show characters from",
            page="Page number to display (default: 1)"
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
            app_commands.Choice(name="Konosuba", value="konosuba"),
            app_commands.Choice(name="Lycoris Recoil", value="lycoris_recoil"),
            app_commands.Choice(name="Hatsune Miku", value="hatsune_miku"),
            app_commands.Choice(name="League of Legends", value="league_of_legends"),
            app_commands.Choice(name="Dota 2", value="dota2"),
            app_commands.Choice(name="Pokemon", value="pokemon")
        ])
        async def show_series(interaction: discord.Interaction, series_name: str, page: int = 1):
            """Show characters from a specific series with pagination"""
            series_display_name = series_name.replace('_', ' ').title()
            await self._send_series_help(interaction, series_name, series_display_name, page)

    async def _send_series_list(self, interaction: discord.Interaction):
        """Send the series list embed"""
        embed = discord.Embed(
            title="Available Series/Games",
            description="Use `/series show <name> [page]` to see characters from a specific series\n"
                        "For example: `/series show one_piece 1`\n\n"
                        "**Commands Format:**\n"
                        "• `/character show <series> <character>` - Get a character image\n"
                        "• `/gif show <series> <character>` - Get an animated GIF\n\n"
                        "Example: `/character show one_piece nami`",
            color=discord.Color.blue()
        )

        anime_series = [
            "One Piece", "Naruto", "Fairy Tail", "Dragon Ball",
            "Attack on Titan", "Demon Slayer", "Jujutsu Kaisen",
            "Cowboy Bebop", "Spy x Family", "One Punch Man",
            "Hunter x Hunter", "Fullmetal Alchemist",
            "My Hero Academia", "JoJo's Bizarre Adventure",
            "Konosuba", "Lycoris Recoil", "Hatsune Miku"
        ]

        games = ["League of Legends", "Dota 2", "Pokemon"]

        embed.add_field(
            name="📺 Anime Series",
            value="\n".join(f"• {name}"
                            for name in anime_series),
            inline=False
        )

        embed.add_field(
            name="🎮 Games",
            value="\n".join(f"• {name}"
                            for name in games),
            inline=False
        )

        embed.add_field(
            name="💡 Tip",
            value="Use `/series show <name> [page]` to see available characters in each series\n"
                  "Example: `/series show league_of_legends 2`",
            inline=False
        )

        await interaction.response.send_message(embed=embed)

    async def _get_paginated_chars(self, series_id: str, page: int) -> Tuple[List[Tuple[str, Tuple[str, str]]], int]:
        """Get paginated characters and total pages"""
        char_mappings = CHARACTER_MAPPINGS.get(series_id, {})
        char_descriptions = CHARACTER_DESCRIPTIONS.get(series_id, {})

        char_items = []
        for char_id, aliases in char_mappings.items():
            if char_id in char_descriptions:
                name, description = char_descriptions[char_id]
                alias_list = [a for a in aliases if a != char_id and not a.endswith('_(cosplay)')]
                if alias_list:
                    description = f"{description}\nAliases: {', '.join(alias_list)}"
                char_items.append((char_id, (name, description)))

        char_items.sort(key=lambda x: x[1][0])

        total_pages = (len(char_items) + CHARS_PER_PAGE - 1) // CHARS_PER_PAGE
        page = max(1, min(page, total_pages))

        start_idx = (page - 1) * CHARS_PER_PAGE
        end_idx = start_idx + CHARS_PER_PAGE

        return char_items[start_idx:end_idx], total_pages

    async def _send_series_help(self, interaction: discord.Interaction, series_id: str, series_name: str,
                                page: int = 1):
        """Send paginated series help embed"""
        chars = CHARACTER_MAPPINGS.get(series_id, {})
        if not chars:
            await interaction.response.send_message(f"No characters found for {series_name}")
            return

        page_chars, total_pages = await self._get_paginated_chars(series_id, page)

        embed = discord.Embed(
            title=f"{series_name} Characters (Page {page}/{total_pages})",
            description=f"List of available characters from {series_name}\n\n"
                        f"**How to use:**\n"
                        f"• `/character show {series_id} <character>` - Get an image\n"
                        f"• `/gif show {series_id} <character>` - Get a GIF\n\n"
                        f"Use `/series show {series_id} <page>` to see other pages",
            color=discord.Color.blue()
        )

        for char_id, (name, description) in page_chars:
            field_value = (
                f"_{description}_\n\n"
                f"**Example:**\n"
                f"• `/character show {series_id} {char_id}`"
            )
            embed.add_field(
                name=name,
                value=field_value,
                inline=False
            )

        embed.set_footer(text=f"Page {page} of {total_pages} | Use page numbers to navigate")

        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot) -> None:
    """Setup function to add cog to bot"""
    try:
        cog = CharacterHelpCog(bot)
        await bot.add_cog(cog)
        bot.tree.add_command(cog.series_group)
        logger.info("Successfully loaded help cog")
    except Exception as e:
        logger.error(f"Error loading help cog: {e}")
        raise