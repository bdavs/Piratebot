import discord
from discord.ext import commands
import shutil
import requests

class Testing(commands.Cog):
    """These are the pirate commands"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True)
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def list_emojis(self, ctx, user=None):

        print(self.bot.emojis)
        await ctx.send(str(self.bot.emojis))

    @commands.command(hidden=True)
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def embed_test(self, ctx, user=None):

        # print(self.bot.emojis)
        #await ctx.send_typing(ctx.message.channel)
        em = discord.Embed(title='My Embed Title', description='My Embed Content.', colour=0xDD0000)
        em.set_author(name=ctx.message.author.name, icon_url=ctx.message.author.avatar_url)

        em.add_field(name="Ship Level", value="x", inline=False)
        em.add_field(name="Field2", value="hi2", inline=True)
        em.add_field(name="Field3", value="hi3", inline=True)
        em_msg = await ctx.send(ctx.message.channel, embed=em)
#        await em_msg.edit(embed=em)

        await ctx.send("<:pirateThink:550815188119715840>")

        """
        hi <:pirateThink:550815188119715840>
        """

    @commands.command(hidden=True)
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def piratify(self, ctx, resize: int = 100, x: int = 10, y: int = 10):
        """for testing only
        makes your pfp into a pirate """
        # mentions = ctx.message.mentions
        if ctx.message.mentions:
            url = ctx.message.mentions[0].avatar_url_as(format="png", size=256)
        else:
            url = ctx.message.author.avatar_url_as(format="png", size=256)

        print(url)
        from PIL import Image, ImageDraw

        avatar_raw = "assets/avatar.png"

        with requests.get(url, stream=True) as r:
            with open(avatar_raw, 'wb') as out_file:
                shutil.copyfileobj(r.raw, out_file)
                out_file.close()

        avatar = Image.open(avatar_raw)
        hat = Image.open("assets/hat.png").convert('RGBA')
        eyepatch = Image.open('assets/eyepatch.png').convert('RGBA')

        hat_width = int(200/100 * resize)
        hat_height = int(100/100 * resize)
        hat = hat.resize(size=(hat_width, hat_height))

        eyepatch_width = int(160/100 * resize)
        eyepatch_height = int(80/100 * resize)
        eyepatch = eyepatch.resize(size=(eyepatch_width, eyepatch_height))

        hat_x = int(0 + x)
        hat_y = int(0 + y)
        avatar.paste(hat, box=(hat_x, hat_y), mask=hat)

        eyepatch_x = int(20 + x)
        eyepatch_y = int(75 + y)
        avatar.paste(eyepatch, box=(eyepatch_x, eyepatch_y), mask=eyepatch)

        avatar.save("assets/avatar_pirate.png", "PNG")

        await ctx.send(file=discord.File('assets/avatar_pirate.png'))


