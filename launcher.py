from pathlib import Path
import asyncio
import logging
import sys
import signal
from typing import Optional

from bot import HentaiBot

# Configure logging for the launcher
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('bot.log')
    ]
)

logger = logging.getLogger('BotLauncher')


class GracefulKiller:
    """Handle graceful shutdown on SIGINT and SIGTERM."""

    def __init__(self):
        self.kill_now = False
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

    def exit_gracefully(self, signum, frame):
        logger.info(f"Received signal {signum}. Starting graceful shutdown...")
        self.kill_now = True


async def shutdown_handler(bot: HentaiBot, killer: GracefulKiller) -> None:
    """Handle graceful shutdown of the bot."""
    while not killer.kill_now:
        await asyncio.sleep(1)

    logger.info("Starting graceful shutdown process...")
    try:
        await bot.close()
        logger.info("Bot shutdown completed successfully")
    except Exception as e:
        logger.error(f"Error during shutdown: {e}", exc_info=e)
        raise


async def main():
    """Main entry point for the bot."""
    try:
        bot = HentaiBot()
        async with bot:
            await bot.start()
    except KeyboardInterrupt:
        logger.info("Received keyboard interrupt, shutting down...")
        if bot:
            await bot.close()
    except Exception as e:
        logger.error(f"Fatal error occurred: {e}", exc_info=e)
        if bot:
            await bot.close()
        raise
    finally:
        logger.info("Bot shutdown complete")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass  # Handle clean exit on Ctrl+C
    except Exception as e:
        logger.critical(f"Failed to start bot: {e}", exc_info=e)
        sys.exit(1)

def run_bot() -> None:
    """Entry point with proper error handling."""
    try:
        # Get event loop
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        # Run the bot
        loop.run_until_complete(main())

    except KeyboardInterrupt:
        logger.info("Received keyboard interrupt")
    except Exception as e:
        logger.critical(f"Fatal error in main loop: {e}", exc_info=e)
        sys.exit(1)
    finally:
        # Cleanup
        try:
            loop.close()
        except Exception as e:
            logger.error(f"Error closing event loop: {e}", exc_info=e)
        logger.info("Shutdown complete")