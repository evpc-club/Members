import discord
from discord.ext import commands

import gconfig

# Specification:
# Every single events here (except raw events) must have the following variables declared at the very first line of the event:
# - log_channel: the channel that's gonna send the embed. Retrieve using gconfig.get_config and config["LOG_CHANNEL"]
# - log_title: the log title that's gonna pass in title in discord.Embed
# - log_content: the log content that's gonna pass in description in discord.Embed
# - log_color: the color of the embed. It must be self.color_... depend on the current event.
# - log_time: the timestamp of the embed. Typically get from entry.created_at.
# - Optional(executor): the Member that triggered the event.


class Logging(commands.Cog):
    '''Commands related to logging actions in server.'''
    def __init__(self, bot):
        self.bot = bot
        self.log_channel = 649111117204815883
        self.emoji = '📝'
        # Moderation action = Black
        # Warn / Mute = Red
        # Change (server change, message change, member change, etc.) = Yellow
        # Delete (delete message, delete role, delete channel, etc.) = Orange
        # Create (create channel, create role, etc.) = Green
        # Join / Leave (server) = Blue
        # Other = Teal
        self.color_moderation = 0x000000
        self.color_warn_mute = discord.Color.red()
        self.color_change = discord.Color.gold()
        self.color_delete = discord.Color.orange()
        self.color_create = discord.Color.green()
        self.color_guild_join_leave = discord.Color.blue()
        self.color_other = discord.Color.teal()

    def log_check(self, guild):
        config = gconfig.get_config(guild.id)
        if config["ERROR"] == 0 and config["STATUS_LOG"] == 1 and config["LOG_CHANNEL"] != 0:
            return True
        elif config["ERROR"] != 0:
            print("File not found.")
            return False
        elif config["STATUS_LOG"] == 0:
            print("Logging not enabled.")
            return False
        else:
            print("Log channel not set.")
            return False

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        guild = message.guild
        if self.log_check(guild):
            config = gconfig.get_config(guild.id)
            log_channel = self.bot.get_channel(config["LOG_CHANNEL"])

            log_title = "Message Deleted"
            log_content = ""
            log_color = self.color_delete
            log_time = None
            deletor = None

            async for entry in message.guild.audit_logs(action = discord.AuditLogAction.message_delete, limit = 1):
                from datetime import datetime
                log_time = datetime.utcnow() # Audit log doesn't log message that the author delete himself.
                deletor = entry.user.id
                log_content = '''
                                Content: %s
                                Author: <@%d>
                                Deletor: <@%d>
                                ----------------------------
                                Channel: <#%s>
                                ''' % (message.content, message.author.id, deletor, message.channel.id)
                embed = discord.Embed(title = log_title, description = log_content, color = log_color, timestamp = log_time)
                embed.set_thumbnail(url = message.author.avatar_url)
                embed.set_author(name = message.author.name, icon_url = message.author.avatar_url)

                await log_channel.send(embed = embed)

    @commands.Cog.listener()
    async def on_bulk_message_delete(self, messages):
        pass

    @commands.Cog.listener()
    async def on_raw_message_edit(self, payload):
        if payload.cached_message != None: # on_message_edit
            return
        else:
            guild = self.bot.get_guild(self.bot.get_channel(payload.channel_id))
            if self.log_check(guild):
                config = gconfig.get_config(guild.id)
                log_channel = self.bot.get_channel(config["LOG_CHANNEL"])
                log_title = "Message Edited"
                log_content = '''
                                    :warning: The content of the message is not found.
                                    Message ID: %d
                                    Channel: <#%s>
                                    ''' % (payload.message_id, payload.channel_id)
                log_color = self.color_change

                embed = discord.Embed(title = log_title, description = log_content, color = log_color)
                await log_channel.send(embed = embed)
    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if after.author.bot == False:
            guild = before.guild
            if self.log_check(guild):
                config = gconfig.get_config(guild.id)
                log_channel = self.bot.get_channel(config["LOG_CHANNEL"])

                log_title = "Message Edited"
                log_content = '''
                                Before: %s
                                After: %s
                                Author: <@%d>
                                ----------------------------
                                Channel: <#%s>
                                ''' % (before.content, after.content, before.author.id, before.channel.id)
                log_color = self.color_change
                log_time = after.edited_at

                embed = discord.Embed(title = log_title, description = log_content, color = log_color, timestamp = log_time)
                                    
                embed.set_thumbnail(url = before.author.avatar_url)
                embed.set_author(name = before.author.name, icon_url = before.author.avatar_url)

                await log_channel.send(embed = embed)
    
    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        if self.log_check(guild):
            config = gconfig.get_config(guild.id)
            log_channel = self.bot.get_channel(config["LOG_CHANNEL"])

            log_title = "User Banned"
            log_content = ""
            log_color = self.color_moderation
            log_time = None

            reason = "Not provided."
            executor = None
            
            async for entry in guild.audit_logs(action = discord.AuditLogAction.ban, limit = 1):        
                if entry.reason == None:
                    reason = "Not provided."
                else:
                    reason = entry.reason
                executor = entry.user.id
                log_time = entry.created_at
                
                log_content = '''
                                User: <@%d>
                                User name: %s
                                Reason: %s
                                ----------------------------
                                Executor: <@%d>
                                '''  % (user.id, str(user), reason, executor)

                embed = discord.Embed(title = log_title, description = log_content, color = log_color, timestamp = log_time)

                await log_channel.send(embed = embed)

    @commands.Cog.listener()
    async def on_member_unban(self, guild, user):
        if self.log_check(guild):
            config = gconfig.get_config(guild.id)
            log_channel = self.bot.get_channel(config["LOG_CHANNEL"])

            log_title = "User Unbanned"
            log_content = ""
            log_color = self.color_moderation
            log_time = None

            reason = ""
            executor = None
            
            async for entry in guild.audit_logs(action = discord.AuditLogAction.nnban, limit = 1):        
                if entry.reason == None:
                    reason = "Not provided."
                else:
                    reason = entry.reason
                executor = entry.user.id
                log_time = entry.created_at
                
                log_content = '''
                                User: <@%d>
                                User name: %s
                                Reason: %s
                                ----------------------------
                                Executor: <@%d>
                                '''  % (user.id, str(user), reason, executor)
                
                embed = discord.Embed(title = log_title, description = log_content, color = log_color, timestamp = log_time)

                await log_channel.send(embed = embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        guild = member.guild
        if self.log_check(guild):
            config = gconfig.get_config(guild.id)
            log_channel = self.bot.get_channel(config["LOG_CHANNEL"])

            log_title = ""
            log_content = ""
            log_color = None
            log_time = None

            reason = "Not provided."
            executor = None
            
            async for entry in guild.audit_logs(limit = 1):
                if entry.target.id == member.id and entry.action == discord.AuditLogAction.kick:
                    if entry.reason == None:
                        reason = "Not provided."
                    else:
                        reason = entry.reason
                    executor = entry.user.id
                    log_time = entry.created_at

                    log_title = "Member Kicked"
                    log_content = '''
                                Member: <@%d>
                                Member name: %s
                                Reason: %s
                                ----------------------------
                                Executor: <@%d>
                                '''  % (member.id, str(member), reason, executor)
                    log_color = self.color_moderation
                    
                    embed = discord.Embed(title = log_title, description = log_content, color = log_color, timestamp = log_time)

                    await log_channel.send(embed = embed)
            
                log_title = "Member Left"
                log_content = '''
                                Member: <@%d>
                                Member name: %s
                                ----------------------------
                                Member ID: %d
                                ''' % (member.id, str(member), member.id)
                log_color = self.color_guild_join_leave
                from datetime import datetime
                log_time = datetime.utcnow() # entry.created_at is unreliable

                embed = discord.Embed(title = log_title, description = log_content, color = log_color, timestamp = log_time)
                embed.set_thumbnail(url = member.avatar_url)

                await log_channel.send(embed = embed)

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        guild = before.guild
        if self.log_check(guild):
            config = gconfig.get_config(guild.id)
            log_channel = self.bot.get_channel(config["LOG_CHANNEL"])

            log_title = ""
            log_content = ""
            log_color = self.color_change
            log_time = None

            flag = False # avoid displaying embed if the member change their activity / status

            member = after

            async for entry in guild.audit_logs(limit = 1):
                if entry.action == discord.AuditLogAction.member_role_update:
                    flag = True
                    old_roles = before.roles
                    new_roles = after.roles
                    role_change = []
                    if len(old_roles) < len(new_roles):
                        log_title = "Member Role Added"
                        role_change = ["<@&%d>" % role.id for role in new_roles if role not in old_roles]
                        log_content = '''
                                        Member: <@%d>
                                        Member name: %s
                                        Role added: %s
                                        ----------------------------
                                        Added by: <@%d>
                                        ''' % (member.id, str(member), role_change[0], entry.user.id)
                        log_time = entry.created_at
                    else:
                        log_title = "Member Role Removed"
                        role_change = ["<@&%d>" % role.id for role in old_roles if role not in new_roles]
                        log_content = '''
                                        Member: <@%d>
                                        Member name: %s
                                        Role removed: %s
                                        ----------------------------
                                        Removed by: <@%d>
                                        ''' % (member.id, str(member), role_change[0])
                elif entry.action == discord.AuditLogAction.member_update:
                    flag = True
                    log_title = "Nickname Changed"
                    old_nick = before.nick
                    new_nick = after.nick
                    if old_nick == new_nick:
                        return
                    elif old_nick == None:
                        old_nick = before.name
                    elif new_nick == None:
                        new_nick = after.name
                    log_content = '''
                                    **Before:** %s
                                    **After:** %s
                                    ----------------------------
                                    Edited by: <@%d>
                                    ''' % (old_nick, new_nick, entry.user.id)
                    log_time = entry.created_at

                if flag:
                    embed = discord.Embed(title = log_title, description = log_content, color = log_color, timestamp = log_time)
                    embed.set_author(name = str(member), icon_url = member.avatar_url)

                    await log_channel.send(embed = embed)

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        guild = channel.guild
        if self.log_check(guild):
            config = gconfig.get_config(guild.id)
            log_channel = self.bot.get_channel(config["LOG_CHANNEL"])

            log_channel = self.bot.get_channel(self.log_channel)
            log_title = ""
            log_content = ""
            log_color = self.color_create

            async for entry in guild.audit_logs(limit = 1, action = discord.AuditLogAction.channel_create):
                if isinstance(channel, discord.TextChannel):
                    log_title = "Text Channel Created"
                    log_content = '''
                                    Name: `%s`
                                    Type: Text Channel
                                    Category: `%s`
                                    Created by: <@%d>
                                    ----------------------------
                                    ID: %d
                                    Is NSFW: %s
                                    Position: %d
                                    ''' % (channel.name, channel.category.name if channel.category != None else "<None>", 
                                    entry.user.id, channel.id, "Yes" if channel.is_nsfw() else "No", channel.position)

                elif isinstance(channel, discord.VoiceChannel):
                    log_title = "Voice Channel Created"
                    log_content = '''
                                    Name: `%s`
                                    Type: Voice Channel
                                    Category: `%s`
                                    Created by: <@%d>
                                    ----------------------------
                                    ID: %d
                                    Position: %d
                                    ''' % (channel.name, channel.category.name if channel.category != None else "<None>",
                                    entry.user.id, channel.position)

                elif isinstance(channel, discord.CategoryChannel):
                    log_title = "Category Created"
                    log_content = '''
                                    Name: `%s`
                                    Created by: <@%d>
                                    ----------------------------
                                    ID: %d
                                    Position: %d
                                    ''' % (channel.name, entry.user.id, channel.id, channel.position)
                
                embed = discord.Embed(title = log_title, description = log_content, color = log_color)
                embed.timestamp = entry.created_at

                await log_channel.send(embed = embed)
    
    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        guild = channel.guild
        if self.log_check(guild):
            config = gconfig.get_config(guild.id)
            log_channel = self.bot.get_channel(config["LOG_CHANNEL"])
            
            log_channel = self.bot.get_channel(self.log_channel)
            log_title = ""
            log_content = ""
            log_color = self.color_create

            async for entry in guild.audit_logs(limit = 1, action = discord.AuditLogAction.channel_delete):
                if isinstance(channel, discord.TextChannel):
                    log_title = "Text Channel Deleted"
                    log_content = '''
                                    Name: `%s`
                                    Type: Text Channel
                                    Category: `%s`
                                    Deleted by: <@%d>
                                    ----------------------------
                                    ID: %d
                                    Is NSFW: %s
                                    Position: %d
                                    ''' % (channel.name, channel.category.name if channel.category != None else "<None>", 
                                    entry.user.id, channel.id, "Yes" if channel.is_nsfw() else "No", channel.position)

                elif isinstance(channel, discord.VoiceChannel):
                    log_title = "Voice Channel Deleted"
                    log_content = '''
                                    Name: `%s`
                                    Type: Voice Channel
                                    Category: `%s`
                                    Deleted by: <@%d>
                                    ----------------------------
                                    ID: %d
                                    Position: %d
                                    ''' % (channel.name, channel.category.name if channel.category != None else "<None>",
                                    entry.user.id, channel.position)

                elif isinstance(channel, discord.CategoryChannel):
                    log_title = "Category Deleted"
                    log_content = '''
                                    Name: `%s`
                                    Created by: <@%d>
                                    ----------------------------
                                    ID: %d
                                    Position: %d
                                    ''' % (channel.name, entry.user.id, channel.id, channel.position)
                
                embed = discord.Embed(title = log_title, description = log_content, color = log_color)
                embed.timestamp = entry.created_at

                await log_channel.send(embed = embed)

    @commands.Cog.listener()
    async def on_guild_channel_update(self, before, after):
        guild = before.guild
        if self.log_check(guild):
            config = gconfig.get_config(guild.id)
            log_channel = self.bot.get_channel(config["LOG_CHANNEL"])

            log_title = ""
            log_content = ""
            log_color = self.color_change
            log_time = None
            executor = None

            async for entry in guild.audit_logs(action = discord.AuditLogAction.channel_update, limit = 1):
                log_time = entry.created_at
                executor = entry.user.id

            if before.name != after.name:
                log_title = "Channel name changed"
                log_content = '''
                                **Before:** %s
                                **After:** %s
                                ----------------------------
                                Channel ID: %d
                                Executor: <@%d>
                                ''' % (before.name, after.name, after.id, executor)
                # Put embed inside here instead of outside because user can change multiple thing before pressing save.
                embed = discord.Embed(title = log_title, description = log_content, color = log_color, timestamp = log_time)
                await log_channel.send(embed = embed)
            # Archived, can cause spamming if move a channel way up/down.
            if before.position != after.position:
                pass
                #log_title = "Channel position changed"
                #log_content = '''
                #                **Before:** %d
                #                **After:** %d
                #                ----------------------------
                #                Channel ID: %d
                #                Category before: %s
                #                Category after: %s
                #                Executor: <@%d>
                #                ''' % (before.position, after.position, after.id, before.category, after.category, executor)
            if before.overwrites != after.overwrites:
                action = ""
                permission = None
                target_type = ""
                for key in after.overwrites:

                    # If there's a permission added/removed (add/remove permission for a member/role)
                    if key not in before.overwrites:
                        log_title = "Channel permission added"
                        log_content = '''
                                        Target: <@%s> (%s)
                                        ----------------------------
                                        Channel: <#%d>
                                        Executor: <@%d>
                                        ''' % (("&" + str(key.id)) if isinstance(key, discord.Role) else str(key.id), 
                                        "Role" if isinstance(key, discord.Role) else "Member", after.id, executor)
                        
                        embed = discord.Embed(title = log_title, description = log_content, color = log_color, timestamp = log_time)
                        await log_channel.send(embed = embed)
                        
                    else:
                        if before.overwrites[key] != after.overwrites[key]:
                            if isinstance(key, discord.Role):
                                target_type = "Role"
                            else:
                                target_type = "Member"
                    
                        # This is not confirmed if true or not, but discord.PermissionOverwrite is quite similar to
                        # discord.Permissions, except that it has None.

                        # Retrieve a PermissionOverwrite object.
                        before_overwrite = before.overwrites[key]
                        after_overwrite = after.overwrites[key]
                        
                        # Get the iter to iterate through the PermissionOverwrite.
                        iter_before = iter(before_overwrite)
                        iter_after = iter(after_overwrite)

                        while True:
                            try:
                                i_before = next(iter_before) # A tuple of (perm, False/None/True)
                                i_after = next(iter_after)
                                if i_before != i_after:
                                    permission = i_after[0]
                                    if i_after[1]:
                                        action = "allowed"
                                    elif i_after[1] is None:
                                        action = "neutralized"
                                    else:
                                        action = "denied"
                                
                                    log_title = "Channel permission %s" % action
                                    log_content = '''
                                                    Permission: %s
                                                    Target: <@%s> (%s)
                                                    ----------------------------
                                                    Channel: <#%d>
                                                    Executor: <@%d>
                                                    ''' % (permission, ("&" + str(key.id)) if isinstance(key, discord.Role) else str(key.id), 
                                                    target_type, after.id, executor)
                                    
                                    embed = discord.Embed(title = log_title, description = log_content, color = log_color, timestamp = log_time)
                                    await log_channel.send(embed = embed)
                                
                            except StopIteration:
                                break
                for key in before.overwrites:
                    if key not in after.overwrites:
                        log_title = "Channel permission removed"
                        log_content = '''
                                        Target: <@%s> (%s)
                                        ----------------------------
                                        Channel: <#%d>
                                        Executor: <@%d>
                                        ''' % (("&" + str(key.id)) if isinstance(key, discord.Role) else str(key.id), 
                                        "Role" if isinstance(key, discord.Role) else "Member", after.id, executor)
                        
                        embed = discord.Embed(title = log_title, description = log_content, color = log_color, timestamp = log_time)
                        await log_channel.send(embed = embed)

            if before.topic != after.topic:
                log_title = "Channel topic changed"
                log_content = '''
                                **Before:** %s
                                **After:** %s
                                ----------------------------
                                Channel ID: %d
                                Executor: <@%d>
                                ''' % (before.topic, after.topic, after.id, executor)
                
                embed = discord.Embed(title = log_title, description = log_content, color = log_color, timestamp = log_time)
                await log_channel.send(embed = embed)
                
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