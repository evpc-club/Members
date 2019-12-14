import discord
import asyncio

class Menu:
    def __init__(self, init_page, terminate_emoji, return_emoji):
        self.__pages__ = {} # A dict with the format {emoji: discord.Embed}
        self.__terminator__ = terminate_emoji
        self.__return__ = return_emoji

        if isinstance(init_page, discord.Embed):
            self.__init_page__ = init_page
        else:
            raise TypeError("'init_page' must be discord.Embed.")
    
    def add_page(self, emoji, page):
        if isinstance(page, discord.Embed):
            if emoji != self.__terminator__:
                self.__pages__[emoji] = page
            else:
                raise IndexError("Cannot add page with %s emoji." % emoji)
        else:
            raise TypeError("'page' must be discord.Embed.")
    
    async def event(self, bot, src):
        if len(self.__pages__) == 0:
            return
        
        self.__pages__[self.__terminator__] = None

        message = await src.send(embed = self.__init_page__)
        for emoji in self.__pages__:
            await message.add_reaction(emoji)
        
        available_options = [] # Available reactions that a user can react.
        for key in self.__pages__:
            available_options.append(key)

        def reaction_check(reaction, user):
            return reaction.message.id == message.id and user != message.author
        
        while True:
            try:
                reaction, user = await bot.wait_for("reaction_add", check = reaction_check, timeout = 120.0)
            except asyncio.TimeoutError:
                await message.edit(content = ":clock12:", embed = None)
                await message.clear_reactions()
                return
            else:
                if reaction.emoji in available_options:
                    if reaction.emoji == self.__terminator__:
                        await message.edit(content = ":white_check_mark:", embed = None)
                        await message.clear_reactions()
                        return
                    elif reaction.emoji == self.__return__:
                        await message.edit(embed = self.__init_page__)

                        available_options = []
                        for key in self.__pages__:
                            available_options.append(key)
                    else:
                        available_options = []
                        available_options = self.__return__

                    
                        await message.edit(embed = self.__pages__[reaction.emoji])
                    await message.clear_reactions()
                    for emoji in available_options:
                        await message.add_reaction(emoji)
                else:
                    await message.remove_reaction(reaction, user)