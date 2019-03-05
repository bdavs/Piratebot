import discord
import asyncio
import json
import random
from discord.ext import commands
from tokenfile import TOKEN

parts = ['cannons', 'crew', 'armor', 'sails']
parts_print = ', '.join(parts)


def write_json_file():
    with open("ship_file.json", "w") as write_file:
        json.dump(ships, write_file)


def find_ship(captain):
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

    def __init__(self, user):
        self.captain = user
        self.cannons = 10
        self.crew = 10
        self.armor = 10
        self.sails = 10

        self.position = 0

    def info(self):
        infostr = "This ship is captained by {4} \nIt has {0} cannons, {1} crew, {2} armor, and {3} sails".\
            format(self.cannons, self.crew, self.armor, self.sails, self.captain)
        return infostr

    def upgrade(self, parameter, amount):
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

        ships[self.position] = self.to_dict()
        write_json_file()
        return True

    def to_dict(self):
        return {
            'captain': self.captain,
            'cannons': self.cannons,
            'crew': self.crew,
            'armor': self.armor,
            'sails': self.sails
        }

    def from_dict(self, json_data):

        if json_data is None:
            return None

        self.captain = json_data['captain']
        self.cannons = json_data['cannons']
        self.crew = json_data['crew']
        self.armor = json_data['armor']
        self.sails = json_data['sails']

        self.position = json_data['position']


class Pirate:

    def __init__(self, bot):
        self.bot = bot

# maybe be safe later
#    def __unload(self):

    @commands.command(pass_context=True, no_pm=True)
    async def ship(self, ctx):
        captain = ctx.message.author.name
        """look at ship."""

        myship = find_ship(captain)

        if not myship:
            myship = Ship(captain)
            ships.append(myship.to_dict())
            write_json_file()
            await self.bot.say('Congratulations on the new ship captain! Here is what she\'s got: \n' + myship.info())
        else:
            await self.bot.say('your ship is fucking awesome, here\'s what its got: \n' + myship.info())


    @commands.command(pass_context=True, no_pm=True)
    async def fight(self, ctx):
        """starts a fight with someone in chat"""
        attacker = ctx.message.author.name
        defenders = ctx.message.mentions
        if not defenders:
            await self.bot.say('Who are you fighting?')
            return
        elif len(defenders) > 1:
            await self.bot.say('Who are you fighting? One at a time (for now)')
            return
        else:
            defender = defenders[0].name
            await self.bot.say('{0} has attacked {1}'.format(attacker, defender))

            attacker_ship = find_ship(attacker)
            if not attacker_ship:
                await self.bot.say('{0} does not have a ship! do something to get one'.format(attacker))
                return

            defender_ship = find_ship(defender)
            if not defender_ship:
                await self.bot.say('{0} does not have a ship! There are no fights'
                                   ' on the high sea if there are no ships to fight'.format(defender))
                return

            attack = random.randint(1, 100)
            attack += attacker_ship.cannons + attacker_ship.crew
            attack -= defender_ship.armor + defender_ship.sails

            defense = random.randint(1, 100)
            defense += defender_ship.cannons + defender_ship.crew
            defense -= attacker_ship.armor + attacker_ship.sails

            if attack > defense:
                winner = attacker
            else:
                winner = defender

            await self.bot.say('{0} shot {2} cannonballs and {1} shot {3}.'
                               ' {4} is the winner!'.format(attacker, defender, attack, defense, winner))

    @commands.command(pass_context=True, no_pm=True)
    async def upgrade(self, ctx):
        """upgrade your ship"""
        user = ctx.message.author.name
        user_ship = find_ship(user)
        if not user_ship:
            await self.bot.say('{0}, you do not have a ship to upgrade! type \'{1}\' to get one.'.format(user, '$ship'))
            return

        await bot.send_message(ctx.message.channel,
                               'What part would you like to upgrade? acceptable parameters are {}'.format(parts_print))

        def int_check(m):
            return m.content.isdigit()

        def part_check(m):
            return m.content in parts

        part_msg = await bot.wait_for_message(timeout=30.0, author=ctx.message.author, check=part_check)
        if part_msg is None:
            fmt = 'Sorry, you took too long.'
            await bot.send_message(ctx.message.channel, fmt)
            return

        part = part_msg.content
        await bot.send_message(ctx.message.channel,
                               'Okay, how much would you like to upgrade {} by?'.format(part))

        amount_msg = await bot.wait_for_message(timeout=30.0, author=ctx.message.author, check=int_check)
        if amount_msg is None:
            fmt = 'Sorry, you took too long.'
            await bot.send_message(ctx.message.channel, fmt)
            return

        amount = int(amount_msg.content)
        user_ship.upgrade(part, amount)

        await bot.send_message(ctx.message.channel,
                               'Congrats here is your new ship: {}'.format(user_ship.info()))


bot = commands.Bot(command_prefix=commands.when_mentioned_or('$'), description='a pirate ship bot')
bot.add_cog(Pirate(bot))

@bot.event
async def on_ready():
    print('Logged in as:\n{0} (ID: {0.id})'.format(bot.user))

@bot.check
async def globally_block_dms(ctx):
    return ctx.guild is not None

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
        print(ships)

bot.run(TOKEN)
