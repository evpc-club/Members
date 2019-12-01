import discord
from discord.ext import commands

class Logging(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.log_channel = 642235200188841996
        self.emoji = '📝'

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        pass

    @commands.Cog.listener()
    async def on_bulk_message_delete(self, messages):
        pass

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if after.author.bot == False:
            log_channel = self.bot.get_channel(self.log_channel)
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

        async for entry in guild.audit_logs(action = discord.AuditLogAction.ban, limit = 1):        
            if entry.reason == None:
                reason = "Not provided."
            else:
                reason = entry.reason
            
            embed = discord.Embed(title = "User banned", color = discord.Color.green())
            embed.add_field(name = "Name", value = str(user), inline = False)
            embed.add_field(name = "Reason", value = reason)
            await log_channel.send(embed = embed)

    @commands.Cog.listener()
    async def on_member_unban(self, guild, user):
        log_channel = self.bot.get_channel(self.log_channel)

        async for entry in guild.audit_logs(action = discord.AuditLogAction.unban, limit = 1):
            if entry.reason == None:
                reason = "Not provided."
            else:
                reason = entry.reason

            embed = discord.Embed(color = discord.Color.green())
            embed.add_field(name = "User unbanned", value = str(user), inline = False)
            embed.add_field(name = "Reason", value = reason)
            await log_channel.send(embed = embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        guild = member.guild
        log_channel = self.bot.get_channel(self.log_channel)

        async for entry in guild.audit_logs(limit = 1):
            if entry.target.id == member.id and entry.action == discord.AuditLogAction.kick:
                if entry.reason == None:
                    reason = "Not provided."
                else:
                    reason = entry.reason

                embed = discord.Embed(color = discord.Color.green())
                embed.add_field(name = "User kicked", value = str(member), inline = False)
                embed.add_field(name = "Reason", value = reason)
                await log_channel.send(embed = embed)
                
        embed = discord.Embed(color = discord.Color.green())
        embed.add_field(name = "User left", value = str(member), inline = False)
        await log_channel.send(embed = embed)

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        pass

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        pass
    
    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        pass

    @commands.Cog.listener()
    async def on_guild_channel_update(self, before, after):
        pass

    @commands.Cog.listener()
    async def on_guild_update(self, before, after):
        pass

    @commands.Cog.listener()
    async def on_guild_role_create(self, role):
        pass

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):
        pass

def setup(bot):
    bot.add_cog(Logging(bot))