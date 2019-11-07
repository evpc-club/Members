import discord
from discord.ext import commands

class BigHelp(commands.HelpCommand):
    def __init__(self):
        docstring = '''Show help about the bot, a command, or a category
                       **Usage:** <prefix>**help** [command/category]
                       **Example 1:** {0}help
                       **Example 2:** {0}help info
                       **Example 3:** {0}help Core'''
        super().__init__(command_attrs={
            'help': docstring
        })
    async def send_bot_help(self, mapping):
        content = discord.Embed(color = discord.Color.green())
        note = '''
        In the help doc, <argument> is required, [argument] is optional.
        If an argument has space(s) in it, use "this argument" to make the bot count as one argument.'''
        content.add_field(name = "Note:", value = note)

        cog = self.context.bot.cogs # List of categories
        for category in cog:
            num_of_commands = 0
            context = ""
            commands = cog[category].get_commands() # List of commands in one category
            for command in commands:
                context += "`" + command.name + "`" + ' ' # Highlight the commands
                num_of_commands += 1
            embed_name = category + " (" + str(num_of_commands) + " commands): "
            content.add_field(name = embed_name, value = context, inline = False)

        await self.context.channel.send(embed = content)

    async def send_cog_help(self, cog):
        content = discord.Embed(color = discord.Color.green())
        display = ""
        command_list = cog.get_commands()
        for command in command_list:
            display += '`%s`: %s\n' % (command.name, command.short_doc)
        
        content.add_field(name = cog.qualified_name, value = display)

        await self.context.channel.send(embed = content)
    async def send_command_help(self, command):
        content = discord.Embed(color = discord.Color.green())
        content.add_field(name = command.name, value = command.help.format(self.context.prefix))    
        await self.context.send(embed = content)