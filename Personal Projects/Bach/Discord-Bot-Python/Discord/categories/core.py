import discord
from discord.ext import commands

class Core(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        from categories.helpcommand.help import BigHelp
        self.bot.help_command = BigHelp()
        self.bot.help_command.cog = self
    
    @commands.command()
    async def info(self, ctx):
        '''
        Information about the bot.
        **Usage:** <prefix>**info**
        **Example:** {0}info
        '''
        embed = discord.Embed(title = self.bot.user.name, description = "A utility bot.", color = discord.Color.green())

        embed.add_field(name = "Team:", value = "**Owner**: Stranger.com#4843\n**Developer**: MikeJollie#1067", inline = False)
        embed.add_field(name = "Bot info:", value = "**Language**: Python", inline = False)
        embed.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url)

        await ctx.send(embed = embed)

    @commands.command()
    async def prefix(self, ctx, pref : str = None):
        '''
        View and set the prefix for the bot.
        **Usage:** <prefix>**prefix** [new prefix]
        **Example 1:** {0}prefix
        **Example 2:** {0}prefix %
        '''

        if pref == None:
            await ctx.send("Current prefix: " + self.bot.command_prefix)
        else:
            self.bot.command_prefix = pref
            await ctx.send("New prefix: " + self.bot.command_prefix)
            # Save the prefix
            fout = open("./setup/prefix.txt", 'w')
            fout.write(self.bot.command_prefix)
            fout.close()

def setup(bot):
    bot.add_cog(Core(bot))