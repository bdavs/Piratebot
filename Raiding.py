import discord
from discord.ext import commands
import os, random
from Ship import Ship

encounters_dir = "Encounters"

places = [["place0","place1","place2"],["place3","place4","place5"],["place6","place7","place8"]]
# places = [list(x) for x in zip(places)]


class Raiding(commands.Cog):
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
            em.add_field(name='Location:', value='({},{}) \"{}\"'.format(user_ship.x, user_ship.y, current_place),
                         inline=False)
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

        await ctx.send('Yer new location is {},{}'.format(user_ship.x,user_ship.y))

        user_ship.update()

    @raid.command(aliases=['battle', 'attack', 'encounter'])
    async def fight(self, ctx):

        captain = ctx.message.author.name
        user_ship = Ship.find_ship(captain)
        if not user_ship:
            await ctx.send('{0}, you do not have a ship! `$ship` to get one'.format(ctx.message.author.mention))
            return
        encounter_file = random.choice(os.listdir(encounters_dir))
        encounter = Encounter.from_filename(encounters_dir + "/" + encounter_file)

        await ctx.send('You encounter a {}, {} \n it can deal {} damage'.format(encounter.name, encounter.description, encounter.attack))

        return

    @raid.command(hidden=True)
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def map(self, ctx, x: int = 200, y: int = 200):
        """for testing only
        currently takes an x and a y and crates an X on the treasure map """

        captain = ctx.message.author.name
        user_ship = Ship.find_ship(captain)

        # tune size for length of crosses in X
        size = 25

        # tune width for thickness of X
        width = 20

        from PIL import Image, ImageDraw

        im = Image.open("assets/treasure_map.png")

        # draw.line((0, im.size[1], im.size[0], 0), fill=(0,128,0), width=10)
        x = im.size[0] / 3 * (user_ship.x + 1)
        y = im.size[1] - (im.size[1] / 3 * (user_ship.y + 1))
        # print(x,y)

#        x = int(x)
#        y = int(y)

        draw = ImageDraw.Draw(im)

        draw.line([(x - size, y - size), (x + size, y + size)], fill=(128, 0, 0), width=width)
        draw.line([(x + size, y - size), (x - size, y + size)], fill=(128, 0, 0), width=width)

        del draw

        im.save("marked_treasure_map.png", "PNG")

        await ctx.send(file=discord.File('marked_treasure_map.png'))


class Encounter:
    def __init__(self, name, level, attack, defense, dodge, reward, description, special_encounter):
        self.name = name
        self.level = level
        self.attack = attack
        self.defense = defense
        self.dodge = dodge
        self.reward = reward
        self.description = description
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
        self.special_encounter = False

        # self.encounter_chance
        """

    @classmethod
    def from_filename(cls, filename):
        """"Initialize MyData from a file"""
        data = []
        with open(filename) as f:
            for line in f:
                data.append(line.strip())

        return cls(data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7])

    def attack(self):
        return

    def defend(self):
        return

    def reward(self):
        return

"""
encounters = []
for filename in os.listdir(encounters_dir):
    full_filename = encounters_dir + "/" + filename
    data = open(full_filename, "r")
    data = data.read().split("\n")
    encounters.append(Encounter(data[0], int(data[1]), int(data[2]), int(data[3]), int(data[4]), list(data[3].split(",")), data[6], bool(data[7])))
"""
