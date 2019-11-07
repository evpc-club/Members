import discord
from discord.ext import commands

class UserProfile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def profile(self, ctx, user: discord.Member = None):
        '''
        Information about yourself or another member.
        **Usage:** <prefix>**profile** [name/ID/nickname/mention]
        **Example 1:** {0}profile MikeJollie
        **Example 2:** {0}profile
        '''

        if user == None:
            member = ctx.author
        else:
            member = user
        embed = discord.Embed(description = "Test")

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

def setup(bot):
    bot.add_cog(UserProfile(bot))