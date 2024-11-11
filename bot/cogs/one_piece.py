# from ast import alias
# from email.mime import image
# from genericpath import isfile
# import pathlib
# from pydoc import describe
# from discord.ext import commands
# import discord
# import typing as t
# import random
# import os
#
# ROOT_DIR = "./hentai/one_piece/"
#
# class HentaiOnePiece(commands.Cog):
#     def __init__(self, bot):
#         self.bot = bot
#
#     async def cog_check(self, ctx):
#         if isinstance(ctx.channel, discord.DMChannel):
#             await ctx.send("Hentai commands are not available in DMs.")
#             return False
#
#         return True
#
#     @commands.command(name="nami")
#     async def nami(self, ctx):
#         dir_path = pathlib.Path(ROOT_DIR + "nami/")
#
#         files = []
#
#         # Iterate directory
#         for path in os.listdir(dir_path):
#             # check if current path is a file
#             if os.path.isfile(os.path.join(dir_path, path)):
#                 files.append(path)
#
#         random_index = random.randint(0, len(files) -1)
#
#         random_file = files[random_index]
#
#         dir_path = "nami/" + random_file
#
#         embed = discord.Embed(title="Nami", description="The Cat Burgalar")
#         file = discord.File(ROOT_DIR + dir_path, filename=random_file)
#         embed.set_image(url="attachment://{}".format(random_file))
#
#         await ctx.send(file=file, embed=embed)
#
#     @commands.command(name="robin")
#     async def robin(self, ctx):
#         dir_path = pathlib.Path(ROOT_DIR + "robin/")
#
#         files = []
#
#         # Iterate directory
#         for path in os.listdir(dir_path):
#             # check if current path is a file
#             if os.path.isfile(os.path.join(dir_path, path)):
#                 files.append(path)
#
#         random_index = random.randint(0, len(files) -1)
#
#         random_file = files[random_index]
#
#         dir_path = "robin/" + random_file
#
#         embed = discord.Embed(title="Robin", description="The Archaeologist")
#         file = discord.File(ROOT_DIR + dir_path, filename=random_file)
#         embed.set_image(url="attachment://{}".format(random_file))
#
#         await ctx.send(file=file, embed=embed)
#
#     @commands.command(name="baby5")
#     async def baby_5(self, ctx):
#         dir_path = pathlib.Path(ROOT_DIR + "baby_5/")
#
#         files = []
#
#         # Iterate directory
#         for path in os.listdir(dir_path):
#             # check if current path is a file
#             if os.path.isfile(os.path.join(dir_path, path)):
#                 files.append(path)
#
#         random_index = random.randint(0, len(files) -1)
#
#         random_file = files[random_index]
#
#         dir_path = "baby_5/" + random_file
#
#         embed = discord.Embed(title="Baby 5", description="Married to Sai of the Happo Navy")
#         file = discord.File(ROOT_DIR + dir_path, filename=random_file)
#         embed.set_image(url="attachment://{}".format(random_file))
#
#         await ctx.send(file=file, embed=embed)
#
#     @commands.command(name="betty")
#     async def belo_betty(self, ctx):
#         dir_path = pathlib.Path(ROOT_DIR + "belo_betty/")
#
#         files = []
#
#         # Iterate directory
#         for path in os.listdir(dir_path):
#             # check if current path is a file
#             if os.path.isfile(os.path.join(dir_path, path)):
#                 files.append(path)
#
#         random_index = random.randint(0, len(files) -1)
#
#         random_file = files[random_index]
#
#         dir_path = "belo_betty/" + random_file
#
#         embed = discord.Embed(title="Belo Betty", description="The East Army Commander of the Revolutionary Army")
#         file = discord.File(ROOT_DIR + dir_path, filename=random_file)
#         embed.set_image(url="attachment://{}".format(random_file))
#
#         await ctx.send(file=file, embed=embed)
#
#     @commands.command(name="carrot")
#     async def belo_betty(self, ctx):
#         dir_path = pathlib.Path(ROOT_DIR + "carrot/")
#
#         files = []
#
#         # Iterate directory
#         for path in os.listdir(dir_path):
#             # check if current path is a file
#             if os.path.isfile(os.path.join(dir_path, path)):
#                 files.append(path)
#
#         random_index = random.randint(0, len(files) -1)
#
#         random_file = files[random_index]
#
#         dir_path = "carrot/" + random_file
#
#         embed = discord.Embed(title="Carrot", description="One of the Musketeers")
#         file = discord.File(ROOT_DIR + dir_path, filename=random_file)
#         embed.set_image(url="attachment://{}".format(random_file))
#
#         await ctx.send(file=file, embed=embed)
#
#     @commands.command(name="conis")
#     async def conis(self, ctx):
#         dir_path = pathlib.Path(ROOT_DIR + "conis/")
#
#         files = []
#
#         # Iterate directory
#         for path in os.listdir(dir_path):
#             # check if current path is a file
#             if os.path.isfile(os.path.join(dir_path, path)):
#                 files.append(path)
#
#         random_index = random.randint(0, len(files) -1)
#
#         random_file = files[random_index]
#
#         dir_path = "conis/" + random_file
#
#         embed = discord.Embed(title="Conis", description="From Skypiea")
#         file = discord.File(ROOT_DIR + dir_path, filename=random_file)
#         embed.set_image(url="attachment://{}".format(random_file))
#
#         await ctx.send(file=file, embed=embed)
#
#     @commands.command(name="hancock")
#     async def hancock(self, ctx):
#         dir_path = pathlib.Path(ROOT_DIR + "hancock/")
#
#         files = []
#
#         # Iterate directory
#         for path in os.listdir(dir_path):
#             # check if current path is a file
#             if os.path.isfile(os.path.join(dir_path, path)):
#                 files.append(path)
#
#         random_index = random.randint(0, len(files) -1)
#
#         random_file = files[random_index]
#
#         dir_path = "hancock/" + random_file
#
#         embed = discord.Embed(title="Boa Hancock", description="The Snake Princess")
#         file = discord.File(ROOT_DIR + dir_path, filename=random_file)
#         embed.set_image(url="attachment://{}".format(random_file))
#
#         await ctx.send(file=file, embed=embed)
#
#     @commands.command(name="hina")
#     async def hina(self, ctx):
#         dir_path = pathlib.Path(ROOT_DIR + "hina/")
#
#         files = []
#
#         # Iterate directory
#         for path in os.listdir(dir_path):
#             # check if current path is a file
#             if os.path.isfile(os.path.join(dir_path, path)):
#                 files.append(path)
#
#         random_index = random.randint(0, len(files) -1)
#
#         random_file = files[random_index]
#
#         dir_path = "hina/" + random_file
#
#         embed = discord.Embed(title="Hina", description="A Rear Admiral for the Marines")
#         file = discord.File(ROOT_DIR + dir_path, filename=random_file)
#         embed.set_image(url="attachment://{}".format(random_file))
#
#         await ctx.send(file=file, embed=embed)
#
#     @commands.command(name="bonney")
#     async def jewelry_bonney(self, ctx):
#         dir_path = pathlib.Path(ROOT_DIR + "bonney/")
#
#         files = []
#
#         # Iterate directory
#         for path in os.listdir(dir_path):
#             # check if current path is a file
#             if os.path.isfile(os.path.join(dir_path, path)):
#                 files.append(path)
#
#         random_index = random.randint(0, len(files) -1)
#
#         random_file = files[random_index]
#
#         dir_path = "bonney/" + random_file
#
#         embed = discord.Embed(title="Jewelry Bonney", description="The Gluten")
#         file = discord.File(ROOT_DIR + dir_path, filename=random_file)
#         embed.set_image(url="attachment://{}".format(random_file))
#
#         await ctx.send(file=file, embed=embed)
#
#     @commands.command(name="kalifa")
#     async def kalifa(self, ctx):
#         dir_path = pathlib.Path(ROOT_DIR + "kalifa/")
#
#         files = []
#
#         # Iterate directory
#         for path in os.listdir(dir_path):
#             # check if current path is a file
#             if os.path.isfile(os.path.join(dir_path, path)):
#                 files.append(path)
#
#         random_index = random.randint(0, len(files) -1)
#
#         random_file = files[random_index]
#
#         dir_path = "kalifa/" + random_file
#
#         embed = discord.Embed(title="Kalifa", description="From CP9")
#         file = discord.File(ROOT_DIR + dir_path, filename=random_file)
#         embed.set_image(url="attachment://{}".format(random_file))
#
#         await ctx.send(file=file, embed=embed)
#
#     @commands.command(name="kami")
#     async def kami(self, ctx):
#         dir_path = pathlib.Path(ROOT_DIR + "kami/")
#
#         files = []
#
#         # Iterate directory
#         for path in os.listdir(dir_path):
#             # check if current path is a file
#             if os.path.isfile(os.path.join(dir_path, path)):
#                 files.append(path)
#
#         random_index = random.randint(0, len(files) -1)
#
#         random_file = files[random_index]
#
#         dir_path = "kami/" + random_file
#
#         embed = discord.Embed(title="Kami", description="A Mermaid from Fishman Island")
#         file = discord.File(ROOT_DIR + dir_path, filename=random_file)
#         embed.set_image(url="attachment://{}".format(random_file))
#
#         await ctx.send(file=file, embed=embed)
#
#     @commands.command(name="koala")
#     async def koala(self, ctx):
#         dir_path = pathlib.Path(ROOT_DIR + "koala/")
#
#         files = []
#
#         # Iterate directory
#         for path in os.listdir(dir_path):
#             # check if current path is a file
#             if os.path.isfile(os.path.join(dir_path, path)):
#                 files.append(path)
#
#         random_index = random.randint(0, len(files) -1)
#
#         random_file = files[random_index]
#
#         dir_path = "koala/" + random_file
#
#         embed = discord.Embed(title="Koala", description="A Revolutionary Army Officer")
#         file = discord.File(ROOT_DIR + dir_path, filename=random_file)
#         embed.set_image(url="attachment://{}".format(random_file))
#
#         await ctx.send(file=file, embed=embed)
#
#     @commands.command(name="marigold")
#     async def marigold(self, ctx):
#         dir_path = pathlib.Path(ROOT_DIR + "marigold/")
#
#         files = []
#
#         # Iterate directory
#         for path in os.listdir(dir_path):
#             # check if current path is a file
#             if os.path.isfile(os.path.join(dir_path, path)):
#                 files.append(path)
#
#         random_index = random.randint(0, len(files) -1)
#
#         random_file = files[random_index]
#
#         dir_path = "marigold/" + random_file
#
#         embed = discord.Embed(title="Marigold", description="Sister of Boa Hancock")
#         file = discord.File(ROOT_DIR + dir_path, filename=random_file)
#         embed.set_image(url="attachment://{}".format(random_file))
#
#         await ctx.send(file=file, embed=embed)
#
#     @commands.command(name="monet")
#     async def monet(self, ctx):
#         dir_path = pathlib.Path(ROOT_DIR + "monet/")
#
#         files = []
#
#         # Iterate directory
#         for path in os.listdir(dir_path):
#             # check if current path is a file
#             if os.path.isfile(os.path.join(dir_path, path)):
#                 files.append(path)
#
#         random_index = random.randint(0, len(files) -1)
#
#         random_file = files[random_index]
#
#         dir_path = "monet/" + random_file
#
#         embed = discord.Embed(title="Monet", description="A Donquixote Pirate")
#         file = discord.File(ROOT_DIR + dir_path, filename=random_file)
#         embed.set_image(url="attachment://{}".format(random_file))
#
#         await ctx.send(file=file, embed=embed)
#
#     @commands.command(name="olvia")
#     async def olvia(self, ctx):
#         dir_path = pathlib.Path(ROOT_DIR + "olvia/")
#
#         files = []
#
#         # Iterate directory
#         for path in os.listdir(dir_path):
#             # check if current path is a file
#             if os.path.isfile(os.path.join(dir_path, path)):
#                 files.append(path)
#
#         random_index = random.randint(0, len(files) -1)
#
#         random_file = files[random_index]
#
#         dir_path = "olvia/" + random_file
#
#         embed = discord.Embed(title="Olvia", description="Mother of Nico Robin")
#         file = discord.File(ROOT_DIR + dir_path, filename=random_file)
#         embed.set_image(url="attachment://{}".format(random_file))
#
#         await ctx.send(file=file, embed=embed)
#
#     @commands.command(name="nojoki")
#     async def nojoki(self, ctx):
#         dir_path = pathlib.Path(ROOT_DIR + "nojoki/")
#
#         files = []
#
#         # Iterate directory
#         for path in os.listdir(dir_path):
#             # check if current path is a file
#             if os.path.isfile(os.path.join(dir_path, path)):
#                 files.append(path)
#
#         random_index = random.randint(0, len(files) -1)
#
#         random_file = files[random_index]
#
#         dir_path = "nojoki/" + random_file
#
#         embed = discord.Embed(title="Nojoki", description="Sister of Nami")
#         file = discord.File(ROOT_DIR + dir_path, filename=random_file)
#         embed.set_image(url="attachment://{}".format(random_file))
#
#         await ctx.send(file=file, embed=embed)
#
#     @commands.command(name="perona")
#     async def perona(self, ctx):
#         dir_path = pathlib.Path(ROOT_DIR + "perona/")
#
#         files = []
#
#         # Iterate directory
#         for path in os.listdir(dir_path):
#             # check if current path is a file
#             if os.path.isfile(os.path.join(dir_path, path)):
#                 files.append(path)
#
#         random_index = random.randint(0, len(files) -1)
#
#         random_file = files[random_index]
#
#         dir_path = "perona/" + random_file
#
#         embed = discord.Embed(title="Perona", description="The Holo Holo Girl")
#         file = discord.File(ROOT_DIR + dir_path, filename=random_file)
#         embed.set_image(url="attachment://{}".format(random_file))
#
#         await ctx.send(file=file, embed=embed)
#
#     @commands.command(name="pudding")
#     async def pudding(self, ctx):
#         dir_path = pathlib.Path(ROOT_DIR + "pudding/")
#
#         files = []
#
#         # Iterate directory
#         for path in os.listdir(dir_path):
#             # check if current path is a file
#             if os.path.isfile(os.path.join(dir_path, path)):
#                 files.append(path)
#
#         random_index = random.randint(0, len(files) -1)
#
#         random_file = files[random_index]
#
#         dir_path = "pudding/" + random_file
#
#         embed = discord.Embed(title="Pudding", description="Daughter of Big Mom")
#         file = discord.File(ROOT_DIR + dir_path, filename=random_file)
#         embed.set_image(url="attachment://{}".format(random_file))
#
#         await ctx.send(file=file, embed=embed)
#
#     @commands.command(name="rebecca")
#     async def rebecca(self, ctx):
#         dir_path = pathlib.Path(ROOT_DIR + "rebecca/")
#
#         files = []
#
#         # Iterate directory
#         for path in os.listdir(dir_path):
#             # check if current path is a file
#             if os.path.isfile(os.path.join(dir_path, path)):
#                 files.append(path)
#
#         random_index = random.randint(0, len(files) -1)
#
#         random_file = files[random_index]
#
#         dir_path = "rebecca/" + random_file
#
#         embed = discord.Embed(title="Rebecca", description="The Gladiator")
#         file = discord.File(ROOT_DIR + dir_path, filename=random_file)
#         embed.set_image(url="attachment://{}".format(random_file))
#
#         await ctx.send(file=file, embed=embed)
#
#     @commands.command(name="reiju")
#     async def reiju(self, ctx):
#         dir_path = pathlib.Path(ROOT_DIR + "reiju/")
#
#         files = []
#
#         # Iterate directory
#         for path in os.listdir(dir_path):
#             # check if current path is a file
#             if os.path.isfile(os.path.join(dir_path, path)):
#                 files.append(path)
#
#         random_index = random.randint(0, len(files) -1)
#
#         random_file = files[random_index]
#
#         dir_path = "reiju/" + random_file
#
#         embed = discord.Embed(title="Reiju", description="Sister to Black Leg Sanji")
#         file = discord.File(ROOT_DIR + dir_path, filename=random_file)
#         embed.set_image(url="attachment://{}".format(random_file))
#
#         await ctx.send(file=file, embed=embed)
#
#     @commands.command(name="sandersonia")
#     async def sandersonia(self, ctx):
#         dir_path = pathlib.Path(ROOT_DIR + "sandersonia/")
#
#         files = []
#
#         # Iterate directory
#         for path in os.listdir(dir_path):
#             # check if current path is a file
#             if os.path.isfile(os.path.join(dir_path, path)):
#                 files.append(path)
#
#         random_index = random.randint(0, len(files) -1)
#
#         random_file = files[random_index]
#
#         dir_path = "sandersonia/" + random_file
#
#         embed = discord.Embed(title="Sandersonia", description="Sister of Boa Hancock")
#         file = discord.File(ROOT_DIR + dir_path, filename=random_file)
#         embed.set_image(url="attachment://{}".format(random_file))
#
#         await ctx.send(file=file, embed=embed)
#
#     @commands.command(name="shirahoshi")
#     async def shirahoshi(self, ctx):
#         dir_path = pathlib.Path(ROOT_DIR + "shirahoshi/")
#
#         files = []
#
#         # Iterate directory
#         for path in os.listdir(dir_path):
#             # check if current path is a file
#             if os.path.isfile(os.path.join(dir_path, path)):
#                 files.append(path)
#
#         random_index = random.randint(0, len(files) -1)
#
#         random_file = files[random_index]
#
#         dir_path = "shirahoshi/" + random_file
#
#         embed = discord.Embed(title="Shirahoshi", description="Princess of Fishman Island")
#         file = discord.File(ROOT_DIR + dir_path, filename=random_file)
#         embed.set_image(url="attachment://{}".format(random_file))
#
#         await ctx.send(file=file, embed=embed)
#
#     @commands.command(name="smoothie")
#     async def smoothie(self, ctx):
#         dir_path = pathlib.Path(ROOT_DIR + "smoothie/")
#
#         files = []
#
#         # Iterate directory
#         for path in os.listdir(dir_path):
#             # check if current path is a file
#             if os.path.isfile(os.path.join(dir_path, path)):
#                 files.append(path)
#
#         random_index = random.randint(0, len(files) -1)
#
#         random_file = files[random_index]
#
#         dir_path = "smoothie/" + random_file
#
#         embed = discord.Embed(title="Smoothie", description="One of the Three Sweet Generals")
#         file = discord.File(ROOT_DIR + dir_path, filename=random_file)
#         embed.set_image(url="attachment://{}".format(random_file))
#
#         await ctx.send(file=file, embed=embed)
#
#     @commands.command(name="sugar")
#     async def sugar(self, ctx):
#         dir_path = pathlib.Path(ROOT_DIR + "sugar/")
#
#         files = []
#
#         # Iterate directory
#         for path in os.listdir(dir_path):
#             # check if current path is a file
#             if os.path.isfile(os.path.join(dir_path, path)):
#                 files.append(path)
#
#         random_index = random.randint(0, len(files) -1)
#
#         random_file = files[random_index]
#
#         dir_path = "sugar/" + random_file
#
#         embed = discord.Embed(title="Sugar", description="A Donquixote Pirate")
#         file = discord.File(ROOT_DIR + dir_path, filename=random_file)
#         embed.set_image(url="attachment://{}".format(random_file))
#
#         await ctx.send(file=file, embed=embed)
#
#     @commands.command(name="tashigi")
#     async def tashigi(self, ctx):
#         dir_path = pathlib.Path(ROOT_DIR + "tashigi/")
#
#         files = []
#
#         # Iterate directory
#         for path in os.listdir(dir_path):
#             # check if current path is a file
#             if os.path.isfile(os.path.join(dir_path, path)):
#                 files.append(path)
#
#         random_index = random.randint(0, len(files) -1)
#
#         random_file = files[random_index]
#
#         dir_path = "tashigi/" + random_file
#
#         embed = discord.Embed(title="Tashigi", description="A Captain in the Marines")
#         file = discord.File(ROOT_DIR + dir_path, filename=random_file)
#         embed.set_image(url="attachment://{}".format(random_file))
#
#         await ctx.send(file=file, embed=embed)
#
#     @commands.command(name="uta")
#     async def tashigi(self, ctx):
#         dir_path = pathlib.Path(ROOT_DIR + "uta/")
#
#         files = []
#
#         # Iterate directory
#         for path in os.listdir(dir_path):
#             # check if current path is a file
#             if os.path.isfile(os.path.join(dir_path, path)):
#                 files.append(path)
#
#         random_index = random.randint(0, len(files) -1)
#
#         random_file = files[random_index]
#
#         dir_path = "uta/" + random_file
#
#         embed = discord.Embed(title="Tashigi", description="A Captain in the Marines")
#         file = discord.File(ROOT_DIR + dir_path, filename=random_file)
#         embed.set_image(url="attachment://{}".format(random_file))
#
#         await ctx.send(file=file, embed=embed)
#
#     @commands.command(name="viola")
#     async def viola(self, ctx):
#         dir_path = pathlib.Path(ROOT_DIR + "viola/")
#
#         files = []
#
#         # Iterate directory
#         for path in os.listdir(dir_path):
#             # check if current path is a file
#             if os.path.isfile(os.path.join(dir_path, path)):
#                 files.append(path)
#
#         random_index = random.randint(0, len(files) -1)
#
#         random_file = files[random_index]
#
#         dir_path = "viola/" + random_file
#
#         embed = discord.Embed(title="Viola", description="Princess of Dressrosa")
#         file = discord.File(ROOT_DIR + dir_path, filename=random_file)
#         embed.set_image(url="attachment://{}".format(random_file))
#
#         await ctx.send(file=file, embed=embed)
#
#     @commands.command(name="vivi")
#     async def vivi(self, ctx):
#         dir_path = pathlib.Path(ROOT_DIR + "vivi/")
#
#         files = []
#
#         # Iterate directory
#         for path in os.listdir(dir_path):
#             # check if current path is a file
#             if os.path.isfile(os.path.join(dir_path, path)):
#                 files.append(path)
#
#         random_index = random.randint(0, len(files) -1)
#
#         random_file = files[random_index]
#
#         dir_path = "vivi/" + random_file
#
#         embed = discord.Embed(title="Vivi", description="Princess of Alabasta")
#         file = discord.File(ROOT_DIR + dir_path, filename=random_file)
#         embed.set_image(url="attachment://{}".format(random_file))
#
#         await ctx.send(file=file, embed=embed)
#
#     @commands.command(name="yamato")
#     async def vivi(self, ctx):
#         dir_path = pathlib.Path(ROOT_DIR + "yamato/")
#
#         files = []
#
#         # Iterate directory
#         for path in os.listdir(dir_path):
#             # check if current path is a file
#             if os.path.isfile(os.path.join(dir_path, path)):
#                 files.append(path)
#
#         random_index = random.randint(0, len(files) -1)
#
#         random_file = files[random_index]
#
#         dir_path = "yamato/" + random_file
#
#         embed = discord.Embed(title="Yamato", description="The Newest Straw Hat")
#         file = discord.File(ROOT_DIR + dir_path, filename=random_file)
#         embed.set_image(url="attachment://{}".format(random_file))
#
#         await ctx.send(file=file, embed=embed)
#
# async def setup(bot):
#     await bot.add_cog(HentaiOnePiece(bot))