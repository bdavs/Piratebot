import discord
import pprint
import asyncio
import json
import random
from discord.ext import commands
from tokenfile import TOKEN

client = discord.Client()

parts = ['cannons', 'crew', 'armor', 'sails']
parts_print = ', '.join(parts)


def write_json_file():
    with open("ship_file.json", "w") as write_file:
        json.dump(ships, write_file)


def find_ship(captain):
    """returns the ship based on captain from ships variable"""
    index = 0
    for s in ships:
        if s['captain'] == captain:
            s['position'] = index
            temp_ship = Ship(captain)
            temp_ship.from_dict(s)
            return temp_ship
        index += 1
    return None


class Ship:
    """defines a single instance of a ship"""
    def __init__(self, user):
        self.captain = user
        self.cannons = 5
        self.crew = 5
        self.armor = 5
        self.sails = 5

        self.gold = 0

        self.position = 0

    def info(self):
        """returns a str with basic parameters of the ship"""
        infostr = "This level {6} ship is captained by {4} \nIt has {0} cannons, {1} crew, {2} armor, and {3} sails \n"\
                  " Its coffers are holding {5} gold".\
            format(self.cannons, self.crew, self.armor, self.sails, self.captain, self.gold, self.level())
        return infostr

    def level(self):
        """returns level of ship based on its primary features"""
        ship_level = self.cannons + self.crew + self.armor + self.sails
        return ship_level

    def upgrade(self, parameter, amount, cost=0):
        """updates the parameters of the ship and subtracts the cost"""
        if parameter == "cannons":
            self.cannons += amount
        elif parameter == "crew":
            self.crew += amount
        elif parameter == "armor":
            self.armor += amount
        elif parameter == "sails":
            self.sails += amount
        else:
            return False
        self.gold -= cost
        ships[self.position] = self.to_dict()
        write_json_file()
        return True

    def to_dict(self):
        """creates a dict from ship params"""
        return {
            'captain': self.captain,
            'cannons': self.cannons,
            'crew': self.crew,
            'armor': self.armor,
            'sails': self.sails,
            'gold': self.gold
        }

    def from_dict(self, json_data):
        """creates a ship based on a dict"""
        if json_data is None:
            return None

        self.captain = json_data['captain']
        self.cannons = json_data['cannons']
        self.crew = json_data['crew']
        self.armor = json_data['armor']
        self.sails = json_data['sails']
        self.gold = json_data['gold']

        # should this be here?
        self.position = json_data['position']


class Pirate:
    """These are the pirate commands"""
    def __init__(self, bot):
        self.bot = bot

# maybe be safe later
#    def __unload(self):

    @commands.command(pass_context=True, no_pm=True, hidden=True)
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

        #draw.polygon([(100,100),(200,200),(1000,1000),(1100,1100)],128,128)
        #draw.line([(500, 200),(600,300)], fill=(128,0,0),width=20)
        #draw.line([(600, 200),(500,300)], fill=(128,0,0),width=20)
        #draw.line((0, im.size[1], im.size[0], 0), fill=(0,128,0), width=10)
        del draw

        # write to stdout
        im.save("marked_treasure_map.png", "PNG")

        await self.bot.send_file(ctx.message.channel, 'marked_treasure_map.png')
#        print(list(ctx.guild.get_all_emojis()))

    @commands.command(pass_context=True, no_pm=True)
    async def ship(self, ctx):
        """look at your ship's info or create one if you're new"""
        captain = ctx.message.author.name

        myship = find_ship(captain)

        if not myship:
            myship = Ship(captain)
            ships.append(myship.to_dict())
            write_json_file()
            await self.bot.say('Congratulations on the new ship, Captain! Here is what she\'s got: \n' + myship.info())
        else:
            await self.bot.say('Your ship is fucking awesome, here\'s what its got: \n' + myship.info())

    @commands.command(pass_context=True, no_pm=True)
    async def fight(self, ctx, defender_msg=None, accept: int = False):
        """starts a fight with someone in chat
        do $fight @victim to attack your victim
        """
        attacker = ctx.message.author.name
        defenders = ctx.message.mentions
        #only continue if valid attacker and defender
        if not defenders:
            await self.bot.say('Who are you fighting?')
            return
        elif len(defenders) > 1:
            await self.bot.say('Who are you fighting? One at a time (for now)')
            return
        else:
            defender = defenders[0].name

            attacker_ship = find_ship(attacker)
            if not attacker_ship:
                await self.bot.say('{0} does not have a ship! $ship to get one'.format(attacker))
                return

            defender_ship = find_ship(defender)
            if not defender_ship:
                await self.bot.say('{0} does not have a ship! There are no fights'
                                   ' on the high sea if there are no ships to fight'.format(defender))
                return

            await self.bot.say('{0} has attacked {1} :rage: '.format(attacker, defender))

            # calculate who wins based on their attack and defense plus random number
            attack = random.randint(1, 100)
            attack += attacker_ship.cannons + attacker_ship.crew
            attack -= defender_ship.armor + defender_ship.sails

            defense = random.randint(1, 100)
            defense += defender_ship.cannons + defender_ship.crew
            defense -= attacker_ship.armor + attacker_ship.sails

            # currently all fights earn 100 gold; to be tuned later
            gold = 100
            if attack > defense:
                winner = attacker
                attacker_ship.gold += gold
                await self.bot.say('{0} shot {2} cannonballs and {1} shot {3}.'
                                   ' {4} is the winner! and earned {5} gold for '
                                   'their coffers'.format(attacker, defender, attack, defense, winner, gold))
            else:
                winner = defender
                await self.bot.say('{0} shot {2} cannonballs and {1} shot {3}.'
                                   ' {4} is the winner! Their ship survives to fight '
                                   'another day.'.format(attacker, defender, attack, defense, winner))

    @commands.command(pass_context=True, no_pm=True)
    async def upgrade(self, ctx):
        """Upgrade your ship"""
        user = ctx.message.author.name
        user_ship = find_ship(user)
        if not user_ship:
            await self.bot.say('{0}, you do not have a ship to upgrade! type \'{1}\' to get one.'.format(user, '$ship'))
            return

        # these checks will ignore any invalid responses
        def int_check(m):
            return m.content.isdigit()

        def part_check(m):
            return m.content in parts

        def y_n_check(m):
            msg = m.content.lower()
            return msg == 'yes' or msg == 'y' or msg == 'no' or msg == 'n'

        await bot.send_message(ctx.message.channel,
                               'What part would you like to upgrade? acceptable parameters are {}'.format(parts_print))

        part_msg = await bot.wait_for_message(timeout=30.0, author=ctx.message.author, check=part_check)
        if part_msg is None:
            fmt = 'Sorry, you took too long.'
            await bot.send_message(ctx.message.channel, fmt)
            return

        part = part_msg.content
        user_dict = user_ship.to_dict()

        await bot.send_message(ctx.message.channel,
                               'Okay, how much would you like to upgrade {} by? '
                               'It is currently level {}'.format(part, user_dict[part]))

        amount_msg = await bot.wait_for_message(timeout=30.0, author=ctx.message.author, check=int_check)
        if amount_msg is None:
            fmt = 'Sorry, you took too long.'
            await bot.send_message(ctx.message.channel, fmt)
            return

        amount = int(amount_msg.content)

        cost = int(amount * 10 + (user_dict[part] + amount) / 10)
        if cost > user_ship.gold:
            await bot.send_message(ctx.message.channel,
                                   'Upgrading {} by {} will cost {}. You only have {} gold. '
                                   'Win some fights to earn more gold.'.format(part, amount, cost, user_ship.gold))
            return

        await bot.send_message(ctx.message.channel,
                               'Upgrading {} by {} will cost {}. You have {} gold, would you like to continue? '
                               '\'yes\' or \'no\''.format(part, amount, cost, user_ship.gold))
        continue_msg = await bot.wait_for_message(timeout=30.0, author=ctx.message.author, check=y_n_check)
        if continue_msg is None:
            fmt = 'Sorry, you took too long.'
            await bot.send_message(ctx.message.channel, fmt)
            return

        msg = continue_msg.content.lower()
        if msg == 'no' or msg == 'n':
            return

        user_ship.upgrade(part, amount, cost)
        await bot.send_message(ctx.message.channel,
                               'Congrats here is your new upgrades: {}'.format(user_ship.info()))


description = 'A pirate ship bot. Lets you fight other users and upgrade your ship. Sail on captain! \n Prefix is $'
bot = commands.Bot(command_prefix=commands.when_mentioned_or('$'), description=description)
bot.add_cog(Pirate(bot))

@bot.event
async def on_ready():
    await bot.change_presence(game=discord.Game(name='Sailing the High Seas | $help'))
    print('Logged in as:\n{0} (ID: {0.id})'.format(bot.user))

"""
@bot.check
async def globally_block_dms(ctx):
    return ctx.guild is not None
"""

"""reading the ship file to add all the users ships to the dataspace"""
with open("ship_file.json", "r") as read_file:
    first = read_file.read(1)
    global ships
    ships = []
    if first:
        read_file.seek(0)
        json_data = json.load(read_file)
        for s in json_data:
            ships.append(s)

        print("here are the ships:")
        pprint.pprint(ships)

bot.run(TOKEN)
