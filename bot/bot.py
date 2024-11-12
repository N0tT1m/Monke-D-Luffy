from pathlib import Path
from typing import List, Optional
import logging
import sys
import asyncio

import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('bot.log')
    ]
)

logger = logging.getLogger('HentaiBot')


class BotConfig:
    """Configuration management for the bot."""

    def __init__(self, env_path: str = ".env"):
        load_dotenv(env_path)
        self.token: str = self._get_required_env("DISCORD_TOKEN")
        self.prefix: str = self._get_env("BOT_PREFIX", "!")
        self.cogs_dir: Path = Path("./bot/cogs")
        self.application_id: int = int(self._get_required_env("APPLICATION_ID"))

    @staticmethod
    def _get_required_env(key: str) -> str:
        value = os.getenv(key)
        if not value:
            raise ValueError(f"Required environment variable {key} is not set")
        return value

    @staticmethod
    def _get_env(key: str, default: str) -> str:
        return os.getenv(key, default)


class HentaiBot(commands.Bot):
    """Main bot class with improved error handling and logging."""

    def __init__(self):
        self.config = BotConfig()
        self._cogs: List[str] = self._load_cog_list()

        # Set up proper intents
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        intents.guilds = True

        super().__init__(
            command_prefix=self._get_prefix,
            case_insensitive=True,
            intents=intents,
            application_id=int(self.config._get_required_env("APPLICATION_ID"))
        )

    async def setup_hook(self) -> None:
        """Initialize bot setup."""
        logger.info("Starting bot setup...")
        try:
            await self._load_cogs()
            # Sync commands
            logger.info("Syncing commands...")
            await self.tree.sync()
            logger.info("Commands synced successfully!")
        except Exception as e:
            logger.error(f"Setup failed: {e}")
            raise

    def _load_cog_list(self) -> List[str]:
        """Load list of cogs from the cogs directory."""
        try:
            return [p.stem for p in self.config.cogs_dir.glob("*.py")
                    if p.stem not in ['__init__']]
        except Exception as e:
            logger.error(f"Failed to load cog list: {e}")
            return []

    async def _get_prefix(self, bot: commands.Bot, message: discord.Message) -> List[str]:
        """Get command prefix - allows for mention or configured prefix."""
        base = [self.config.prefix]
        if message.guild:
            # Could add custom per-guild prefix logic here
            pass
        return commands.when_mentioned_or(*base)(bot, message)

    async def _load_cogs(self) -> None:
        """Load all cogs from the cogs directory."""
        for cog in self._cogs:
            try:
                if not cog.startswith('__'):  # Skip __init__.py and similar files
                    await self.load_extension(f"bot.cogs.{cog}")
                    logger.info(f"Loaded cog: {cog}")
            except Exception as e:
                logger.error(f"Failed to load cog {cog}: {e}")

    async def start(self) -> None:
        """Start the bot with error handling."""
        try:
            logger.info("Starting bot...")
            # Sync commands again on start
            await self.tree.sync()
            await super().start(self.config.token, reconnect=True)
        except Exception as e:
            logger.error(f"Failed to start bot: {e}")
            raise

    async def close(self) -> None:
        """Cleanup and close the bot connection."""
        logger.info("Shutting down bot...")
        try:
            await super().close()
        except Exception as e:
            logger.error(f"Error during shutdown: {e}")
            raise
        finally:
            logger.info("Shutdown complete")

    # Event handlers
    async def on_ready(self) -> None:
        """Handle bot ready event."""
        app_info = await self.application_info()
        self.client_id = app_info.id

        # Set the bot's status
        await self.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name="Use /series list for help"  # Updated to show slash command
            ),
            status=discord.Status.online
        )

        logger.info(f"Bot ready - Logged in as {self.user} (ID: {self.user.id})")
        logger.info("Slash commands should be available now!")

    async def on_connect(self) -> None:
        """Handle bot connect event."""
        logger.info(f"Connected to Discord (latency: {self.latency * 1000:.0f}ms)")

    async def on_disconnect(self) -> None:
        """Handle bot disconnect event."""
        logger.warning("Disconnected from Discord")

    async def on_resumed(self) -> None:
        """Handle bot resume event."""
        logger.info("Resumed Discord connection")

    # Error handling
    async def _handle_app_command_error(
            self,
            interaction: discord.Interaction,
            error: app_commands.AppCommandError
    ) -> None:
        """Handle application command errors."""
        logger.error(f"App command error: {error}", exc_info=error)

        error_message = "An error occurred while processing the command."
        if isinstance(error, app_commands.CommandOnCooldown):
            error_message = f"This command is on cooldown. Try again in {error.retry_after:.2f} seconds."
        elif isinstance(error, app_commands.MissingPermissions):
            error_message = "You don't have permission to use this command."

        try:
            await interaction.response.send_message(
                error_message,
                ephemeral=True
            )
        except discord.InteractionResponded:
            await interaction.followup.send(
                error_message,
                ephemeral=True
            )

    async def on_error(self, event_method: str, *args, **kwargs) -> None:
        """Handle general bot errors."""
        logger.error(
            f"Error in {event_method}",
            exc_info=sys.exc_info()
        )

    async def on_command_error(
            self,
            ctx: commands.Context,
            error: commands.CommandError
    ) -> None:
        """Handle command-specific errors."""
        if isinstance(error, commands.CommandNotFound):
            return

        error_msg = str(error)
        logger.error(f"Command error: {error_msg}", exc_info=error)

        await ctx.send(
            f"An error occurred: {error_msg}",
            delete_after=10
        )

        # Add these new command methods

    @commands.is_owner()
    @commands.command(name='sync')
    async def sync(self, ctx: commands.Context):
        """Sync all slash commands"""
        try:
            logger.info("Syncing commands...")
            synced = await self.tree.sync()
            logger.info(f"Synced {len(synced)} commands")
            await ctx.send(f"Synced {len(synced)} commands")
        except Exception as e:
            logger.error(f"Failed to sync commands: {e}")
            await ctx.send(f"Failed to sync commands: {e}")

    @commands.is_owner()
    @commands.command(name='sync_guild')
    async def sync_guild(self, ctx: commands.Context):
        """Sync commands to the current guild"""
        try:
            logger.info(f"Syncing commands to guild {ctx.guild.id}")
            self.tree.copy_global_to(guild=ctx.guild)
            synced = await self.tree.sync(guild=ctx.guild)
            logger.info(f"Synced {len(synced)} commands to guild")
            await ctx.send(f"Synced {len(synced)} commands to this guild")
        except Exception as e:
            logger.error(f"Failed to sync commands to guild: {e}")
            await ctx.send(f"Failed to sync commands to guild: {e}")

    @commands.is_owner()
    @commands.command(name='clear_commands')
    async def clear_commands(self, ctx: commands.Context):
        """Clear all global commands"""
        try:
            logger.info("Clearing global commands...")
            self.tree.clear_commands(guild=None)
            await self.tree.sync()
            await ctx.send("Cleared all global commands")
        except Exception as e:
            logger.error(f"Failed to clear commands: {e}")
            await ctx.send(f"Failed to clear commands: {e}")

    @commands.is_owner()
    @commands.command(name='clear_guild_commands')
    async def clear_guild_commands(self, ctx: commands.Context):
        """Clear all guild commands"""
        try:
            logger.info(f"Clearing commands from guild {ctx.guild.id}")
            self.tree.clear_commands(guild=ctx.guild)
            await self.tree.sync(guild=ctx.guild)
            await ctx.send("Cleared all guild commands")
        except Exception as e:
            logger.error(f"Failed to clear guild commands: {e}")
            await ctx.send(f"Failed to clear guild commands: {e}")