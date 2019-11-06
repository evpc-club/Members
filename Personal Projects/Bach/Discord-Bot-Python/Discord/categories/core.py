import discord
from discord.ext import commands

class Core(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def info(self, ctx):
        '''
        Information about the bot.
        **Usage:** <prefix>**info**
        **Example:** {p}info
        '''

        embed = discord.Embed(title = self.bot.user.name, description = "A utility bot.", color = discord.Color.green())

        embed.add_field(name = "Team:", value = "**Owner**: Stranger.com#4843\n**Developer**: MikeJollie#1067", inline = False)
        embed.add_field(name = "Bot info:", value = "**Language**: Python", inline = False)
        embed.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url)

        await ctx.send(embed = embed)
    
    @commands.command()
    async def help(self, ctx, subhelp : str = None):
        '''
        Show you how to use commands for this bot.
        Use **help** [category/command] if you need help for a specific category or command.
        **Usage:** <prefix>**help** [category/command]
        **Example 1:** {p}help
        **Example 2:** {p}help info
        **Example 3:** {p}help Core
        '''

        content = discord.Embed(color = discord.Color.green())
        note = '''
        In the help doc, <argument> is required, [argument] is optional and {p} represent the prefix of the bot.
        If an argument has space(s) in it, use "argument" to make the bot count as one argument.'''
        content.add_field(name = "Note:", value = note)

        if subhelp == None: # Normal help command.
            cog = self.bot.cogs # List of categories
            for category in cog:
                num_of_commands = 0
                context = ""
                commands = cog[category].get_commands() # List of commands in one category
                for command in commands:
                    context += "`" + command.name + "`" + ' ' # Highlight the commands
                    num_of_commands += 1
                embed_name = category + " (" + str(num_of_commands) + " commands): "
                content.add_field(name = embed_name, value = context, inline = False)
        else: # Category or command specified in help.
            cog = self.bot.get_cog(subhelp)
            command = self.bot.get_command(subhelp)

            if cog != None: # A category is mentioned.
                commands_in_cog = cog.get_commands()
                context = ""
                for command in commands_in_cog:
                    context += "`{}`: {}\n\n".format(command.name, command.brief)

                content.add_field(name = cog.qualified_name, value = context)
            elif command != None: # A command is mentioned.
                content.add_field(name = command.name, value = command.help)
            else:
                content.add_field(name = "Error:", value = "Category or command not found.")

        await ctx.send(embed = content)
    
    @commands.command()
    async def prefix(self, ctx, pref : str = None):
        '''
        View and set the prefix for the bot.
        **Usage:** <prefix>**prefix** [new prefix]
        **Example 1:** {p}prefix
        **Example 2:** {p}prefix %
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