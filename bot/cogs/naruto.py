from ast import alias
from email.mime import image
from genericpath import isfile
import pathlib
from pydoc import describe
from discord.ext import commands
import discord
import typing as t
import random
import os

ROOT_DIR = "./hentai/naruto/"

class HentaiNaruto(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        if isinstance(ctx.channel, discord.DMChannel):
            await ctx.send("Hentai commands are not available in DMs.")
            return False
        
        return True

    @commands.command(name="anko")
    async def anko(self, ctx):
        dir_path = pathlib.Path(ROOT_DIR + "anko/")

        files = []

        # Iterate directory
        for path in os.listdir(dir_path):
            # check if current path is a file
            if os.path.isfile(os.path.join(dir_path, path)):
                files.append(path)

        random_index = random.randint(0, len(files) -1)

        random_file = files[random_index]

        dir_path = "anko/" + random_file

        embed = discord.Embed(title="Anko", description="Chunin Exams Proctor")
        file = discord.File(ROOT_DIR + dir_path, filename=random_file)
        embed.set_image(url="attachment://{}".format(random_file))

        await ctx.send(file=file, embed=embed)

    @commands.command(name="hinata")
    async def hinata(self, ctx):
        dir_path = pathlib.Path(ROOT_DIR + "hinata/")

        files = []

        # Iterate directory
        for path in os.listdir(dir_path):
            # check if current path is a file
            if os.path.isfile(os.path.join(dir_path, path)):
                files.append(path)

        random_index = random.randint(0, len(files) -1)

        random_file = files[random_index]

        dir_path = "hinata/" + random_file

        embed = discord.Embed(title="Hinata", description="Wife of Naurto")
        file = discord.File(ROOT_DIR + dir_path, filename=random_file)
        embed.set_image(url="attachment://{}".format(random_file))

        await ctx.send(file=file, embed=embed)

    @commands.command(name="ino")
    async def ino(self, ctx):
        dir_path = pathlib.Path(ROOT_DIR + "ino/")

        files = []

        # Iterate directory
        for path in os.listdir(dir_path):
            # check if current path is a file
            if os.path.isfile(os.path.join(dir_path, path)):
                files.append(path)

        random_index = random.randint(0, len(files) -1)

        random_file = files[random_index]

        dir_path = "ino/" + random_file

        embed = discord.Embed(title="Ino", description="Rival to Sakura")
        file = discord.File(ROOT_DIR + dir_path, filename=random_file)
        embed.set_image(url="attachment://{}".format(random_file))

        await ctx.send(file=file, embed=embed)

    @commands.command(name="sakura")
    async def sakura(self, ctx):
        dir_path = pathlib.Path(ROOT_DIR + "sakura/")

        files = []

        # Iterate directory
        for path in os.listdir(dir_path):
            # check if current path is a file
            if os.path.isfile(os.path.join(dir_path, path)):
                files.append(path)

        random_index = random.randint(0, len(files) -1)

        random_file = files[random_index]

        dir_path = "sakura/" + random_file

        embed = discord.Embed(title="Sakura", description="A Medical Ninja")
        file = discord.File(ROOT_DIR + dir_path, filename=random_file)
        embed.set_image(url="attachment://{}".format(random_file))

        await ctx.send(file=file, embed=embed)

    @commands.command(name="shizune")
    async def shizune(self, ctx):
        dir_path = pathlib.Path(ROOT_DIR + "shizune/")

        files = []

        # Iterate directory
        for path in os.listdir(dir_path):
            # check if current path is a file
            if os.path.isfile(os.path.join(dir_path, path)):
                files.append(path)

        random_index = random.randint(0, len(files) -1)

        random_file = files[random_index]

        dir_path = "shizune/" + random_file

        embed = discord.Embed(title="Shizune", description="Niece of Tsunade")
        file = discord.File(ROOT_DIR + dir_path, filename=random_file)
        embed.set_image(url="attachment://{}".format(random_file))

        await ctx.send(file=file, embed=embed)

    @commands.command(name="termari")
    async def termari(self, ctx):
        dir_path = pathlib.Path(ROOT_DIR + "termari/")

        files = []

        # Iterate directory
        for path in os.listdir(dir_path):
            # check if current path is a file
            if os.path.isfile(os.path.join(dir_path, path)):
                files.append(path)

        random_index = random.randint(0, len(files) -1)

        random_file = files[random_index]

        dir_path = "termari/" + random_file

        embed = discord.Embed(title="Termari", description="Wife of Shikamaru")
        file = discord.File(ROOT_DIR + dir_path, filename=random_file)
        embed.set_image(url="attachment://{}".format(random_file))

        await ctx.send(file=file, embed=embed)

    @commands.command(name="tenten")
    async def ten_ten(self, ctx):
        dir_path = pathlib.Path(ROOT_DIR + "ten_ten/")

        files = []

        # Iterate directory
        for path in os.listdir(dir_path):
            # check if current path is a file
            if os.path.isfile(os.path.join(dir_path, path)):
                files.append(path)

        random_index = random.randint(0, len(files) -1)

        random_file = files[random_index]

        dir_path = "ten_ten/" + random_file

        embed = discord.Embed(title="Tenten", description="A Chunin Exams Proctor")
        file = discord.File(ROOT_DIR + dir_path, filename=random_file)
        embed.set_image(url="attachment://{}".format(random_file))

        await ctx.send(file=file, embed=embed)

    @commands.command(name="tsunade")
    async def shizune(self, ctx):
        dir_path = pathlib.Path(ROOT_DIR + "tsunade/")

        files = []

        # Iterate directory
        for path in os.listdir(dir_path):
            # check if current path is a file
            if os.path.isfile(os.path.join(dir_path, path)):
                files.append(path)

        random_index = random.randint(0, len(files) -1)

        random_file = files[random_index]

        dir_path = "tsunade/" + random_file

        embed = discord.Embed(title="Tsunade", description="Hokage")
        file = discord.File(ROOT_DIR + dir_path, filename=random_file)
        embed.set_image(url="attachment://{}".format(random_file))

        await ctx.send(file=file, embed=embed)

async def setup(bot):
    await bot.add_cog(HentaiNaruto(bot))