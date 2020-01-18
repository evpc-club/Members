import discord
import asyncio

class Menu:
    def __init__(self, init_page, terminate_emoji, return_emoji):
        '''
        Param:
        - `init_page`: The center page.
        - `terminate_emoji`: The stop emoji.
        - `return_emoji`: The return emoji.
        Exception:
        - TypeError: This exception is raised when `init_page` is not a `discord.Embed`.
        '''
        self.__pages__ = {} # A dict with the format {emoji: discord.Embed}
        self.__terminator__ = terminate_emoji
        self.__return__ = return_emoji

        if isinstance(init_page, discord.Embed):
            self.__init_page__ = init_page
        else:
            raise TypeError("'init_page' must be discord.Embed.")
    
    def add_page(self, emoji, page):
        '''
        Add page to the menu.\n
        Param:
        - `emoji`: the emoji you want the page to be reacted.
        - `page`: the page you want to add. It must be a `discord.Embed`.

        Exception:
        - IndexError: This exception is raised when `emoji` is the same as `terminate_emoji` in the constructor.
        - TypeError: This exception is raised when `page` is not a `discord.Embed`.
        '''
        if isinstance(page, discord.Embed):
            if emoji != self.__terminator__:
                self.__pages__[emoji] = page
            else:
                raise IndexError("Cannot add page with %s emoji." % emoji)
        else:
            raise TypeError("'page' must be discord.Embed.")

    async def event(self, bot, channel, interupt = True, author = None):
        '''
        This function is a coroutine.

        A function use to interact with the menu.

        Param:
        - `bot`: a `commands.Bot` instance or a `discord.Client` instance.
        - `channel`: the channel you want to send the menu in.
        - `interupt`: `False` if you don't want other user to react the menu, `True` otherwise. Default value is `True`.
        - `author`: the user you want to be the only one to interact the menu. If `interupt` is set to `True`,
        it'll raise exception if this is set.
        
        Exception:
        - AttributeError: This exception is raised when either `bot` and/or `channel` is wrong type.
        - RuntimeError: This exception is raised when `interupt` is `False` and `author` is `None`, or `interupt` is `True`
        and `author` is not `None`.
        '''
        if len(self.__pages__) == 0:
            return
        if (interupt and author is not None) or (interupt == False and author is None):
            raise RuntimeError("`interupt` and `author` raised error. Please read the description of the function.")
        
        self.__pages__[self.__terminator__] = None

        message = await channel.send(embed = self.__init_page__)
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
                if interupt == False:
                    if user == author:
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
                    else:
                        await message.remove_reaction(reaction, user)
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