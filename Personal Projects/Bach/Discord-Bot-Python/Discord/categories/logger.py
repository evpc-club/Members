import discord
from discord.ext import commands

class Logging(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.log_channel = 642235200188841996

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if after.author.bot == False:
            log_channel = self.bot.get_channel(self.log_channel)
            print("Message edited: " + before.content + " now is " + after.content)
            embed = discord.Embed(color = discord.Color.green())
            message_edit_log = '''
                                Before: %s
                                After: %s
                                Author: %s''' % (before.content, after.content, after.author.name)
                                
            embed.add_field(name = "Message edited", value = message_edit_log)

            await log_channel.send(embed = embed)
    
    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        log_channel = self.bot.get_channel(self.log_channel)
        reason = "Not provided."

        ban_list = await guild.bans() # A tuple of (user, reason)
        for ban_case in ban_list:
            if ban_case.user == user:
                reason = ban_case.reason
        
        embed = discord.Embed(color = discord.Color.green())
        embed.add_field(name = "User banned", value = user.name, inline = False)
        embed.add_field(name = "Reason", value = reason)
        await log_channel.send(embed = embed)

    @commands.Cog.listener()
    async def on_member_unban(self, guild, user):
        log_channel = self.bot.get_channel(self.log_channel)
        async for entry in guild.audit_logs(action = discord.AuditLogAction.unban, limit = 1):
            embed = discord.Embed(color = discord.Color.green())
            embed.add_field(name = "User unbanned", value = user.name, inline = False)
            embed.add_field(name = "Reason", value = entry.reason)
            await log_channel.send(embed = embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        pass

def setup(bot):
    bot.add_cog(Logging(bot))