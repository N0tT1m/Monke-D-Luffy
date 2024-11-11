from pathlib import Path
from typing import List, Optional
import logging
import sys
import asyncio

import discord
from discord.ext import commands
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

        intents = discord.Intents.all()
        super().__init__(
            command_prefix=self._get_prefix,
            case_insensitive=True,
            intents=intents
        )

        # Register error handlers
        self.tree.error(self._handle_app_command_error)

    def _load_cog_list(self) -> List[str]:
        """Load list of cogs from the cogs directory."""
        try:
            return [p.stem for p in self.config.cogs_dir.glob("*.py")]
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

    async def setup_hook(self) -> None:
        """Initialize bot setup."""
        logger.info("Starting bot setup...")
        try:
            await self._load_cogs()
        except Exception as e:
            logger.error(f"Setup failed: {e}")
            raise

    async def _load_cogs(self) -> None:
        """Load all cogs from the cogs directory."""
        for cog in self._cogs:
            try:
                await self.load_extension(f"bot.cogs.{cog}")
                logger.info(f"Loaded cog: {cog}")
            except Exception as e:
                logger.error(f"Failed to load cog {cog}: {e}")

    async def start(self) -> None:
        """Start the bot with error handling."""
        try:
            logger.info("Starting bot...")
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
        logger.info(f"Bot ready - Logged in as {self.user} (ID: {self.user.id})")

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
            error: discord.app_commands.AppCommandError
    ) -> None:
        """Handle application command errors."""
        logger.error(f"App command error: {error}", exc_info=error)
        await interaction.response.send_message(
            "An error occurred while processing the command.",
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


def run_bot() -> None:
    """Entry point for running the bot."""
    bot = HentaiBot()

    async def runner():
        try:
            await bot.start()
        except KeyboardInterrupt:
            await bot.close()
        except Exception as e:
            logger.critical(f"Fatal error: {e}", exc_info=e)
            await bot.close()

    asyncio.run(runner())


if __name__ == "__main__":
    run_bot()