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

bot = commands.Bot(command_prefix = prefix)

@bot.event
async def on_ready():
    print("Logged in as")
    print(bot.user.name)
    print(bot.user.id)
    print("------------")
    await bot.change_presence(status = discord.Status.idle, activity = discord.Game(" with nuclear bomb"))

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
