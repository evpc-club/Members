import discord
from discord.ext import commands

class Core(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        from categories.templates.help import BigHelp
        self.bot.help_command = BigHelp()
        self.bot.help_command.cog = self
    

    @commands.command()
    async def info(self, ctx):
        '''
        Information about the bot.
        **Usage: <prefix>info**
        **Cooldown:** None.
        **Example:** {0}info

        You need: None.
        I need: send_messages.
        '''
        embed = discord.Embed(title = self.bot.user.name, description = "A utility bot.", color = discord.Color.green())

        embed.add_field(name = "Team:", value = "**Owner**: Stranger.com#4843\n**Developer**: MikeJollie#1067", inline = False)
        embed.add_field(name = "Bot info:", value = "**Language**: Python", inline = False)
        embed.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url)
        embed.set_thumbnail(url = self.bot.user.avatar_url)

        await ctx.send(embed = embed)

    @commands.command()
    async def profile(self, ctx, user: discord.Member = None):
        '''
        Information about yourself or another __member__.
        **Usage:** <prefix>**profile** [name/ID/nickname/mention]
        **Example 1:** {0}profile MikeJollie
        **Example 2:** {0}profile

        You need: None.
        I need: send_messages.
        '''

        if user == None:
            member = ctx.author
        else:
            member = user
        embed = discord.Embed()

        embed.set_author(name = member.name, icon_url = member.avatar_url)

        embed.add_field(name = "Username:", value = member.name)
        embed.add_field(name = "Nickname:", value = member.nick)
        embed.add_field(name = "Avatar URL:", value = "[Click here](%s)" % member.avatar_url)

        embed.set_thumbnail(url = member.avatar_url)

        roleList = member.roles
        roles = ""
        for index in range(len(roleList) - 1, 0, -1): # The roles are ordered from bottom to top, so roleList[0] is @everyone.
            roles = roles + "<@&%s>" % str(roleList[index].id)
            if index > 1:
                roles += "- "
        embed.add_field(name = "Roles:", value = roles)

        await ctx.send(embed = embed)

    @commands.command()
    async def serverinfo(self, ctx):
        '''
        Information about the server that invoke this command.
        **Usage:** <prefix>**serverinfo**
        **Example:** {0}serverinfo

        You need: None.
        I need: send_messages.
        '''
        guild = ctx.guild
        embed = discord.Embed(description = "Information about this server.", color = discord.Color.green())
        embed.set_thumbnail(url = guild.icon_url)
        embed.add_field(name = "Name", value = guild.name)
        embed.add_field(name = "Created at (dd/mm/yyyy)", value = "%s/%s/%s" % (str(guild.created_at.day), str(guild.created_at.month), str(guild.created_at.year)))
        embed.add_field(name = "Owner", value = str(guild.owner))
        embed.add_field(name = "Roles", value = str(len(guild.roles)) + " roles.")
        embed.add_field(name = "Channels", value = "Text channels: %d\nVoice channels: %d" % (len(guild.text_channels), len(guild.voice_channels)))
        
        online = 0
        bot = 0
        guild_size = 0
        for member in guild.members:
            if member.status != discord.Status.offline:
                online += 1
            if member.bot:
                bot += 1
            guild_size += 1
        
        member_text = "%d members\n%d online\n%d bots, %d humans." % (guild_size, online, bot, guild_size - bot)

        embed.add_field(name = "Members", value = member_text)
        embed.set_footer(text = "Server ID: %s" % str(guild.id))

        await ctx.send(embed = embed)

    @commands.command(enabled = False)
    @commands.has_permissions(manage_guild = True)
    @commands.cooldown(1, 5.0, commands.BucketType.default)
    async def prefix(self, ctx, pref : str = None):
        '''
        View and set the prefix for the bot.
        **Usage:** <prefix>**prefix** [new prefix]
        **Cooldown:** 5 seconds (global cooldown).
        **Example 1:** {0}prefix
        **Example 2:** {0}prefix %
        
        You need: manage_guild.
        I need: send_messages.
        '''

        if pref == None:
            await ctx.send("Current prefix: " + ctx.prefix)
        else:
            self.bot.command_prefix = pref
            await ctx.send("New prefix: " + self.bot.command_prefix)
            # Save the prefix
            fout = open("./setup/prefix.txt", 'w')
            fout.write(self.bot.command_prefix)
            fout.close()

    @commands.command()
    async def note(self, ctx):
        '''
        Provide syntax convention in {0}help.
        **Usage:** <prefix>**note**
        **Example:** {0}note

        You need: None.
        I need: send_messages.
        '''

        embed = discord.Embed(title = "Note:", description = "A help of a command usually consisted of these parts:", color = discord.Color.green())

        description_note = "+ Tells what does the command do."
        note_note = "+ Optional, usually it means the command has something special condition."
        usage_note = '''+ Shows you the syntax of the command.
                        + [argument] is optional argument, while <argument> is required.
                        + If one of your arguments has spaces, use "this argument". Ex: %skick "This is a user" Dumb.''' % ctx.prefix
        cooldown_note = '''+ Optional, tells you the command's interval.
                           + If it says (guild cooldown), it means the command is not available for the entire server in that interval.
                           + If it says (user cooldown), it means the command is not available for the user invoked in that interval.
                           + If it says (global cooldown), it means the command is not available for anywhere that use the bot.'''
        example_note = "+ Shows some examples to help you understand the syntax."
        yperm_note = "+ Shows you permissions you need to execute the command."
        mperm_note = "+ Shows you permissions the bot need to execute the command."

        embed.add_field(name = "**A description**", value = description_note, inline = False)
        embed.add_field(name = "**A note**", value = note_note, inline = False)
        embed.add_field(name = "**Usage**", value = usage_note, inline = False)
        embed.add_field(name = "**Cooldown**", value = cooldown_note, inline = False)
        embed.add_field(name = "**Examples**", value = example_note, inline = False)
        embed.add_field(name = "**Your required permissions**", value = yperm_note, inline = False)
        embed.add_field(name = "**My required permissions**", value = mperm_note, inline = False)

        await ctx.send(embed = embed)

    @commands.command()
    @commands.cooldown(1, 3.0, commands.BucketType.default)
    async def report(self, ctx, *, content : str):
        '''
        Report a bug or suggest a feature for the bot.
        Note: Provide constructive reports and suggestions are appreciated.
        **Usage:** <prefix>**report** <report/suggest> <content>
        **Cooldown:** 3 seconds (global cooldown).
        **Example 1:** {0}report report This command has a bug.
        **Example 2:** {0}report suggest This command should be improved.

        You need: None.
        I need: send_messages.
        '''
        report_chan = 644339079164723201
        channel = ctx.bot.get_channel(report_chan)

        flag = content.split()[0]
        if (flag == "report") or (flag == "suggest"):
            msg = ""
            for i in range(1, len(content.split())):
                msg += content.split()[i] + ' '
            embed = discord.Embed(title = flag.capitalize(), description = msg, color = discord.Color.green())
            embed.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url)
            embed.set_footer(text = "Sender ID: " + str(ctx.author.id))
            await channel.send(embed = embed)
            await ctx.send("Your opinion has been sent.")
        else:
            await ctx.send("Incorrect argument. First argument should be either `suggest` or `report`.")

    @commands.command()
    async def changelog(self, ctx):
        '''
        Show the latest 10 changes of the bot.
        **Usage:** <prefix>**changelog**
        **Example:** {0}changelog

        You need: None.
        I need: send_messages.
        '''
        channel_id = 644393721512722432
        channel = self.bot.get_channel(channel_id)
        from categories.templates.navigate import Pages
        paginator = Pages(0)
        async for message in channel.history(limit = 10):
            embed = discord.Embed(description = message.content, color = discord.Color.green())
            paginator.add_page(embed)
        await paginator.event(self.bot, ctx.channel)

def setup(bot):
    bot.add_cog(Core(bot))