import discord
from discord.ext import commands

class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        '''
        Show the latency of the bot.
        **Usage:** <prefix>**ping**
        **Example:** {p}ping
        '''

        latency = self.bot.latency

        await ctx.send(str(format((latency * 1000), '.2f')) + "ms")

    @commands.command()
    async def say(self, ctx, *, content: str):
        '''
        Repeat what you say.
        **Usage:** <prefix>**say** <message (can contain spaces)>
        **Example:** {p}say MikeJollie is gay.
        '''

        await ctx.send(content)

    @commands.command()
    async def calc(self, ctx, *, content: str):
        '''
        A mini calculator that calculate almost everything.
        Note: This command is still in testing.
        **Usage:** <prefix>**calc** <expression>
        **Example 1:** {p}calc 1+2
        **Example 2:** {p}calc 5*(2 + 3)
        **Example 3:** {p}calc sqrt(25)
        '''

        from categories.utilityfun.calc import calculate
        result = calculate(content)
        embed = discord.Embed(color = discord.Color.green())
        embed.add_field(name = "Result:", value = result)
        await ctx.send(embed = embed)

    @commands.command()
    async def embed(self, ctx):
        '''
        Send an embed message. You'll respond to 3 questions to set the embed you want.
        Note: This command is incomplete and is full of errors. Use at your own desire.
        **Usage:** <prefix>**embed**
        **Example:** {p}embed
        '''

        import asyncio

        def check(message):
            return message.content != "" and message.content != "Pass"
        
        title = ""
        content = ""
        color = discord.Color.default()

        await ctx.send("What's your title?")

        try:
            msg1 = await self.bot.wait_for("message", timeout = 60.0, check = check)
        except asyncio.TimeoutError:
            await ctx.send("Process ended due to overtime.")
        else:
            title = msg1
            await ctx.send("What's your content?")

            try:
                msg2 = await self.bot.wait_for("message", timeout = 60.0, check = check)
            except asyncio.TimeoutError:
                await ctx.send("Process ended due to overtime.")
            else:
                content = msg2
                await ctx.send("What color do you want? Supported colors: green, default (Discord's default color), red, orange, blue.")

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
                
                embed = discord.Embed(color = color)
                embed.add_field(name = title, value = content)

                await ctx.send(embed = embed)

    @commands.command()
    async def howgay(self, ctx, *, target: str):
        '''
        An ultimate measurement of gayness.
        **Usage:** <prefix>**howgay** <anything you want to measure>
        **Example 1:** {p}howgay MikeJollie
        **Example 2:** {p}howgay "iPhone 11"
        '''
        
        import random
        percent_gay = random.randint(0, 100)
        await ctx.send(target + " is `" + str(percent_gay) + "%` gay.")

def setup(bot):
    bot.add_cog(Utility(bot))