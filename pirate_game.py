DEV = True
import discord

import random
from discord.ext import commands
from Ship import Ship
if DEV:
    from dev_tokenfile import TOKEN
    COOLDOWN = 1
    from Testing import Testing
else:
    from tokenfile import TOKEN
    COOLDOWN = 30

client = discord.Client()

parts = ['Cannons', 'Crew', 'Armor', 'Sails']
parts_emotes = ['<a:cannon:554558216889958400> Cannons', '<a:crew:554559291609055242> Crew',
                '<a:armor:554559559545520128> Armor', ' <a:sails:554558739747831808> Sails']
parts_print = '\n'.join(parts_emotes)


class Pirate(commands.Cog):
    """These are the pirate commands"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, no_pm=True, aliases=['info'])
    @commands.cooldown(1, COOLDOWN, commands.BucketType.user)
    async def ship(self, ctx):
        """look at your ship's info or create one if you're new
        You may also look at another users ship with $ship @user
        """
        defenders = ctx.message.mentions
        if defenders:
            for defender in defenders:
                captain = defender.name
                user_ship = Ship.find_ship(captain)
                if not user_ship:
                    await ctx.send("{} does not yet have a ship.".format(captain))
                else:
                    em = discord.Embed(title='Ship Level', description=str(user_ship.level()), colour=0xAA0000)
                    em.set_author(name=captain + '\'s Ship', icon_url=defender.avatar_url)
                    em.add_field(name="__Part__", value=parts_print, inline=True)
                    em.add_field(name="__Level__", value=user_ship.info(), inline=True)
                    em.set_footer(text="Their ship's coffers hold {} gold".format(user_ship.gold),
                                  icon_url="https://cdn.discordapp.com/emojis/554730061463289857.gif")
                    em_msg = await ctx.send(embed=em)
            return

        captain = ctx.message.author.name
        user_ship = Ship.find_ship(captain)

        if not user_ship:
            user_ship = Ship(captain)
            Ship.update(user_ship, is_new=True)

            await ctx.send('Congratulations on the new ship, Captain {}! Welcome aboard!'
                           '\nCannons and Crew contribute to your attack,'
                           ' while Armor and Sails contribute to defense\nHere\'s what she\'s got:'.format(captain))

        em = discord.Embed(title='Ship Level', description=str(user_ship.level()), colour=0xDD0000)
        em.set_author(name=ctx.message.author.name + '\'s Ship', icon_url=ctx.message.author.avatar_url)
        em.add_field(name="__Part__", value=parts_print, inline=True)
        em.add_field(name="__Level__", value=user_ship.info(), inline=True)
        em.set_footer(text="Your ship's coffers hold {} gold".format(user_ship.gold),
                      icon_url="https://cdn.discordapp.com/emojis/554730061463289857.gif")
        em_msg = await ctx.send(embed=em)

    @commands.command(pass_context=True, no_pm=True, aliases=['battle', 'attack'])
    @commands.cooldown(1, COOLDOWN, commands.BucketType.user)
    async def fight(self, ctx):
        """starts a fight with someone in chat
        do $fight @victim to attack your victim
        """
        attacker = ctx.message.author.name
        defenders = ctx.message.mentions
        # only continue if valid attacker and defender
        attacker_ship = Ship.find_ship(attacker)
        if not attacker_ship:
            await ctx.send('{0}, you do not have a ship! `$ship` to get one'.format(ctx.message.author.mention))
            return
        if not defenders:
            await ctx.send('Who are you fighting? `$fight @user` to fight someone')
            return
        elif len(defenders) > 1:
            await ctx.send('Who are you fighting? One at a time (for now)')
            return
        else:
            defender = defenders[0].name

            if attacker == defender:
                attacker_ship.gold -= 50
                if attacker_ship.gold < 0:
                    attacker_ship.gold = 0
                Ship.update(attacker_ship)
                await ctx.send('A mutiny has started on {0}\'s ship! The treasure hold has been ransacked! '
                                   '{1} gold was taken.'.format(defender, 50))
                return

            defender_ship = Ship.find_ship(defender)
            if not defender_ship:
                await ctx.send('{0} does not have a ship! There are no fights'
                                   ' on the high sea if there are no ships to fight'.format(defender))
                return

            #actually start fight
            em = discord.Embed(title='{0} has attacked {1} :rage: '.format(attacker, defender),  colour=0xDDDD00)

            # calculate who wins based on their attack and defense plus random number
            attacker_ship.repair_hull()
            defender_ship.repair_hull()
            attacker_msg = ''
            defender_msg = ''
            while attacker_ship.hull > 0 and defender_ship.hull > 0:
                attack = random.randint(1, 100)
                attack += attacker_ship.cannons + attacker_ship.crew
                # attack -= defender_ship.armor + defender_ship.sails

                defense = random.randint(1, 100)
                defense += defender_ship.cannons + defender_ship.crew
                # defense -= attacker_ship.armor + attacker_ship.sails

                defender_ship.damage_hull(attack)
                attacker_ship.damage_hull(defense)

                attacker_msg +=  'Fired a volley of **{}** cannonballs <a:cannon:554558216889958400> \n'.format(attack)
                defender_msg += '<a:cannon_reversed:554722119905181735> Returned fired a volley of **{}** cannonballs \n'.format(defense)

            em.add_field(name="__{}__".format(attacker), value=attacker_msg, inline=True)
            em.add_field(name="__{}__".format(defender), value=defender_msg, inline=True)

            if attacker_ship.hull > defender_ship.hull:

                # base gold at 100, more gold earned for harder fights, less or easier ones
                gold = 100 + (defender_ship.level() - attacker_ship.level()) * 2
                gold = gold if gold > 0 else 0
                attacker_ship.gold += gold
                Ship.update(attacker_ship)

                em.add_field(name='{} is the winner! :crossed_swords:'.format(attacker),
                             value='<a:treasure_chest:554730061463289857> They earned **{}** gold for their coffers.'.format(gold), inline=False)

            else:
                em.add_field(name='{} is the winner! :shield:'.format(defender),
                             value=' <a:armor:554559559545520128> Their ship survives to fight another day.', inline=False)

            await ctx.send(embed=em)

            # reset hulls just in case
            attacker_ship.repair_hull()
            defender_ship.repair_hull()

    @commands.command(pass_context=True, no_pm=True)
    @commands.cooldown(1, COOLDOWN, commands.BucketType.user)
    async def upgrade(self, ctx, part: str=None, amount=None):
        """Upgrade your ship"""
        user = ctx.message.author.name
        user_ship = Ship.find_ship(user)
        if not user_ship:
            await ctx.send('{0}, you do not have a ship to upgrade! Type `$ship` to get one.'.format(ctx.message.author.mention))
            return

        if not part:
            em = discord.Embed(title='Ship Upgrades', description=str("currently level: " + str(user_ship.level())), colour=0xDD0000)
            em.set_author(name=ctx.message.author.name + '\'s Ship has docked in the port', icon_url=ctx.message.author.avatar_url)
            em.add_field(name="__Part__", value=parts_print, inline=True)
            em.add_field(name="__Current Level__", value=user_ship.info(), inline=True)
            em.add_field(name="__Next Upgrade Costs__", value=user_ship.upgrade_costs(), inline=True)
            em.add_field(name="To upgrade: `$upgrade part`", value="you can also say `$upgrade part amount` or `$upgrade part max` to upgrade multiple levels", inline=False)
            em.set_footer(text="Your ship's coffers hold {} gold".format(user_ship.gold),
                          icon_url="https://cdn.discordapp.com/emojis/554730061463289857.gif")
            em_msg = await ctx.send(embed=em)
            return

        part = part.lower()
        if part not in map(str.lower, parts):
            await ctx.send('Sorry, that\'s not an upgradable part. What part would you like to upgrade? Acceptable parameters are:\n{}'.format(parts_print))
            return

        user_dict = user_ship.to_dict()

        if not amount:
            # only upgrade by 1
            cost = Ship.calc_upgrade(user_dict[part])
            amount = 1
        else:
            if amount.isdigit():
                amount = int(amount)
                cost = Ship.calc_upgrade(user_dict[part], amount)
                await ctx.send('AMOUNT INCLUDED Upgrading {} by {} will cost {}. You only have {} gold. '
                               'Win some fights to earn more gold.'.format(part, amount, cost, user_ship.gold))
            elif amount.lower() == 'max':
                cost = 0
                amount = 0
                while cost < user_ship.gold:
                    amount += 1
                    cost = Ship.calc_upgrade(user_dict[part], amount)

                #stop overdrafting gold
                amount -= 1
                cost = Ship.calc_upgrade(user_dict[part], amount)

                if amount == 0:
                    amount = 1
                    cost = Ship.calc_upgrade(user_dict[part], amount)
                    await ctx.send('Upgrading {} by {} will cost {}. You only have {} gold. '
                                   'Win some fights to earn more gold.'.format(part, amount, cost, user_ship.gold))
                    return


#        cost = int(amount * 10 + (user_dict[part] + amount) / 10)
        if cost > user_ship.gold:
            await ctx.send('Upgrading {} by {} will cost {}. You only have {} gold. '
                           'Win some fights to earn more gold.'.format(part, amount, cost, user_ship.gold))
            return

        user_ship.upgrade(part, amount, cost)

        await ctx.send('Congrats here is your new upgrades:')

        em = discord.Embed(title='Ship Level', description=str(user_ship.level()), colour=0xDD0000)
        em.set_author(name=ctx.message.author.name + '\'s Ship', icon_url=ctx.message.author.avatar_url)
        em.add_field(name="__Part__", value=parts_print, inline=True)
        em.add_field(name="__Level__", value=user_ship.info(), inline=True)
        em.set_footer(text="Your ship's coffers hold {} gold".format(user_ship.gold),
                      icon_url="https://cdn.discordapp.com/emojis/554730061463289857.gif")
        em_msg = await ctx.send(embed=em)


description = 'A pirate ship bot. Lets you fight other users and upgrade your ship. Sail on captain! \n Prefix is $'
bot = commands.Bot(command_prefix=commands.when_mentioned_or('$'), description=description, case_insensitive=True)
bot.add_cog(Pirate(bot))

if DEV:
    bot.add_cog(Testing(bot))

@bot.event
async def on_ready():
    """ran once connected. good place for environment changes"""
    await bot.change_presence(activity=discord.Game(name='Sailing the High Seas | $help'))
    print('Logged in as:\n{0} (ID: {0.id})'.format(bot.user))

bot.run(TOKEN)
