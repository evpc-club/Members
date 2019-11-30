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
    @commands.cooldown(1, 5.0, commands.BucketType.default)
    async def update_mod(self, ctx, name):
        '''
        Reload a module.
        Useful when you don't want to disconnect the bot but still update your change.
        **Usage:** <prefix>**update_mod** <extension name>
        **Cooldown:** 5 seconds (global cooldown)
        **Example:** {0}update_mod categories.templates.navigate

        You need: dev status.
        I need: send_messages.
        '''
        self.bot.reload_extension(name)
        await ctx.send("Reloaded extension " + name)
        print("Reloaded extension " + name)
    @update_mod.error
    async def update_mod_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send("This command is reserved for bot developers only!")
        elif isinstance(error, commands.ExtensionNotFound):
            await ctx.send("I cannot find this extension. Check your typo or the repo again.")
    
    @commands.command(hidden = True)
    @commands.check(is_dev)
    async def reset_all_cooldown(self, ctx):
        '''
        Self-explanatory.
        **Usage:** <prefix>**reset_all_cooldown**
        **Example:** {0}reset_all_cooldown

        You need: dev status.
        I need: send_messages.
        '''
        for command in self.bot.commands:
            if command.is_on_cooldown(ctx):
                command.reset_cooldown(ctx)
        await ctx.send("All cooldown reseted.")



def setup(bot):
    bot.add_cog(Dev(bot))