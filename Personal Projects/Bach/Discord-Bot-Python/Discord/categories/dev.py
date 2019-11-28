import discord
from discord.ext import commands

# Commands for developers to test things and stuffs.


def is_dev(ctx):
    return ctx.author.id in [472832990012243969, 462726152377860109, 481934034130174010]
                            #MikeJollie#1067     Stranger.com#4843   MJ2#8267

class Dev(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(hidden = True)
    @commands.check(is_dev)
    async def update_mod(self, ctx, name):
        self.bot.reload_extension(name)
        await ctx.send("Reloaded extension " + name)
        print("Reloaded extension " + name)
    @update_mod.error
    async def update_mod_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send("This command is reserved for bot developers only!")
        elif isinstance(error, commands.ExtensionNotFound):
            await ctx.send("I cannot find this extension. Check your typo or the repo again.")



def setup(bot):
    bot.add_cog(Dev(bot))