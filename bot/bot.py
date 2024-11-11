from pathlib import Path
from unittest import load_tests

import discord
from discord.ext import commands

from dotenv import load_dotenv
import os


load_dotenv(".env")

class HentaiBot(commands.Bot):
    def __init__(self):
        self._cogs = [p.stem for p in Path(".").glob("./bot/cogs/*.py")]
        super().__init__(command_prefix=self.prefix, case_insensitive=True, intents=discord.Intents.all())

    async def setup(self):
        print("Running setup...")

        for cog in self._cogs:
            await self.load_extension(f"bot.cogs.{cog}")
            print(f" Loaded `{cog}` cog.")

        print("Setup complete.")

    async def run(self):
        await self.setup()

        TOKEN = os.getenv("DISCORD_TOKEN")

        print("Running bot...")
        super().run(TOKEN, reconnect=True)

    async def shutdown(self):
        print("Closing connection to Discord...")
        await super().close()

    async def close(self):
        print("Closing on keyboard interrupt...")
        await self.shutdown()

    async def on_connect(self):
        print(f" Connected to Discord (latency: {self.latency*1000:,.0f} ms).")

    async def on_resumed(self):
        print("Bot resumed.")

    async def on_disconnect(self):
        print("Bot disconnected.")

    async def on_error(self, err, *args, **kwargs):
        raise

    async def on_command_error(self, ctx, exc):
        raise getattr(exc, "original", exc)

    async def on_ready(self):
        self.client_id = (await self.application_info()).id
        print("Bot ready.")

    async def prefix(self, bot, msg):
        return commands.when_mentioned_or(os.getenv("BOT_PREFIX"))(bot, msg)

    async def process_commands(self, msg):
        ctx = await self.get_context(msg, cls=commands.Context)

        if ctx.command is not None:
            await self.invoke(ctx)

    async def on_message(self, msg):
        if not msg.author.bot:
            await self.process_commands(msg)