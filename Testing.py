import discord
from discord.ext import commands
from Ship import Ship
import json

places = [["place0","place1","place2"],["place3","place4","place5"],["place6","place7","place8"]]


class Testing(commands.Cog):
    """These are the pirate commands"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, no_pm=True)
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def raid(self, ctx, action: str=None, x:int =None, y:int =None):
        captain = ctx.message.author.name
        user_ship = Ship.find_ship(captain)
        current_place = places[user_ship.x][user_ship.y]
        if not action:  # display raid information
            em = discord.Embed(title="{}'s Raiding party".format(captain),
                               description="Level: {}".format(user_ship.level()), colour=0x33aa33)
            em.set_author(name=captain + '\'s Ship', icon_url=ctx.message.author.avatar_url)
            em.add_field(name='Location:', value='({},{}) \"{}\"'.format(user_ship.x, user_ship.y, current_place), inline=False)
            em.add_field(name="What\'s here:", value="things, maybe put this in the footer?", inline=True)

            em.set_footer(text="Your ship's coffers hold {} gold".format(user_ship.gold),
                          icon_url="https://cdn.discordapp.com/emojis/554730061463289857.gif")
        if action == 'move':
            return


    @commands.command(pass_context=True, no_pm=True, hidden=True)
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def test2(self, ctx, user=None):

        print(self.bot.emojis)
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


    @commands.command(pass_context=True, no_pm=True, hidden=True)
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def test(self, ctx, x: int = 0, y: int = 0):
        """for testing only
        currently takes an x and a y and crates an X on the treasure map """
        x = int(x)
        y = int(y)

        # tune size for length of crosses in X
        size = 25

        # tune width for thickness of X
        width = 20

        from PIL import Image, ImageDraw

        im = Image.open("assets/treasure_map.png")

        draw = ImageDraw.Draw(im)

        draw.line([(x-size, y-size), (x+size, y+size)], fill=(128, 0, 0), width=width)
        draw.line([(x+size, y-size), (x-size, y+size)], fill=(128, 0, 0), width=width)

        del draw

        im.save("marked_treasure_map.png", "PNG")

        await ctx.send(ctx.message.channel, 'marked_treasure_map.png')



