import discord
from discord.ext import commands
from Ship import Ship
import json

places = [["place0","place1","place2"],["place3","place4","place5"],["place6","place7","place8"]]
# places = [list(x) for x in zip(places)]

class Testing(commands.Cog):
    """These are the pirate commands"""
    def __init__(self, bot):
        self.bot = bot

    @commands.group(pass_context=True, no_pm=True)
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def raid(self, ctx):
        if not ctx.invoked_subcommand:  # display raid information

            captain = ctx.message.author.name
            user_ship = Ship.find_ship(captain)
            current_place = places[user_ship.x][user_ship.y]

            em = discord.Embed(title="{}'s Raiding party".format(captain),
                               description="Level: {}".format(user_ship.level()), colour=0x33aa33)
            em.set_author(name=captain + '\'s Ship', icon_url=ctx.message.author.avatar_url)
            em.add_field(name='Location:', value='({},{}) \"{}\"'.format(user_ship.x, user_ship.y, current_place), inline=False)
            em.add_field(name="What\'s here:", value="things, maybe put this in the footer?", inline=True)

            em.set_footer(text="Your ship's coffers hold {} gold".format(user_ship.gold),
                          icon_url="https://cdn.discordapp.com/emojis/554730061463289857.gif")
            await ctx.send(embed=em)

    @raid.command(pass_context=True, no_pm=True)
    async def move(self, ctx, direction=None):
        captain = ctx.message.author.name
        user_ship = Ship.find_ship(captain)
        current_place = places[user_ship.x][user_ship.y]

        if direction is None:
            await ctx.send('Do we have a heading captain {}? North, South, East, West'.format(captain))
            return
        direction = direction.lower()
        if direction == 'north' or direction == 'up':
            if user_ship.y + 1 > 2:
                await ctx.send('Ye reached the edge of the map. Here thar be dragons. Ye turned back.')
                return
            user_ship.y += 1
        elif direction == 'south' or direction == 'down':
            if user_ship.y - 1 < 0:
                await ctx.send('Ye reached the edge of the map. Here thar be dragons. Ye turned back.')
                return
            user_ship.y -= 1
        elif direction == 'east' or direction == 'right':
            if user_ship.y + 1 > 2:
                await ctx.send('Ye reached the edge of the map. Here thar be dragons. Ye turned back.')
                return
            user_ship.x += 1
        elif direction == 'west' or direction == 'left':
            if user_ship.y + 1 > 2:
                await ctx.send('Ye reached the edge of the map. Here thar be dragons. Ye turned back.')
                return
            user_ship.x -= 1
        else:
            await ctx.send('invalid direction')

        Ship.update(user_ship)



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

        await ctx.send(file=discord.File('marked_treasure_map.png'))



