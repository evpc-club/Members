import discord

# A class that support navigating pages of embeds.

class Pages:
    def __init__(self, init_page = 0):
        self.__page_list__ = []
        self.__current_page__ = init_page
        self.__emoji_list__ = ['⏮️', '◀️', '▶️', '⏭️', '⏹️']
    
    def add_page(self, page):
        if isinstance(page, discord.Embed):
            self.__page_list__.append(page)
        else:
            raise TypeError("'page' must be discord.Embed.")
    
    async def event(self, bot, src):
        import asyncio
        message = await src.send(embed = self.__page_list__[self.__current_page__])
        for emoji in self.__emoji_list__:
            await message.add_reaction(emoji)
        
        def reaction_check(reaction, user):
            return reaction.emoji in self.__emoji_list__ and reaction.message.id == message.id and user != message.author
        while True:
            try:
                reaction, user = await bot.wait_for("reaction_add", check = reaction_check, timeout = 120.0)
            except asyncio.TimeoutError:
                self.__current_page__ = -1
                await message.edit(content = ":clock12:", embed = None)
                await message.clear_reactions()
                return
            else:
                if reaction.emoji == '⏮️':
                    self.__current_page__ = 0
                elif reaction.emoji == '◀️':
                    if self.__current_page__ != 0:
                        self.__current_page__ -= 1
                elif reaction.emoji == '▶️':
                    if self.__current_page__ < len(self.__page_list__) - 1:
                        self.__current_page__ += 1
                elif reaction.emoji == '⏭️':
                    self.__current_page__ = len(self.__page_list__) - 1
                elif reaction.emoji == '⏹️':
                    self.__current_page__ = -1
                    await message.edit(content = ":white_check_mark:", embed = None)
                    await message.clear_reactions()
                    return
                
                await message.edit(embed = self.__page_list__[self.__current_page__])
                await message.remove_reaction(reaction, user)