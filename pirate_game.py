DEV = True
import discord
import error_handler
import random
from discord.ext import commands
from Ship import Ship
from Raiding import Raiding,Encounter
if DEV:
    from dev_tokenfile import TOKEN
    COOLDOWN = 30
    from Testing import Testing
else:
    from tokenfile import TOKEN
    COOLDOWN = 30

# client = discord.Client()


# Constants
parts = ['Cannons', 'Crew', 'Armor', 'Sails']
parts_emotes = ['<a:cannon:554558216889958400> Cannons', '<a:crew:554559291609055242> Crew',
                '<a:armor:554559559545520128> Armor', ' <a:sails:554558739747831808> Sails']
parts_print = '\n'.join(parts_emotes)

# 20 hours for each daily now
Daily_Time = 60 * 60 * 20
Daily_Gold = 300



class Pirate(commands.Cog):
    """These are the pirate commands"""
    def __init__(self, bot):
        self.bot = bot

    @commands.group(aliases=['info'])
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def ship(self, ctx):
        """look at your ship's info or create one if you're new
        You may also look at another users ship with $ship @user
        """
        if ctx.invoked_subcommand:
            return
        defenders = ctx.message.mentions
        if defenders:
            for defender in defenders:
                captain = defender.name
                user_ship = Ship.find_ship(captain)
                if not user_ship:
                    await ctx.send("{} does not yet have a ship.".format(captain))
                else:
                    em = discord.Embed(colour=0xAA0000)
                    em.set_author(name=user_ship.ship_name, icon_url=defender.avatar_url)
                    em.add_field(name='Ship Level: {}'.format(str(user_ship.level())),
                                 value="Win/Loss: {}/{}".format(user_ship.win, user_ship.loss), inline=False)
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
            user_ship.update(is_new=True)

            await ctx.send('Congratulations on the new ship, Captain {}! Welcome aboard!'
                           '\nCannons and Crew contribute to your attack,'
                           ' while Armor and Sails contribute to defense\nHere\'s what she\'s got:'.format(captain))

        em = discord.Embed(colour=0xDD0000)
        em.set_author(name=user_ship.ship_name,
                      icon_url=ctx.message.author.avatar_url)
        em.add_field(name='Ship Level: {}'.format(str(user_ship.level())),
                     value="Win/Loss: {}/{}".format(user_ship.win, user_ship.loss), inline=False)
        #em.add_field(name='Ship Level', value=str(user_ship.level()), inline=False)
        em.add_field(name="__Part__", value=parts_print, inline=True)
        em.add_field(name="__Level__", value=user_ship.info(), inline=True)
        em.set_footer(text="Your ship's coffers hold {} gold".format(user_ship.gold),
                      icon_url="https://cdn.discordapp.com/emojis/554730061463289857.gif")
        em_msg = await ctx.send(embed=em)

    @ship.command()
    async def name(self, ctx, *, name=None):
        """naming your ship"""
        captain = ctx.message.author.name
        user_ship = Ship.find_ship(captain)
        if name is None:
            await ctx.send('Your ship\'s current name is {}'.format(user_ship.ship_name))
            return
        user_ship.ship_name = name
        user_ship.update()
        await ctx.send('Your ship\'s new name is {}'.format(user_ship.ship_name))

    @commands.command(aliases=['battle', 'attack'])
    @commands.guild_only()
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
            # reset cooldowns when not successful fights
            # self.fight.reset_cooldown()
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
                attacker_ship.update()
                await ctx.send('A mutiny has started on {0}\'s ship! The treasure hold has been ransacked! '
                                   '{1} gold was taken.'.format(defender, 50))
                return

            defender_ship = Ship.find_ship(defender)
            if not defender_ship:
                await ctx.send('{0} does not have a ship! There are no fights'
                                   ' on the high sea if there are no ships to fight'.format(defender))
                return

            # actually start fight
            em = discord.Embed(title='{0} has attacked {1} :rage: '.format(attacker, defender),  colour=0xDDDD00)

            # calculate who wins based on their attack and defense plus random number
            attacker_ship.repair_hull()
            defender_ship.repair_hull()
            attacker_msg = ''
            defender_msg = ''
            while attacker_ship.hull > 0 and defender_ship.hull > 0:
                attack = random.randint(1, 100)
                attack += attacker_ship.cannons + attacker_ship.crew

                defense = random.randint(1, 100)
                defense += defender_ship.cannons + defender_ship.crew

                defender_ship.damage_hull(attack)
                attacker_ship.damage_hull(defense)

                attacker_msg += 'Fired a volley of **{}** cannonballs <a:cannon:554558216889958400> \n'.format(attack)
                defender_msg += '<a:cannon_reversed:554722119905181735> Return fired a volley of **{}** cannonballs \n'.format(defense)

            # reset hulls just in case
            attacker_ship.repair_hull()
            defender_ship.repair_hull()
            em.add_field(name="__{}__ HP: {}".format(attacker, attacker_ship.hull), value=attacker_msg, inline=True)
            em.add_field(name="__{}__ HP: {}".format(defender, defender_ship.hull), value=defender_msg, inline=True)

            if attacker_ship.hull > defender_ship.hull:  # attacker wins
                # base gold at 100, more gold earned for harder fights, less or easier ones
                gold = 100 + (defender_ship.level() - attacker_ship.level()) * 2
                gold = gold if gold > 0 else 0
                attacker_ship.gold += gold
                attacker_ship.win += 1
                defender_ship.loss += 1
                attacker_ship.update()
                defender_ship.update()

                em.add_field(name='{} is the winner! :crossed_swords:'.format(attacker),
                             value='<a:treasure_chest:554730061463289857> They earned **{}** gold for their coffers.'.format(gold), inline=False)

            else:  # defender wins
                defender_ship.win += 1
                attacker_ship.loss += 1
                attacker_ship.update()
                defender_ship.update()
                em.add_field(name='{} is the winner! :shield:'.format(defender),
                             value=' <a:armor:554559559545520128> Their ship survives to fight another day.', inline=False)

            await ctx.send(embed=em)

    @fight.error
    async def fight_error_handler(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(
                "{}, Your ship is still being repaired from your last fight. It should be done in {} seconds".format(
                    ctx.author.name, int(error.retry_after)))
        elif isinstance(error, commands.NoPrivateMessage):
            try:
                return await ctx.author.send(f'{ctx.command} can not be used in Private Messages.')
            except:
                pass

    @commands.command()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def upgrade(self, ctx, part: str = None, amount=None):
        """Upgrade your ship"""
        user = ctx.message.author.name
        user_ship = Ship.find_ship(user)
        if not user_ship:
            await ctx.send('{0}, you do not have a ship to upgrade! Type `$ship` to get one.'.format(ctx.message.author.mention))
            return

        if not part:
            em = discord.Embed(title='Ship Upgrades', description=str("Current Level: " + str(user_ship.level())), colour=0x3796ff)
            em.set_author(name=ctx.message.author.name + '\'s Ship has docked in the port', icon_url=ctx.message.author.avatar_url)
            em.add_field(name="__Part__", value=parts_print, inline=True)
            em.add_field(name="__Current Level__", value=user_ship.info(), inline=True)
            em.add_field(name="__Next Upgrade Costs__", value=user_ship.upgrade_costs(), inline=True)
            em.add_field(name="To upgrade: `$upgrade part`", value="You can also say `$upgrade part amount` or `$upgrade part max` to upgrade multiple levels", inline=False)
            em.set_footer(text="Your ship's coffers hold {} gold".format(user_ship.gold),
                          icon_url="https://cdn.discordapp.com/emojis/554730061463289857.gif")
            em_msg = await ctx.send(embed=em)
            return

        part = part.lower()
        if part not in map(str.lower, parts):
            await ctx.send('Sorry, that\'s not an upgradable part. What part would you like to upgrade? '
                           'Acceptable parameters are:\n{}'.format(parts_print))
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
            elif amount.lower() == 'max':
                cost = 0
                amount = 0
                while cost < user_ship.gold:
                    amount += 1
                    cost = Ship.calc_upgrade(user_dict[part], amount)

                # stop over-drafting gold
                amount -= 1
                cost = Ship.calc_upgrade(user_dict[part], amount)

                if amount == 0:
                    amount = 1
                    cost = Ship.calc_upgrade(user_dict[part], amount)
                    await ctx.send('Upgrading {} by {} will cost {}. You only have {} gold. '
                                   'Win some fights to earn more gold.'.format(part, amount, cost, user_ship.gold))
                    return

        if cost > user_ship.gold:
            await ctx.send('Upgrading {} by {} will cost {}. You only have {} gold. '
                           'Win some fights to earn more gold.'.format(part, amount, cost, user_ship.gold))
            return

        user_ship.upgrade(part, amount, cost)

        em = discord.Embed(title="Upgraded {} by {} level(s)".format(part, amount),
                           description="This cost {} gold".format(cost), colour=0x3796ff)
        em.set_author(name=ctx.message.author.name + '\'s Ship', icon_url=ctx.message.author.avatar_url)
        em.add_field(name='Ship Level', value=str(user_ship.level()), inline=False)
        em.add_field(name="__Part__", value=parts_print, inline=True)
        em.add_field(name="__Level__", value=user_ship.info(), inline=True)
        em.set_footer(text="Your ship's coffers hold {} gold".format(user_ship.gold),
                      icon_url="https://cdn.discordapp.com/emojis/554730061463289857.gif")
        em_msg = await ctx.send(embed=em)

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, Daily_Time, commands.BucketType.user)
    async def daily(self, ctx):
        captain = ctx.message.author.name
        user_ship = Ship.find_ship(captain)
        user_ship.gold += Daily_Gold
        user_ship.update()
        await ctx.send('You earned {} gold for your daily. Come back tomorrow for more'.format(Daily_Gold))

    @daily.error
    async def daily_error_handler(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            seconds = int(error.retry_after)
            hours = seconds / 3600
            minutes = seconds / 60
            if hours > 1:
                await ctx.send(
                    "{}, Your daily is not available yet. It should be available in {:0.1f} hours".format(
                        ctx.author.name, hours))
            elif minutes > 1:
                await ctx.send(
                    "{}, Your daily is not available yet. It should be available in {:0.1f} minutes".format(
                        ctx.author.name, minutes))
            else:
                await ctx.send(
                    "{}, Your daily is not available yet. It should be available in {:0.0f} seconds".format(
                        ctx.author.name, seconds))
        elif isinstance(error, commands.NoPrivateMessage):
            try:
                return await ctx.author.send(f'{ctx.command} can not be used in Private Messages.')
            except:
                pass

if __name__ == "__main__":
    description = 'A pirate ship bot. Lets you fight other users and upgrade your ship. Sail on captain! \n Prefix is $'
    bot = commands.Bot(command_prefix=commands.when_mentioned_or('$'), description=description, case_insensitive=True)
    bot.add_cog(Pirate(bot))
    error_handler.setup(bot)
    if DEV:  # to be used when testing
        bot.add_cog(Testing(bot))
        bot.add_cog(Raiding(bot))


    @bot.event
    async def on_ready():
        """ran once connected. good place for environment changes"""
        await bot.change_presence(activity=discord.Game(name='Sailing the High Seas | $help'))
        print('Logged in as:\n{0} (ID: {0.id})'.format(bot.user))

# if __name__ == "__main__":
    bot.run(TOKEN)
