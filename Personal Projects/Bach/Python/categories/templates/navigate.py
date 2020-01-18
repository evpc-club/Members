import discord
import asyncio

# A class that support navigating pages of embeds.

class Pages:
    def __init__(self, init_page = 0):
        '''
        Param:
        - `init_page`: the starting page. Default is `0`.
        '''
        self.__page_list__ = []
        self.__current_page__ = init_page
        self.__emoji_list__ = ['⏮️', '◀️', '▶️', '⏭️', '⏹️']
    
    def add_page(self, page):
        if isinstance(page, discord.Embed):
            self.__page_list__.append(page)
        else:
            raise TypeError("'page' must be discord.Embed.")
    
    async def event(self, bot, channel, interupt = True, author = None):
        '''
        This function is a coroutine.

        A function use to interact with the paginator.

        Param:
        - `bot`: a `commands.Bot` instance or a `discord.Client` instance.
        - `channel`: the channel you want to send the paginator in.
        - `interupt`: `False` if you don't want other user to react the paginator, `True` otherwise. Default value is `True`.
        - `author`: the user you want to be the only one to interact the paginator. If `interupt` is set to `True`,
        it'll raise exception if this is set.
        
        Exception:
        - AttributeError: This exception is raised when either `bot` and/or `channel` is wrong type.
        - RuntimeError: This exception is raised when `interupt` is `False` and `author` is `None`, or `interupt` is `True`
        and `author` is not `None`.
        '''
        if len(self.__page_list__) == 0:
            return
        if (interupt and author is not None) or (interupt == False and author is None):
            raise RuntimeError("`interupt` and `author` raised error. Please read the description of the function.")
        
        for num in range(0, len(self.__page_list__)):
            self.__page_list__[num].set_footer(text = "Page %d/%d" % (num + 1, len(self.__page_list__)))

        message = await channel.send(embed = self.__page_list__[self.__current_page__])
        for emoji in self.__emoji_list__:
            await message.add_reaction(emoji)

        def reaction_check(reaction, user):
            return reaction.message.id == message.id and user != message.author
        while True:
            try:
                reaction, user = await bot.wait_for("reaction_add", check = reaction_check, timeout = 120.0)
            except asyncio.TimeoutError:
                self.__current_page__ = -1
                await message.edit(content = ":clock12:", embed = None)
                await message.clear_reactions()
                return
            else:
                if interupt:
                    if reaction.emoji in self.__emoji_list__:
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
                else:
                    if user == author:
                        if reaction.emoji in self.__emoji_list__:
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