# This application use the convenience of discord.ext.

import os
import traceback
import discord
from discord.ext import commands

fin = open("./setup/token.txt", 'r')
TOKEN = fin.read()
fin.close()
fin = open("./setup/prefix.txt", 'r')
prefix = fin.read()
fin.close()

bot = commands.Bot(command_prefix = commands.when_mentioned_or(prefix))

@bot.event
async def on_ready():
    print("Logged in as")
    print(bot.user.name)
    print(bot.user.id)
    print("------------")
    await bot.change_presence(status = discord.Status.online, activity = discord.Game(" with nuclear bomb"))

@bot.event
async def on_message(message):
    if isinstance(message.channel, discord.DMChannel):
        RESPONSE_LIST = ["I only talk in server, sorry.",
                        "Sorry mate, I really hate responding to DM.",
                        "Hey my developer hasn't allowed me to say in DM.",
                        "You may go to your server and use one of my commands.",
                        "So many people try to DM bots, but they always fail.",
                        "Bot is my name, DM is not my game.",
                        "Stop raiding my DM.",
                        "Sorry, can't respond your message here :(",
                        "It is really impossible to expect from a bot to respond to someone's DM.",
                        "I can't talk in DM, ask this guy -> <@472832990012243969>"]
        try:
            dm_chan = message.author.dm_channel
        except AttributeError as ae: # This raise AttributeError for no reason. message.author is supposed to be a User not ClientUser.
            pass
        
        import random
        random_response = random.randint(0, len(RESPONSE_LIST) - 1)
        await dm_chan.send(RESPONSE_LIST[random_response])
    

    await bot.process_commands(message)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You are missing the following permission(s) to execute this command: " + str(error.missing_perms))
    elif isinstance(error, commands.BotMissingPermissions):
        await ctx.send("I'm missing the following permission(s) to execute this command: " + str(error.missing_perms))
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Missing arguments. Please use " + bot.command_prefix + "help for more information.")
    elif isinstance(error, commands.TooManyArguments):
        await ctx.send("Too many arguments. Please use " + bot.command_prefix + "help for more information.")
    elif isinstance(error, commands.DisabledCommand):
        await ctx.send("Sorry, but this command is disabled for now, it'll be back soon :thumbsup:")
    else:
        await ctx.send(error)
        print(traceback.print_exc())
        print(error)
    
try:
    if __name__ == "__main__":
        for filename in os.listdir('./categories'):
            if filename.endswith('.py'):
                bot.load_extension(f'categories.{filename[:-3]}')
except commands.ExtensionNotFound as enf:
    print("Extension not found.")
    print(traceback.print_exc())
except commands.ExtensionFailed as ef:
    print("The extension or its setup function had an execution error.")
    print(traceback.print_exc())
except commands.NoEntryPointError as nep:
    print("No setup function.")
    print(traceback.print_exc())
except:
    print("Unknown error detected.")
    print(traceback.print_exc())
else:
    bot.run(TOKEN)