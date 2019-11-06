import discord
from discord.ext import commands

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    @commands.has_permissions(kick_members = True)
    async def kick(self, ctx, member : discord.Member, reason = None):
        '''
        Kick a member.
        **Usage:** <prefix>**kick** <name/ID/nickname/mention> [reason]
        **Example 1:** {p}kick MikeJollie Dumb
        **Example 2:** {p}kick @MikeJollie Still dumb
        '''

        guild = ctx.author.guild
        victim_name = str(member)
        if reason == None:
            reason = "Not provided."

        await guild.kick(member)
        await ctx.send("**User** `%s` has been kicked from %s**" % (victim_name, guild.name))
        await ctx.send("**Reason:** `%s`." % reason)
    
    @commands.command()
    @commands.has_permissions(ban_members = True)
    async def ban(self, ctx, member : discord.Member, *, reason = None):
        '''
        Ban a member.
        **Usage:** <prefix>**ban** <name/ID/nickname/mention> [reason]
        **Example 1:** ban MikeJollie Spam too much
        **Example 2:** ban @MikeJollie Stop spamming!
        '''

        guild = ctx.author.guild
        victim_name = str(member)
        if reason == None:
            reason = "Not provided."
            
        await guild.ban(member)
        await ctx.send("**User `%s` has been banned from %s**" % (victim_name, guild.name))
        await ctx.send("**Reason:** `%s`." % reason)
    

    
def setup(bot):
    bot.add_cog(Moderation(bot))