import discord
from discord.ext import commands

import traceback
import sys
import json

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        guild_list = self.bot.guilds
        #guild_info = Record("./data/guild.db")
        for guild in guild_list:
            # guild configuration
            try:
                file_name = str(guild.id) + ".json"
                fin = open("./data/" + file_name, 'r')
            except FileNotFoundError as fnfe:
                fout = open("./data/" + file_name, 'w+')
                default_config = {
                    "ERROR": 0,
                    "GUILD_ID": guild.id,
                    "STATUS_LOG": 0,
                    "LOG_CHANNEL": 0,
                    "STATUS_WELCOME": 0,
                    "WELCOME_CHANNEL": 0,
                    "WELCOME_TEXT": "",
                    "STATUS_FILTER": 0,
                    "FILTER_WORDS": []
                }
                json.dump(default_config, fout, indent = 4)
                print("File %s created." % file_name)
                fout.close()

            # guild data
            #guild_info.create_table(str(guild.id))
            #for member in guild.members:
            #    guild_info.create_row(member_id = member.id, description = "", money = 0, warns = 0)
        

        

        print("Logged in as")
        print(self.bot.user.name)
        print(self.bot.user.id)
        print("------------")
        await self.bot.change_presence(
            status = discord.Status.idle, 
            activity = discord.Game(" with Discord API")
        )

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
            
        elif isinstance(message.channel, discord.DMChannel):
            RESPONSE_LIST = [
                    "I only talk in server, sorry.",
                    "Sorry mate, I really hate responding to DM.",
                    "Hey my developer hasn't allowed me to say in DM.",
                    "You may go to your server and use one of my commands.",
                    "So many people try to DM bots, but they always fail.",
                    "Bot is my name, DM is not my game.",
                    "Stop raiding my DM.",
                    "Sorry, can't respond your message here :(",
                    "It is really impossible to expect from a bot to respond to someone's DM.",
                    "I can't talk in DM, ask this guy -> <@472832990012243969>"
            ]
            dm_chan = message.author.dm_channel
            
            import random
            random_response = random.randint(0, len(RESPONSE_LIST) - 1)
            await dm_chan.send(RESPONSE_LIST[random_response])
        
        #await self.bot.process_commands(message) # uncomment this if this event is outside of a cog.

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        try:
            if isinstance(error, commands.CommandError):
                print("%s raised an error!" % ctx.command.name)
        except AttributeError: # If command not found, wrong syntax, etc.
            pass

        if isinstance(error, commands.CommandNotFound):
            async with ctx.typing(): # This will make the bot type for 10 seconds.
                n = 0
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send("You are missing the following permission(s) to execute this command: " + str(error.missing_perms))
        elif isinstance(error, commands.BotMissingPermissions):
            await ctx.send("I'm missing the following permission(s) to execute this command: " + str(error.missing_perms))
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Missing arguments. Please use `%shelp %s` for more information." % (ctx.prefix, ctx.command))
        elif isinstance(error, commands.TooManyArguments):
            await ctx.send("Too many arguments. Please use `%shelp %s` for more information." % (ctx.prefix, ctx.command))
        elif isinstance(error, commands.BadArgument):
            if ctx.command.name == "kick" or ctx.command.name == "ban":
                return
        elif isinstance(error, commands.DisabledCommand):
            await ctx.send("Sorry, but this command is disabled for now, it'll be back soon :thumbsup:")
        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.send("Hey there slow down! %0.2f seconds left!" % error.retry_after)
        else:
            error_text = "This command raised the following exception. Please copy and report it to the developer using `report`. Thank you and sorry for this inconvenience."
            error_text += "```%s```" % error
            await ctx.send(error_text)
            print('Ignoring exception in command {}:'.format(ctx.command), file = sys.stderr)
            traceback.print_exception(type(error), error, error.__traceback__, file = sys.stderr)

    @commands.Cog.listener()
    async def on_command_completion(self, ctx):
        if ctx.cog.qualified_name == "Dev":
            import datetime
            print("\n\n%s used %s at %s." % (str(ctx.author), ctx.command.name, str(datetime.datetime.today())), end = '\n\n')

def setup(bot):
    bot.add_cog(Events(bot))