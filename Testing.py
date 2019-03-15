import discord
from discord.ext import commands
import os
from Ship import Ship
import shutil
import requests

import json

encounters_dir = "Encounters"

places = [["place0","place1","place2"],["place3","place4","place5"],["place6","place7","place8"]]
# places = [list(x) for x in zip(places)]


class Testing(commands.Cog):
    """These are the pirate commands"""
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
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

    @raid.command(aliases=['sail'])
    async def move(self, ctx, direction=None):
        captain = ctx.message.author.name
        user_ship = Ship.find_ship(captain)
        current_place = places[user_ship.x][user_ship.y]

        if direction is None:
            await ctx.send('Do we have a heading Captain {}? North, South, East, West'.format(captain))
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

        user_ship.update()

    @raid.command(aliases=['battle', 'attack'])
    async def fight(self, ctx, direction=None):

        return

    @raid.command(pass_context=True, no_pm=True, hidden=True)
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def map(self, ctx, x: int = 200, y: int = 200):
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

        draw.line([(x - size, y - size), (x + size, y + size)], fill=(128, 0, 0), width=width)
        draw.line([(x + size, y - size), (x - size, y + size)], fill=(128, 0, 0), width=width)

        del draw

        im.save("marked_treasure_map.png", "PNG")

        await ctx.send(file=discord.File('marked_treasure_map.png'))

    @commands.command(hidden=True)
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

    @commands.command(hidden=True)
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def test(self, ctx):
        """for testing only
        makes your pfp into a pirate """
        # mentions = ctx.message.mentions
        if ctx.message.mentions:
            url = ctx.message.mentions[0].avatar_url_as(format="png",size=256)
        else:
            url = ctx.message.author.avatar_url_as(format="png",size=256)

        print(url)
        from PIL import Image, ImageDraw

        avatar_raw = "assets/avatar.png"

        with requests.get(url, stream=True) as r:
            with open("assets/avatar.png", 'wb') as out_file:
                shutil.copyfileobj(r.raw, out_file)
                out_file.close()

        avatar = Image.open("assets/avatar.png")
        hat = Image.open("assets/hat.png").convert('RGBA')
        eyepatch = Image.open('assets/eyepatch.png').convert('RGBA')

        # hat = hat.convert('RGBA')
        hat = hat.resize(size=(200, 100))
        avatar.paste(hat, box=(10, 10), mask=hat)

        eyepatch = eyepatch.resize(size=(160, 80))
        avatar.paste(eyepatch, box=(30, 85), mask=eyepatch)

        avatar.save("assets/avatar_pirate.png", "PNG")

        await ctx.send(file=discord.File('assets/avatar_pirate.png'))

        """
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
        """


class Encounter:
    def __init__(self, name, level, attack, defense, dodge, reward, description, on_land, special_encounter):
        self.name = name
        self.level = level
        self.attack = attack
        self.defense = defense
        self.dodge = dodge
        self.reward = reward
        self.description = description
        self.on_land = on_land
        self.special_encounter = special_encounter

    """
    def __init__(self):
        self.name = ""
        self.level = 0
        self.attack = 0
        self.defense = 0
        self.dodge = 0
        self.reward = [0, ""]
        self.description = ""
        self.on_land = False
        self.special_encounter = False

        # self.encounter_chance
        """

    @classmethod
    def fromfilename(cls, filename):
        """"Initialize MyData from a file"""
        data = open(filename).readlines()
        return cls(data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8])

    def attack(self):
        return

    def defend(self):
        return

    def reward(self):
        return


for filename in os.listdir(encounters_dir):
    full_filename = encounters_dir + "/" + filename
    data = open(full_filename, "r")
    data = data.read().split("\n")
    Encounter(data[0], int(data[1]), int(data[2]), int(data[3]), int(data[4]), list(data[3].split(",")), data[6], bool(data[7]), bool(data[8]))
