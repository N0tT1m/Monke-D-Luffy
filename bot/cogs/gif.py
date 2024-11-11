from ast import alias
from email.mime import image
from genericpath import isfile
import pathlib
from discord.ext import commands
import discord
import typing as t
import random
import os

ROOT_DIR = "./hentai/"

class HentaiGif(commands.Cog):
    def __init__(self, bot, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bot = bot

    async def cog_check(self, ctx):
        if isinstance(ctx.channel, discord.DMChannel):
            await ctx.send("Hentai commands are not available in DMs.")
            return False
        
        return True

    @commands.command(name="namig", aliases=["ng", "gif nami"])
    async def nami_gif(self, ctx):
        dir_path = pathlib.Path(ROOT_DIR + "_nami_gif/")

        files = []

        # Iterate directory
        for path in os.listdir(dir_path):
            # check if current path is a file
            if os.path.isfile(os.path.join(dir_path, path)):
                files.append(path)

        random_index = random.randint(0, len(files) -1)

        random_file = files[random_index]

        dir_path = "_nami_gif/" + random_file

        embed = discord.Embed(title="Nami Gif", description="Nami The Cat Burgalar")
        file = discord.File(ROOT_DIR + dir_path, filename=random_file)
        embed.set_image(url="attachment://{}".format(random_file))

        await ctx.send(file=file, embed=embed)

    @commands.command(name="hancockg", aliases=["hancock gif", "gif hancock"])
    async def hancock_gif(self, ctx):
        dir_path = pathlib.Path(ROOT_DIR + "_hancock_gif/")

        files = []

        # Iterate directory
        for path in os.listdir(dir_path):
            # check if current path is a file
            if os.path.isfile(os.path.join(dir_path, path)):
                files.append(path)

        random_index = random.randint(0, len(files) -1)

        random_file = files[random_index]

        dir_path = "_hancock_gif/" + random_file

        embed = discord.Embed(title="Hancock Gif", description="Hancock The Snake Princess")
        file = discord.File(ROOT_DIR + dir_path, filename=random_file)
        embed.set_image(url="attachment://{}".format(random_file))

        await ctx.send(file=file, embed=embed)

    # @commands.command(name="namikalifag", aliases=["nkg", "gif nami & kalifa", "nami and kalifa gif", "gif nami and kalifa"])
    # async def nami_and_kalifa_gif(self, ctx):
    #     dir_path = pathlib.Path(ROOT_DIR + "_nami_and_kalifa_gif/")

    #     files = []

    #     # Iterate directory
    #     for path in os.listdir(dir_path):
    #         # check if current path is a file
    #         if os.path.isfile(os.path.join(dir_path, path)):
    #             files.append(path)

    #     random_index = random.randint(0, len(files) -1)

    #     random_file = files[random_index]

    #     dir_path = "_nami_and_kalifa_gif/" + random_file

    #     embed = discord.Embed(title="Nami & Kalifa Gif", description="Nami The Cat Burgalar & Kalifa of CP9")
    #     file = discord.File(ROOT_DIR + dir_path, filename=random_file)
    #     embed.set_image(url="attachment://{}".format(random_file))

    #     await ctx.send(file=file, embed=embed)

    @commands.command(name="namirobing", aliases=["nrg", "gif nami & robin", "nami and robin gif", "gif nami and robin"])
    async def nami_and_robin_gif(self, ctx):
        dir_path = pathlib.Path(ROOT_DIR + "_nami_and_robin_gif/")

        files = []

        # Iterate directory
        for path in os.listdir(dir_path):
            # check if current path is a file
            if os.path.isfile(os.path.join(dir_path, path)):
                files.append(path)

        random_index = random.randint(0, len(files) -1)

        random_file = files[random_index]

        dir_path = "_nami_and_robin_gif/" + random_file

        embed = discord.Embed(title="Nami & Robin Gif", description="Nami The Cat Burgalar")
        file = discord.File(ROOT_DIR + dir_path, filename=random_file)
        embed.set_image(url="attachment://{}".format(random_file))

        await ctx.send(file=file, embed=embed)

    @commands.command(name="nojikog", aliases=["nog", "gif nojiko"])
    async def nojiko_gif(self, ctx):
        dir_path = pathlib.Path(ROOT_DIR + "_nojiko_gif/")

        files = []

        # Iterate directory
        for path in os.listdir(dir_path):
            # check if current path is a file
            if os.path.isfile(os.path.join(dir_path, path)):
                files.append(path)

        random_index = random.randint(0, len(files) -1)

        random_file = files[random_index]

        dir_path = "_nojiko_gif/" + random_file

        embed = discord.Embed(title="Nojiko Gif", description="Nojiko The Sister Of Nami")
        file = discord.File(ROOT_DIR + dir_path, filename=random_file)
        embed.set_image(url="attachment://{}".format(random_file))

        await ctx.send(file=file, embed=embed)

    @commands.command(name="peronag", aliases=["pg", "gif perona"])
    async def perona_gif(self, ctx):
        dir_path = pathlib.Path(ROOT_DIR + "_perona_gif/")

        files = []

        # Iterate directory
        for path in os.listdir(dir_path):
            # check if current path is a file
            if os.path.isfile(os.path.join(dir_path, path)):
                files.append(path)

        random_index = random.randint(0, len(files) -1)

        random_file = files[random_index]

        dir_path = "_perona_gif/" + random_file

        embed = discord.Embed(title="Perona Gif", description="Perona The Holo Holo Girl")
        file = discord.File(ROOT_DIR + dir_path, filename=random_file)
        embed.set_image(url="attachment://{}".format(random_file))

        await ctx.send(file=file, embed=embed)

    @commands.command(name="rebeccag", aliases=["rg", "gif rebecca"])
    async def rebecca_gif(self, ctx):
        dir_path = pathlib.Path(ROOT_DIR + "_rebecca_gif/")

        files = []

        # Iterate directory
        for path in os.listdir(dir_path):
            # check if current path is a file
            if os.path.isfile(os.path.join(dir_path, path)):
                files.append(path)

        random_index = random.randint(0, len(files) -1)

        random_file = files[random_index]

        dir_path = "_rebecca_gif/" + random_file

        embed = discord.Embed(title="Rebecca Gif", description="Rebecca The Gladiator")
        file = discord.File(ROOT_DIR + dir_path, filename=random_file)
        embed.set_image(url="attachment://{}".format(random_file))

        await ctx.send(file=file, embed=embed)
        
    @commands.command(name="robing", aliases=["rog", "gif robin"])
    async def robin_gif(self, ctx):
        dir_path = pathlib.Path(ROOT_DIR + "_robin_gif/")

        files = []

        # Iterate directory
        for path in os.listdir(dir_path):
            # check if current path is a file
            if os.path.isfile(os.path.join(dir_path, path)):
                files.append(path)

        random_index = random.randint(0, len(files) -1)

        random_file = files[random_index]

        dir_path = "_robin_gif/" + random_file

        embed = discord.Embed(title="Robin Gif", description="Robin The Archaeologist")
        file = discord.File(ROOT_DIR + dir_path, filename=random_file)
        embed.set_image(url="attachment://{}".format(random_file))

        await ctx.send(file=file, embed=embed)
    
    @commands.command(name="sidewomeng", aliases=["swg", "gif side women"])
    async def side_women_gif(self, ctx):
        dir_path = pathlib.Path(ROOT_DIR + "_side_women_gif/")

        files = []

        # Iterate directory
        for path in os.listdir(dir_path):
            # check if current path is a file
            if os.path.isfile(os.path.join(dir_path, path)):
                files.append(path)

        random_index = random.randint(0, len(files) -1)

        random_file = files[random_index]

        dir_path = "_side_women_gif/" + random_file

        embed = discord.Embed(title="Side Women Gif", description="Side Women From One Piece")
        file = discord.File(ROOT_DIR + dir_path, filename=random_file)
        embed.set_image(url="attachment://{}".format(random_file))

        await ctx.send(file=file, embed=embed)

    @commands.command(name="vivig", aliases=["vg", "gif vivi"])
    async def vivi_gif(self, ctx):
        dir_path = pathlib.Path(ROOT_DIR + "_vivi_gif/")

        files = []

        # Iterate directory
        for path in os.listdir(dir_path):
            # check if current path is a file
            if os.path.isfile(os.path.join(dir_path, path)):
                files.append(path)

        random_index = random.randint(0, len(files) -1)

        random_file = files[random_index]

        dir_path = "_vivi_gif/" + random_file

        embed = discord.Embed(title="Vivi Gif", description="Vivi The Alabasta Princess")
        file = discord.File(ROOT_DIR + dir_path, filename=random_file)
        embed.set_image(url="attachment://{}".format(random_file))

        await ctx.send(file=file, embed=embed)

    @commands.command(name="yamatog", aliases=["yg", "gif yamato"])
    async def yamato_gif(self, ctx):
        dir_path = pathlib.Path(ROOT_DIR + "_yamato_gif/")

        files = []

        # Iterate directory
        for path in os.listdir(dir_path):
            # check if current path is a file
            if os.path.isfile(os.path.join(dir_path, path)):
                files.append(path)

        random_index = random.randint(0, len(files) -1)

        random_file = files[random_index]

        dir_path = "_yamato_gif/" + random_file

        embed = discord.Embed(title="Yamato Gif", description="Kazoki Odens Successor")
        file = discord.File(ROOT_DIR + dir_path, filename=random_file)
        embed.set_image(url="attachment://{}".format(random_file))

        await ctx.send(file=file, embed=embed)
    
async def setup(bot):
    await bot.add_cog(HentaiGif(bot))