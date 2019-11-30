import discord
from discord.ext import commands

class Moderation(commands.Cog):
    '''Commands related to moderate actions such as kick, ban, etc.'''
    def __init__(self, bot):
        self.bot = bot
        self.emoji = '2️⃣'
    
    @commands.command()
    @commands.has_permissions(kick_members = True)
    @commands.bot_has_permissions(kick_members = True)
    @commands.cooldown(2, 5.0, commands.BucketType.guild)
    async def kick(self, ctx, member : discord.Member, reason = None):
        '''
        Kick a member.
        **Usage:** <prefix>**kick** <name/ID/nickname/mention> [reason]
        **Cooldown:** 5 seconds after 2 uses (guild cooldown).
        **Example 1:** {0}kick MikeJollie Dumb
        **Example 2:** {0}kick @MikeJollie Still dumb
        **Example 3:** {0}kick 472832990012243969

        You need: kick_members.
        I need: kick_members, send_messages.
        '''

        guild = ctx.author.guild
        victim_name = str(member)
        if reason == None:
            reason = "Not provided."

        try:
            await guild.kick(member, reason = reason)
        except discord.Forbidden as f:
            await ctx.send("I cannot kick someone that's higher than me!")
        else:
            await ctx.send("**User** `%s` has been kicked from %s**" % (victim_name, guild.name))
            await ctx.send("**Reason:** `%s`" % reason)
    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send("I cannot kick someone that's not in the guild! If you want someone not to join your guild, use `%shackban`." % ctx.prefix)

    @commands.command()
    @commands.has_permissions(ban_members = True)
    @commands.bot_has_permissions(ban_members = True)
    @commands.cooldown(2, 5.0, commands.BucketType.guild)
    async def ban(self, ctx, user : discord.Member, *, reason = None):
        '''
        Ban a member __in__ the server.
        **Usage:** <prefix>**ban** <name/ID/nickname/mention> [reason]
        **Cooldown:** 5 seconds after 2 uses (guild cooldown).
        **Example 1:** {0}ban MikeJollie Spam too much
        **Example 2:** {0}ban @MikeJollie Stop spamming!
        
        You need: ban_members.
        I need: ban_members, send_messages.
        '''

        guild = ctx.author.guild
        victim_name = str(user)
        if reason == None:
            reason = "Not provided."
        try:
            await guild.ban(user, reason = reason)
        except discord.Forbidden as f:
            await ctx.send("I cannot ban someone that's higher than me!")
        else:
            await ctx.send("**User `%s` has been banned from %s**" % (victim_name, guild.name))
            await ctx.send("**Reason:** `%s`" % reason)
    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send("I cannot ban someone that's not in the guild normally. I need the power of `%shackban` to ban." % ctx.prefix)
    
    @commands.command()
    @commands.has_permissions(ban_members = True)
    @commands.bot_has_permissions(ban_members = True)
    @commands.cooldown(2, 5.0, commands.BucketType.guild)
    async def hackban(self, ctx, id : int, *, reason = None):
        '''
        Ban a user __outside__ the server.
        **Usage:** <prefix>**hackban** <ID> [reason]
        **Cooldown:** 5 seconds after 2 uses (guild cooldown).
        **Example:** {0}hackban 472832990012243969 Develope a bot

        You need: ban_members.
        I need: ban_members, send_messages.
        '''
        guild = ctx.author.guild
        await guild.ban(discord.Object(id = id), reason = reason)
        await ctx.send("**User `%s` has been banned from %s**" % (str(id), guild))
        await ctx.send("**Reason:** `%s`" % reason)
    
    @commands.command()
    @commands.has_permissions(ban_members = True)
    @commands.bot_has_permissions(ban_members = True)
    @commands.cooldown(2, 5.0, commands.BucketType.guild)
    async def unban(self, ctx, id : int, *, reason = None):
        '''
        Unban a user.
        **Usage:** <prefix>**unban** <ID> [reason]
        **Cooldown:** 5 seconds after 2 uses (guild cooldown).
        **Example:** {0}unban 472832990012243969 You've redeemed your goodness.

        You need: ban_members.
        I need: ban_members, send_messages.
        '''
        guild = ctx.author.guild
        await guild.unban(discord.Object(id = id), reason = reason)
        await ctx.send("**User `%s` has been unbanned from %s**" % (str(id), guild))
        await ctx.send("**Reason:** `%s`" % reason)

def setup(bot):
    bot.add_cog(Moderation(bot))