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

    @commands.command(hidden = True)
    async def testMenu(self, ctx):
        embed1 = discord.Embed(title = "Init")
        embed2 = discord.Embed(title = "Page1")
        embed3 = discord.Embed(title = "Page2")
        from categories.templates.menu import Menu
        menu = Menu(embed1,'⏹', '🔼')
        menu.add_page('1️⃣', embed2)
        menu.add_page('2️⃣', embed3)

        await menu.event(self.bot, ctx.channel)
    
    @commands.command(hidden = True)
    async def testTime(self, ctx):
        import datetime
        import pytz.tzinfo
        embed1 = discord.Embed(title = "Time")
        embed1.add_field(name = "timestamp", value = "embed1.timestamp")
        await ctx.send(embed = embed1)
        time = ctx.message.created_at
        time2 = time.astimezone()
        print(time)
        print(type(time))
        print(time2)
        print(time2.tzname())
        print(datetime.datetime.now())
        embed2 = discord.Embed(title = "Time2", timestamp = time2)
        embed2.add_field(name = "timestamp", value = embed2.timestamp)
        await ctx.send(embed = embed2)

    @commands.command(hidden = True)
    async def testTime2(self, ctx):
        import datetime
        embed = discord.Embed(title = "Hi")
        embed.timestamp = ctx.message.created_at
        await ctx.send(embed = embed)
def setup(bot):
    bot.add_cog(Experiment(bot))