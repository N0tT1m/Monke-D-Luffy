# bot/cogs/help.py

import discord
from discord import app_commands
from discord.ext import commands
from typing import Dict, List
import logging
from .utils.constants import CHARACTER_DESCRIPTIONS

logger = logging.getLogger('HelpCog')


class CharacterHelpCog(commands.Cog, name="Help Commands"):
    """Help commands for character listings"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.series_commands = self._generate_series_commands()
        self.series_group = app_commands.Group(
            name="series",
            description="Show available series and characters"
        )
        self.setup_series_commands()

    def _generate_series_commands(self) -> Dict[str, List[str]]:
        """Generate mapping of series to their character commands"""
        series_commands = {}
        for series, chars in CHARACTER_DESCRIPTIONS.items():
            char_list = []
            for char_name in chars.keys():
                char_list.append(f"/{char_name}")
                char_list.append(f"/{char_name}_gif")
            series_commands[series] = char_list
        return series_commands

    def setup_series_commands(self):
        """Setup all series-related commands"""

        # List command
        @self.series_group.command(name="list")
        async def series_list(interaction: discord.Interaction):
            """List all available series and their commands"""
            await self._send_series_list(interaction)

        # Show command
        @self.series_group.command(name="show")
        @app_commands.describe(series_name="The name of the series to show characters from")
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
        async def show_series(interaction: discord.Interaction, series_name: str):
            """Show characters from a specific series"""
            series_display_name = series_name.replace('_', ' ').title()
            await self._send_series_help(interaction, series_name, series_display_name)

    async def _send_series_list(self, interaction: discord.Interaction):
        """Send the series list embed"""
        embed = discord.Embed(
            title="Available Series/Games",
            description="Use `/series show <name>` to see characters from a specific series\n"
                        "For example: `/series show one_piece`\n\n"
                        "**Types of Commands:**\n"
                        "• `/character <name>` - Get a regular image\n"
                        "• `/gif <name>` - Get an animated GIF\n"
                        "• `/series show <name>` - List all characters in a series",
            color=discord.Color.blue()
        )

        # Define series categories
        anime_series = [
            "One Piece", "Naruto", "Fairy Tail", "Dragon Ball",
            "Attack on Titan", "Demon Slayer", "Jujutsu Kaisen",
            "Cowboy Bebop", "Spy x Family", "One Punch Man",
            "Hunter x Hunter", "Fullmetal Alchemist",
            "My Hero Academia", "JoJo's Bizarre Adventure",
            "Konosuba", "Lycoris Recoil", "Hatsune Miku"
        ]

        games = ["League of Legends", "Dota 2", "Pokemon"]

        # Add fields for each category
        embed.add_field(
            name="📺 Anime Series",
            value="\n".join(f"• `/series show {name.lower().replace(' ', '_').replace(':', '_')}`"
                            for name in anime_series),
            inline=False
        )

        embed.add_field(
            name="🎮 Games",
            value="\n".join(f"• `/series show {name.lower().replace(' ', '_')}`"
                            for name in games),
            inline=False
        )

        embed.add_field(
            name="💡 Tip",
            value="Use `/character` or `/gif` followed by the character's name!",
            inline=False
        )

        await interaction.response.send_message(embed=embed)

    async def _send_series_help(self, interaction: discord.Interaction, series_id: str, series_name: str):
        # Rest of the help sending code remains the same...
        chars = CHARACTER_DESCRIPTIONS.get(series_id, {})
        if not chars:
            await interaction.response.send_message(f"No characters found for {series_name}")
            return

        embed = discord.Embed(
            title=f"{series_name} Characters",
            description=f"List of available characters from {series_name}\n\n"
                        f"**Command Format:**\n"
                        f"• Regular image: `/character <name>`\n"
                        f"• Animated GIF: `/gif <name>`",
            color=discord.Color.blue()
        )

        # Split characters into smaller chunks
        chunk_size = 8
        char_items = list(chars.items())
        chunks = [char_items[i:i + chunk_size] for i in range(0, len(char_items), chunk_size)]

        for i, chunk in enumerate(chunks, 1):
            char_list = []
            for char_id, (name, _) in chunk:
                char_list.append(f"**{name}**")
                char_list.append(f"• `/character {char_id}`")
                char_list.append(f"• `/gif {char_id}`")
                char_list.append("")  # Add spacing between characters

            field_name = f"Characters (Part {i}/{len(chunks)})"
            field_value = "\n".join(char_list)

            if len(field_value) <= 1024:
                embed.add_field(
                    name=field_name,
                    value=field_value,
                    inline=False
                )

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