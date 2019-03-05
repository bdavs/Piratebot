import discord
import random
from discord.ext import commands
from tokenfile import TOKEN



class Pirate:


    def __init__(self, bot):
        self.bot = bot
        self.voice_states = {}

# maybe be safe later
#    def __unload(self):


    @commands.command(pass_context=True, no_pm=True)
    async def ship(self, args):
        """look at ship."""
        await self.bot.say('your ship is fucking awesome')

    @commands.command(pass_context=True, no_pm=True)
    async def fight(self, ctx):
        """Summons the bot to join your voice channel."""
        attacker = ctx.message.author.name
        defenders = ctx.message.mentions
        if not defenders:
            await self.bot.say('Who are you fighting?')
        else:
            defender = defenders[0].name
            await self.bot.say('You are {0} and attacked {1}'.format(attacker,defender))






bot = commands.Bot(command_prefix=commands.when_mentioned_or('$'), description='a piratey bot')
bot.add_cog(Pirate(bot))

@bot.event
async def on_ready():
    print('Logged in as:\n{0} (ID: {0.id})'.format(bot.user))

bot.run(TOKEN)