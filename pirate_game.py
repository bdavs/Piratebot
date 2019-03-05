import discord
import json
import random
from discord.ext import commands
from tokenfile import TOKEN


class Ship:

    def __init__(self, user):
        self.captain = user
        self.cannons = 10
        self.crews = 10
        self.armor = 10
        self.sails = 10

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
    def toJSON(self):
        return {
            'captain': self.captain,
            'cannons': self.cannons,
            'crews': self.crews,
            'armor': self.armor,
            'sails': self.sails
        }

class Pirate:

    def __init__(self, bot):
        self.bot = bot

# maybe be safe later
#    def __unload(self):

    @commands.command(pass_context=True, no_pm=True)
    async def ship(self, ctx):
        """look at ship."""
        myship = Ship(ctx.message.author.name)
        sometext = myship.info()
        await self.bot.say('your ship is fucking awesome, here\'s what its got: \n'+sometext)
        ships.append(myship.toJSON())
        jsonData = ships
        print(ships, myship.toJSON())
        with open("ship_file.json", "w") as write_file:
            json.dump(jsonData, write_file)

    @commands.command(pass_context=True, no_pm=True)
    async def fight(self, ctx):
        """starts a fight with someone in chat"""
        attacker = ctx.message.author.name
        defenders = ctx.message.mentions
        if not defenders:
            await self.bot.say('Who are you fighting?')
        elif len(defenders)>1:
            await self.bot.say('Who are you fighting? One at a time (for now)')
        else:
            defender = defenders[0].name
            await self.bot.say('{0} has attacked {1}'.format(attacker, defender))

            attack = random.randint(1, 100)
            defense = random.randint(1, 100)
            #attack +=
            if attack > defense:
                winner = attacker
            else:
                winner = defender

            await self.bot.say('{0} shot {2} cannonballs and {1} shot {3}. {4} is the winner!'.format(attacker, defender, attack, defense, winner))


bot = commands.Bot(command_prefix=commands.when_mentioned_or('$'), description='a pirate ship bot')
bot.add_cog(Pirate(bot))

@bot.event
async def on_ready():
    print('Logged in as:\n{0} (ID: {0.id})'.format(bot.user))

with open("ship_file.json", "r") as read_file:
    first = read_file.read(1)
    global ships
    ships = []
    if first:
        ships = json.load(read_file)
        print(ships)

bot.run(TOKEN)
