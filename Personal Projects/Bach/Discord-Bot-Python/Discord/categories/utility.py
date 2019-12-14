import discord
from discord.ext import commands
import asyncio

class Utility(commands.Cog, command_attrs = {"cooldown_after_parsing" : True}):
    '''Commands related to utilities and fun.'''
    def __init__(self, bot):
        self.bot = bot
        self.emoji = '😆'

    @commands.command()
    async def ping(self, ctx):
        '''
        Show the latency of the bot.
        **Usage:** <prefix>**{command_name}**
        **Example:** {prefix}{command_name}

        You need: None.
        I need: send_messages.
        '''

        latency = self.bot.latency

        await ctx.send(str(format((latency * 1000), '.2f')) + "ms")

    @commands.command()
    async def dice(self, ctx):
        '''
        Roll a dice for you.
        **Usage:** <prefix>**{command_name}**
        **Example:** {prefix}{command_name}

        You need: None.
        I need: send_messages.
        '''
        import random
        await ctx.send("It's %d :game_die:" % (random.randint(1, 6)))

    @commands.command(enabled = False)
    async def poll(self, ctx, title, *choices):
        '''
        Make a poll for you.
        Note: the number of options must greater than 1.
        **Usage:** <prefix>**{command_name}** <title> <choice 1 / choice 2 / choice n>
        **Example:** {prefix}{command_name} "What's the most awesome bot in Discord?" MichaelBotPy MikeJollie
        '''
        await ctx.send("Randomly")

    @commands.command()
    async def say(self, ctx, *, content: str):
        '''
        Repeat what you say.
        **Usage:** <prefix>**{command_name}** <message (can contain spaces)>
        **Example:** {prefix}{command_name} MikeJollie is gay.

        You need: None.
        I need: send_messages.
        '''
        await ctx.message.delete()
        await ctx.send(content)

    @commands.command()
    async def speak(self, ctx, *, content: str):
        '''
        Make the bot speak!
        **Usage:** <prefix>**{command_name}** <message (can contain spaces)>
        **Example:** {prefix}{command_name} MikeJollie is gay

        You need: None.
        I need: send_tts_messages.
        '''
        await ctx.message.delete()
        await ctx.send(content, tts = True)

    @commands.command(enabled = True)
    async def calc(self, ctx, *, content: str):
        '''
        A mini calculator that calculate almost everything.
        Note: This command is still in testing. Trignometry functions return radian.
        **Usage:** <prefix>**{command_name}** <expression>
        **Example 1:** {prefix}{command_name} 1+2
        **Example 2:** {prefix}{command_name} 5*(2 + 3)
        **Example 3:** {prefix}{command_name} sqrt(25)

        You need: None.
        I need: send_messages.
        '''

        from categories.utilityfun.calc import calculate
        result = calculate(content)
        embed = discord.Embed(color = discord.Color.green())
        embed.add_field(name = "**Result:**", value = result)
        await ctx.send(embed = embed)

    @commands.command(cooldown_after_parsing = True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    async def embed(self, ctx, title : str = "", content : str = '', color : str = "", destination : str = ""):
        '''
        Send an embed message.
        Note: You'll respond to 3 questions to set the embed you want.
        **Usage:** <prefix>**{command_name}**
        **Cooldown:** 5 seconds (user cooldown).
        **Example:** {prefix}{command_name}

        You need: None.
        I need: read_message_history, manage_messages, send_messages.
        '''

        await ctx.message.delete()

        def check(message):
            return message.content != "" and message.content != "Pass"
        
        async def clean(prompt):
            input_list = await ctx.channel.history(limit = 3).flatten()

            for message in input_list:
                if message.id != prompt.id and message.author == ctx.message.author:
                    await message.delete()
                elif message.id == prompt.id:
                    await message.delete()
                    break


        title = ""
        content = ""
        color = discord.Color.default()

        prompt = await ctx.send("What's your title?")

        try:
            msg1 = await self.bot.wait_for("message", timeout = 60.0, check = check)
        except asyncio.TimeoutError:
            await ctx.send("Process ended due to overtime.")
        else:
            title = "**" + msg1.content + "**"

            await clean(prompt)

            prompt = await ctx.send("What's your content?")

            try:
                msg2 = await self.bot.wait_for("message", timeout = 60.0, check = check)
            except asyncio.TimeoutError:
                await ctx.send("Process ended due to overtime.")
            else:
                content = msg2.content

                await clean(prompt)

                prompt = await ctx.send("What color do you want? Supported colors: green, default (Discord's default color), red, orange, blue.")

                try:
                    msg3 = await self.bot.wait_for("message", timeout = 60.0, check = check)
                except asyncio.TimeoutError:
                    pass
                else:
                    if msg3.content.upper() == 'RED':
                        color = discord.Color.red()
                    elif msg3.content.upper() == 'GREEN':
                        color = discord.Color.green()
                    elif msg3.content.upper() == 'BLUE':
                        color = discord.Color.blue()
                    elif msg3.content.upper() == 'ORANGE':
                        color = discord.Color.orange()

                    await clean(prompt)
                

                embed = discord.Embed(title = title, description = content, color = color)

                await ctx.send(embed = embed)

    @commands.command(cooldown_after_parsing = True)
    @commands.cooldown(5, 10.0, commands.BucketType.user)
    async def howgay(self, ctx, *, target: str):
        '''
        An ultimate measurement of gayness.
        **Usage:** <prefix>**{command_name}** <anything you want to measure>
        **Cooldown:** 10 seconds after 5 uses (user cooldown).
        **Example 1:** {prefix}{command_name} MikeJollie
        **Example 2:** {prefix}{command_name} "iPhone 11"

        You need: None.
        I need: send_messages.
        '''
        
        import random
        percent_gay = random.randint(0, 100)
        await ctx.send(target + " is `" + str(percent_gay) + "%` gay.")

    @commands.command(cooldown_after_parsing = True)
    @commands.cooldown(5, 10.0, commands.BucketType.user)
    async def how(self, ctx, measure_unit : str, *, target : str):
        '''
        An ultimate measurement to measure everything except gayness.
        **Usage:** <prefix>**{command_name}** <something to use to rate> <something to rate>
        **Cooldown:** 10 seconds after 5 uses (user cooldown).
        **Example 1:** {prefix}{command_name} smart Stranger.com
        **Example 2:** {prefix}{command_name} "stupidly dumb" "Nightmare monsters"

        You need: None.
        I need: send_messages.
        '''

        import random
        percent_thing = random.randint(0, 100)
        await ctx.send(target + " is `" + str(percent_thing) + "%` " + measure_unit + ".")

    @commands.command(hidden = True, cooldown_after_parsing = True)
    @commands.cooldown(1, 120.0, commands.BucketType.user)
    async def send(self, ctx, id : int, *, msg : str):
        '''
        Send a message to either a channel or a user that the bot can see.
        **Usage:** <prefix>**{command_name}** <user ID / channel ID> <content>
        **Cooldown:** 120 seconds (user cooldown)
        **Example 1:** {prefix}{command_name} 577663051722129427 Gay.
        **Example 2:** {prefix}{command_name} 400983101507108876 All of you are gay.

        You need: None.
        I need: send_messages at <destination>.
        '''
        target = self.bot.get_user(id)
        if target == None:
            target = self.bot.get_channel(id)
            if target == None:
                await ctx.send("Destination not found.")
                return
        try:
            await target.send(msg)
        except AttributeError:
            await ctx.send("I cannot send message to myself dummy.")
        except discord.Forbidden:
            await ctx.send("It seems like I cannot send message to this place!")
        else:
            await ctx.send("Message sent!")

def setup(bot):
    bot.add_cog(Utility(bot))