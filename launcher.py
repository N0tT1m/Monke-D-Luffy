from bot import HentaiBot
import nest_asyncio
import asyncio

async def main():
    bot = HentaiBot()
    await bot.run()

if __name__ == "__main__":
    nest_asyncio.apply()
    asyncio.run(main())