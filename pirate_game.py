import discord
import json
import random
from discord.ext import commands
from tokenfile import TOKEN


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
        self.crews = 10
        self.armor = 10
        self.sails = 10

        self.position = 0

    def info(self):
        infostr = "This ship is captained by {4} \nIt has {0} cannons, {1} crew, {2} armor, and {3} sails".\
            format(self.cannons, self.crews, self.armor, self.sails, self.captain)
        return infostr

    def upgrade(self, parameter, amount):
        if parameter == "cannons":
            self.cannons += amount
        elif parameter == "crews":
            self.crews += amount
        elif parameter == "armor":
            self.armor += amount
        elif parameter == "sails":
            self.sails += amount
        else:
            return "failed"
        return "success"

    def to_dict(self):
        return {
            'captain': self.captain,
            'cannons': self.cannons,
            'crews': self.crews,
            'armor': self.armor,
            'sails': self.sails
        }

    def from_dict(self, json_data):

        if json_data is None:
            return None

        self.captain = json_data['captain']
        self.cannons = json_data['cannons']
        self.crews = json_data['crews']
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
            print('appended')

        else:
            print(myship.upgrade("crews", 10))
            ships[myship.position] = myship.to_dict()
            print('upgraded')

        with open("ship_file.json", "w") as write_file:
            json.dump(ships, write_file)

        await self.bot.say('your ship is fucking awesome, here\'s what its got: \n' + myship.info())

    @commands.command(pass_context=True, no_pm=True)
    async def fight(self, ctx):
        """starts a fight with someone in chat"""
        attacker = ctx.message.author.name
        defenders = ctx.message.mentions
        if not defenders:
            await self.bot.say('Who are you fighting?')
            return
        elif len(defenders)>1:
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
            attack += attacker_ship.cannons + attacker_ship.crews
            attack -= defender_ship.armor + defender_ship.sails

            defense = random.randint(1, 100)
            defense += defender_ship.cannons + defender_ship.crews
            defense -= attacker_ship.armor + attacker_ship.sails

            if attack > defense:
                winner = attacker
            else:
                winner = defender

            await self.bot.say('{0} shot {2} cannonballs and {1} shot {3}.'
                               ' {4} is the winner!'.format(attacker, defender, attack, defense, winner))


bot = commands.Bot(command_prefix=commands.when_mentioned_or('$'), description='a pirate ship bot')
bot.add_cog(Pirate(bot))

@bot.event
async def on_ready():
    print('Logged in as:\n{0} (ID: {0.id})'.format(bot.user))


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
