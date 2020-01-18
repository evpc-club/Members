import discord
from discord.ext import commands

import os
import traceback
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("token")
prefix = os.getenv("prefix")

bot = commands.Bot(command_prefix = commands.when_mentioned_or(prefix))

try:
    if __name__ == "__main__":
        for filename in sorted(os.listdir('./categories')):
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