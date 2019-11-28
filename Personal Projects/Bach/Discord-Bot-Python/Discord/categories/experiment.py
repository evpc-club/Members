import discord
from discord.ext import commands

# This category is for testing purpose.
class Experiment(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(hidden = True)
    async def testPaginator(self, ctx):
        '''
        {0}
        '''
        embed1 = discord.Embed()
        embed1.add_field(name = "Hola1", value = "Yo1")
        embed2 = discord.Embed()
        embed2.add_field(name = "Hola2", value = "Yo2")
        embed3 = discord.Embed()
        embed3.add_field(name = "Hola3", value = "Yo3")
        from categories.templates.navigate import Pages
        navigator = Pages()
        navigator.add_page(embed1)
        navigator.add_page(embed2)
        navigator.add_page(embed3)

        await navigator.event(self.bot, ctx.channel)



def setup(bot):
    bot.add_cog(Experiment(bot))