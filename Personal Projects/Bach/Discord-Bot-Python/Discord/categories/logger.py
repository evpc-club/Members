import discord
from discord.ext import commands

import datetime

import gconfig

# Specification:
# Every single events here (except raw events) must have the following variables declared at the very first line after checking log:
# - log_channel: the channel that's gonna send the embed. Retrieve using gconfig.get_config and config["LOG_CHANNEL"]
# - log_title: the log title that's gonna pass in title in discord.Embed
# - log_content: the log content that's gonna pass in description in discord.Embed
# - log_color: the color of the embed. It must be self.color_... depend on the current event.
# - log_time: the timestamp of the embed. Typically get from entry.created_at.
# - Optional(executor): the Member ID that triggered the event.

# Log embed specification:
# Every single embed send here (except raw events) must have the following format:
# Embed.author as the executor.
# Embed.title as log_title.
# Embed.description as log_content.
# Embed.color as log_color.
# Embed.timestamp as log_time.
# Embed.footer as the executor.


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

    def role_dpyperms_to_dperms(self, role_permissions : str):
        if role_permissions == "administrator":
            return "Administrator"
        if role_permissions == "view_audit_log":
            return "View Audit Log"
        if role_permissions == "manage_guild":
            return "Manage Server"
        if role_permissions == "manage_roles":
            return "Manage Roles"
        if role_permissions == "manage_channels":
            return "Manage Channels"
        if role_permissions == "kick_members":
            return "Kick Members"
        if role_permissions == "ban_members":
            return "Ban Members"
        if role_permissions == "create_instant_invite":
            return "Create Invite"
        if role_permissions == "change_nickname":
            return "Change Nickname"
        if role_permissions == "manage_nicknames":
            return "Manage Nicknames"
        if role_permissions == "manage_emojis":
            return "Manage Emojis"
        if role_permissions == "manage_webhooks":
            return "Manage Webhooks"
        if role_permissions == "read_messages":
            return "Read Text Channels & See Voice Channels"
        if role_permissions == "send_messages":
            return "Send Messages"
        if role_permissions == "send_tts_messages":
            return "Send TTS Messages"
        if role_permissions == "embed_links":
            return "Embed Links"
        if role_permissions == "attach_files":
            return "Attach Files"
        if role_permissions == "read_message_history":
            return "Read Message History"
        if role_permissions == "mention_everyone":
            return "Mention Everyone"
        if role_permissions == "external_emojis":
            return "Use External Emojis"
        if role_permissions == "add_reactions":
            return "Add Reactions"
        if role_permissions == "connect":
            return "Connect"
        if role_permissions == "speak":
            return "Speak"
        if role_permissions == "mute_members":
            return "Mute Members"
        if role_permissions == "deafen_members":
            return "Deafen Members"
        if role_permissions == "move_members":
            return "Move Members"
        if role_permissions == "use_voice_activation":
            return "Use Voice Activity"
        if role_permissions == "priority_speaker":
            return "Priority Speaker"
        if role_permissions == "stream":
            return "Go Live"
    
    def channel_dpyperms_to_dperms(self, channel_permissions):
        if channel_permissions == "create_instant_invite":
            return "Create Invite"
        if channel_permissions == "manage_channels":
            return "Manage Channels"
        if channel_permissions == "manage_roles":
            return "Manage Permissions"
        if channel_permissions == "manage_webhooks":
            return "Manage Webhooks"
        if channel_permissions == "read_messages":
            return "Read Messages & View Channel"
        if channel_permissions == "send_messages":
            return "Send Messages"
        if channel_permissions == "send_tts_messages":
            return "Send TTS Messages"
        if channel_permissions == "embed_links":
            return "Embed Links"
        if channel_permissions == "attach_files":
            return "Attach Files"
        if channel_permissions == "read_message_history":
            return "Read Message History"
        if channel_permissions == "mention_everyone":
            return "Mention Everyone"
        if channel_permissions == "external_emojis":
            return "Use External Emojis"
        if channel_permissions == "add_reactions":
            return "Add Reactions"
        # Voice channels
        if channel_permissions == "connect":
            return "Connect"
        if channel_permissions == "speak":
            return "Speak"
        if channel_permissions == "mute_members":
            return "Mute Members"
        if channel_permissions == "deafen_members":
            return "Deafen Members"
        if channel_permissions == "move_members":
            return "Move Members"
        if channel_permissions == "use_voice_activation":
            return "Use Voice Activity"
        if channel_permissions == "priority_speaker":
            return "Priority Speaker"
        if channel_permissions == "stream":
            return "Go Live"
    
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

            executor_id = 0

            async for entry in message.guild.audit_logs(action = discord.AuditLogAction.message_delete, limit = 1):
                executor_id = entry.user.id
                log_time = datetime.utcnow() # Audit log doesn't log message that the author delete himself.

                log_content = '''
                                Content: %s
                                Author: <@%d>
                                Deleted by: <@%d>
                                ----------------------------
                                Channel: <#%s>
                                ''' % (
                                    message.content, 
                                    message.author.id, 
                                    executor_id, 
                                    message.channel.id
                                )
                embed = discord.Embed(
                    title = log_title, 
                    description = log_content, 
                    color = log_color, 
                    timestamp = log_time
                )
                embed.set_thumbnail(url = message.author.avatar_url)
                embed.set_author(
                    name = str(entry.user), 
                    icon_url = entry.user.avatar_url
                )
                embed.set_footer(
                    text = str(entry.user),
                    icon_url = entry.user.avatar_url
                )

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

                embed = discord.Embed(
                    title = log_title, 
                    description = log_content, 
                    color = log_color
                )
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
                                **Before:** %s
                                **After:** %s
                                Author: <@%d>
                                ----------------------------
                                Channel: <#%s>
                                ''' % (before.content, after.content, after.author.id, after.channel.id)
                log_color = self.color_change
                log_time = after.edited_at

                embed = discord.Embed(
                    title = log_title, 
                    description = log_content, 
                    color = log_color, 
                    timestamp = log_time
                )
                                    
                embed.set_thumbnail(url = after.author.avatar_url)
                embed.set_author(
                    name = str(after.author), 
                    icon_url = after.author.avatar_url
                )
                embed.set_footer(
                    text = str(after.author),
                    icon_url = after.author.avatar_url
                )

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
            executor_id = 0
            
            async for entry in guild.audit_logs(action = discord.AuditLogAction.ban, limit = 1):        
                if entry.reason == None:
                    reason = "Not provided."
                else:
                    reason = entry.reason
                executor_id = entry.user.id
                log_time = entry.created_at
                
                log_content = '''
                                User: <@%d>
                                User name: %s
                                Reason: %s
                                ----------------------------
                                Banned by: <@%d>
                                '''  % (user.id, str(user), reason, executor_id)

                embed = discord.Embed(
                    title = log_title, 
                    description = log_content, 
                    color = log_color, 
                    timestamp = log_time
                )
                embed.set_author(
                    name = str(entry.user),
                    icon_url = entry.user.avatar_url
                )
                embed.set_footer(
                    text = str(entry.user),
                    icon_url = entry.user.avatar_url
                )

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
            executor_id = None
            
            async for entry in guild.audit_logs(action = discord.AuditLogAction.unban, limit = 1):        
                if entry.reason == None:
                    reason = "Not provided."
                else:
                    reason = entry.reason
                executor_id = entry.user.id
                log_time = entry.created_at
                
                log_content = '''
                                User: <@%d>
                                User name: %s
                                Reason: %s
                                ----------------------------
                                Unbanned by: <@%d>
                                '''  % (user.id, str(user), reason, executor_id)
                
                embed = discord.Embed(
                    title = log_title, 
                    description = log_content, 
                    color = log_color, 
                    timestamp = log_time
                )
                embed.set_author(
                    name = str(entry.user),
                    icon_url = entry.user.avatar_url
                )
                embed.set_footer(
                    text = str(entry.user),
                    icon_url = entry.user.avatar_url
                )

                await log_channel.send(embed = embed)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        guild = member.guild
        if self.log_check(guild):
            config = gconfig.get_config(guild.id)
            log_channel = self.bot.get_channel(config["LOG_CHANNEL"])

            log_title = "Member Joined"
            log_content = '''
                            Member: <@%d>
                            Member name: %s
                            ----------------------------
                            Member ID: %d
                            Account created on: %d/%d/%d %d:%s %s (UTC)
                            ''' % (
                                member.id,
                                str(member),
                                member.id,
                                member.created_at.month,
                                member.created_at.day,
                                member.created_at.year,
                                member.created_at.hour % 12,
                                "0" + str(member.created_at.minute) if member.created_at.minute / 10 < 1 else str(member.created_at.minute),
                                "AM" if member.created_at.hour / 12 < 1 else "PM"
                            )
            log_color = self.color_guild_join_leave
            log_time = datetime.datetime.utcnow()

            embed = discord.Embed(
                title = log_title,
                description = log_content,
                color = log_color,
                timestamp = log_time
            )
            embed.set_thumbnail(url = member.avatar_url)
            embed.set_author(
                name = str(member),
                icon_url = member.avatar_url
            )
            embed.set_footer(
                text = str(member),
                icon_url = member.avatar_url
            )

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
            executor_id = 0
            
            async for entry in guild.audit_logs(limit = 1):
                if entry.target.id == member.id and entry.action == discord.AuditLogAction.kick:
                    if entry.reason == None:
                        reason = "Not provided."
                    else:
                        reason = entry.reason
                    
                    executor_id = entry.user.id
                    log_time = entry.created_at

                    log_title = "Member Kicked"
                    log_content = '''
                                Member: <@%d>
                                Member name: %s
                                Reason: %s
                                ----------------------------
                                Executor: <@%d>
                                '''  % (member.id, str(member), reason, executor_id)
                    log_color = self.color_moderation
                    
                    embed = discord.Embed(
                        title = log_title, 
                        description = log_content, 
                        color = log_color, 
                        timestamp = log_time
                    )
                    embed.set_thumbnail(url = member.avatar_url)
                    embed.set_author(
                        name = str(entry.user),
                        icon_url = entry.user.avatar_url
                    )
                    embed.set_footer(
                        text = str(entry.user),
                        icon_url = entry.user.avatar_url
                    )

                    await log_channel.send(embed = embed)
            
                log_title = "Member Left"
                log_content = '''
                                Member: <@%d>
                                Member name: %s
                                ----------------------------
                                Member ID: %d
                                ''' % (member.id, str(member), member.id)
                log_color = self.color_guild_join_leave
                log_time = datetime.datetime.utcnow() # entry.created_at is unreliable

                embed = discord.Embed(
                    title = log_title, 
                    description = log_content, 
                    color = log_color, 
                    timestamp = log_time
                )
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

            executor_id = 0
            flag = False # avoid displaying embed if the member change their activity / status

            async for entry in guild.audit_logs(limit = 1):
                executor_id = entry.user.id
                log_time = entry.created_at

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
                                        ''' % (after.id, str(after), role_change[0], executor_id)
                    else:
                        log_title = "Member Role Removed"
                        role_change = ["<@&%d>" % role.id for role in old_roles if role not in new_roles]

                        log_content = '''
                                        Member: <@%d>
                                        Member name: %s
                                        Role removed: %s
                                        ----------------------------
                                        Removed by: <@%d>
                                        ''' % (after.id, str(after), role_change[0], executor_id)
                elif entry.action == discord.AuditLogAction.member_update:
                    flag = True

                    old_nick = before.nick
                    new_nick = after.nick
                    if old_nick == new_nick:
                        return
                    elif old_nick == None:
                        old_nick = before.name
                    elif new_nick == None:
                        new_nick = after.name
                    
                    log_title = "Nickname Changed"
                    log_content = '''
                                    **Before:** %s
                                    **After:** %s
                                    ----------------------------
                                    Edited by: <@%d>
                                    ''' % (old_nick, new_nick, executor_id)
                
                if flag:
                    embed = discord.Embed(
                        title = log_title, 
                        description = log_content, 
                        color = log_color, 
                        timestamp = log_time
                    )
                    embed.set_author(
                        name = str(entry.user), 
                        icon_url = entry.user.avatar_url
                    )
                    embed.set_footer(
                        text = str(entry.user),
                        icon_url = entry.user.avatar_url
                    )

                    await log_channel.send(embed = embed)

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        guild = channel.guild
        if self.log_check(guild):
            config = gconfig.get_config(guild.id)
            log_channel = self.bot.get_channel(config["LOG_CHANNEL"])

            log_title = ""
            log_content = ""
            log_color = self.color_create
            log_time = None

            executor_id = 0

            async for entry in guild.audit_logs(limit = 1, action = discord.AuditLogAction.channel_create):
                executor_id = entry.user.id
                log_time = entry.created_at

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
                                    ''' % (
                                        channel.name, 
                                        channel.category.name if channel.category != None else "<None>", 
                                        executor_id, 
                                        channel.id, 
                                        "Yes" if channel.is_nsfw() else "No", 
                                        channel.position
                                    )

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
                                    ''' % (
                                        channel.name, 
                                        channel.category.name if channel.category != None else "<None>",
                                        executor_id, 
                                        channel.position
                                    )

                elif isinstance(channel, discord.CategoryChannel):
                    log_title = "Category Created"
                    log_content = '''
                                    Name: `%s`
                                    Created by: <@%d>
                                    ----------------------------
                                    ID: %d
                                    Position: %d
                                    ''' % (
                                        channel.name, 
                                        entry.user.id, 
                                        channel.id, 
                                        channel.position
                                    )
                
                embed = discord.Embed(
                    title = log_title, 
                    description = log_content, 
                    color = log_color,
                    timestamp = log_time
                )
                embed.set_author(
                    name = str(entry.user),
                    icon_url = entry.user.avatar_url
                )
                embed.set_footer(
                    text = str(entry.user),
                    icon_url = entry.user.avatar_url
                )

                await log_channel.send(embed = embed)
    
    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        guild = channel.guild
        if self.log_check(guild):
            config = gconfig.get_config(guild.id)
            log_channel = self.bot.get_channel(config["LOG_CHANNEL"])
            
            log_title = ""
            log_content = ""
            log_color = self.color_delete
            log_time = None

            executor_id = 0

            async for entry in guild.audit_logs(limit = 1, action = discord.AuditLogAction.channel_delete):
                executor_id = entry.user.id
                log_time = entry.created_at

                if isinstance(channel, discord.TextChannel):
                    log_title = "Text Channel Deleted"
                    log_content = '''
                                    Name: `%s`
                                    Type: Text Channel
                                    Category: `%s`
                                    Deleted by: <@%d>
                                    ----------------------------
                                    ID: %d
                                    Was NSFW: %s
                                    Position: %d
                                    ''' % (
                                        channel.name, 
                                        channel.category.name if channel.category != None else "<None>", 
                                        executor_id, 
                                        channel.id, 
                                        "Yes" if channel.is_nsfw() else "No", 
                                        channel.position
                                    )

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
                                    ''' % (
                                        channel.name, 
                                        channel.category.name if channel.category != None else "<None>",
                                        executor_id, 
                                        channel.position
                                    )
                    log_time = entry.created_at

                elif isinstance(channel, discord.CategoryChannel):
                    log_title = "Category Deleted"
                    log_content = '''
                                    Name: `%s`
                                    Created by: <@%d>
                                    ----------------------------
                                    ID: %d
                                    Position: %d
                                    ''' % (
                                        channel.name, 
                                        executor_id, 
                                        channel.id, 
                                        channel.position
                                    )
                
                embed = discord.Embed(
                    title = log_title, 
                    description = log_content, 
                    color = log_color,
                    timestamp = log_time
                )
                embed.set_author(
                    name = str(entry.user),
                    icon_url = entry.user.avatar_url
                )
                embed.set_footer(
                    text = str(entry.user),
                    icon_url = entry.user.avatar_url
                )

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

            executor_id = 0

            async for entry in guild.audit_logs(action = discord.AuditLogAction.channel_update, limit = 1):
                executor_id = entry.user.id
                log_time = entry.created_at

                if before.name != after.name:
                    log_title = "Channel Name Changed"
                    log_content = '''
                                    Channel: <#%d>
                                    **Before:** %s
                                    **After:** %s
                                    ----------------------------
                                    Channel ID: %d
                                    Changed by: <@%d>
                                    ''' % (
                                        after.id,
                                        before.name, 
                                        after.name, 
                                        after.id, 
                                        executor_id
                                    )
                    # Put embed inside here instead of outside because user can change multiple thing before pressing save.
                    embed = discord.Embed(
                        title = log_title, 
                        description = log_content, 
                        color = log_color, 
                        timestamp = log_time
                    )
                    embed.set_author(
                        name = str(entry.user),
                        icon_url = entry.user.avatar_url
                    )
                    embed.set_footer(
                        text = str(entry.user),
                        icon_url = entry.user.avatar_url
                    )

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
                if before.topic != after.topic and before.topic != None: # For some reasons, changing the name of a new channel will also call this.
                    log_title = "Channel Topic Changed"
                    log_content = '''
                                    Channel: <#%d>
                                    **Before:** %s
                                    **After:** %s
                                    ----------------------------
                                    Channel ID: %d
                                    Changed by: <@%d>
                                    ''' % (
                                        after.id,
                                        before.topic, 
                                        after.topic, 
                                        after.id, 
                                        executor_id
                                    )
                    
                    embed = discord.Embed(
                        title = log_title, 
                        description = log_content, 
                        color = log_color, 
                        timestamp = log_time
                    )
                    embed.set_author(
                        name = str(entry.user),
                        icon_url = entry.user.avatar_url
                    )
                    embed.set_footer(
                        text = str(entry.user),
                        icon_url = entry.user.avatar_url
                    )
                    
                    await log_channel.send(embed = embed)
            # The structure of overwrites look like this:
            # class PermissionOverwrite { self.send_messages = True/None/False; self.read_messages = True/None/False;...}
            # before.overwrites and after.overwrites return sth like this:
            # {"Role/Member": PermissionOverwrite, "Role/Member": PermissionOverwrite,...}
            #
            # So first of, we check if there are any new keys or missing keys
            # If yes, then it's permission added, and we look for the key and its value.
            # If no, then we iterate (by iter()) through all the attributes in PermissionOverwrite for before and after
            # If there's sth different, then we log it right away, because a user can edit many...
            # ...permissions before one press "Save Changes".
            async for entry in guild.audit_logs(action = discord.AuditLogAction.overwrite_update, limit = 1):
                executor_id = entry.user.id
                log_time = entry.created_at

                if before.overwrites != after.overwrites:
                    action = ""
                    permission = None
                    target_type = ""

                    for key in after.overwrites:

                        # If there's a permission added/removed (add/remove permission for a member/role)
                        if key not in before.overwrites:
                            log_title = "Channel Permission Added"
                            log_content = '''
                                            Target: <@%s> (%s)
                                            ----------------------------
                                            Channel: <#%d>
                                            Added by: <@%d>
                                            ''' % (
                                                ("&" + str(key.id)) if isinstance(key, discord.Role) else str(key.id), 
                                                "Role" if isinstance(key, discord.Role) else "Member", 
                                                after.id, 
                                                executor_id
                                            )
                            
                            embed = discord.Embed(
                                title = log_title, 
                                description = log_content, 
                                color = log_color, 
                                timestamp = log_time
                            )
                            embed.set_author(
                                name = str(entry.user),
                                icon_url = entry.user.avatar_url
                            )
                            embed.set_footer(
                                text = str(entry.user),
                                icon_url = entry.user.avatar_url
                            )

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
                                        permission = self.channel_dpyperms_to_dperms(i_after[0])
                                        if i_after[1]:
                                            action = "Granted"
                                        elif i_after[1] is None:
                                            action = "Neutralized"
                                        else:
                                            action = "Denied"
                                    
                                        log_title = "Channel Permission %s" % action
                                        log_content = '''
                                                        Permission: `%s`
                                                        Target: <@%s> (%s)
                                                        ----------------------------
                                                        Channel: <#%d>
                                                        Executor: <@%d>
                                                        ''' % (
                                                            permission, 
                                                            ("&" + str(key.id)) if isinstance(key, discord.Role) else str(key.id), 
                                                            target_type, 
                                                            after.id, 
                                                            executor_id
                                                        )
                                        
                                        embed = discord.Embed(
                                            title = log_title, 
                                            description = log_content, 
                                            color = log_color, 
                                            timestamp = log_time
                                        )
                                        embed.set_author(
                                            name = str(entry.user),
                                            icon_url = entry.user.avatar_url
                                        )
                                        embed.set_footer(
                                            text = str(entry.user),
                                            icon_url = entry.user.avatar_url
                                        )

                                        await log_channel.send(embed = embed)
                                    
                                except StopIteration:
                                    break
                    for key in before.overwrites:
                        if key not in after.overwrites:
                            log_title = "Channel Permission Removed"
                            log_content = '''
                                            Target: <@%s> (%s)
                                            ----------------------------
                                            Channel: <#%d>
                                            Removed by: <@%d>
                                            ''' % (
                                                ("&" + str(key.id)) if isinstance(key, discord.Role) else str(key.id), 
                                                "Role" if isinstance(key, discord.Role) else "Member", 
                                                after.id, 
                                                executor_id
                                            )
                            
                            embed = discord.Embed(
                                title = log_title, 
                                description = log_content, 
                                color = log_color, 
                                timestamp = log_time
                            )
                            embed.set_author(
                                name = str(entry.user),
                                icon_url = entry.user.avatar_url
                            )
                            embed.set_footer(
                                text = str(entry.user),
                                icon_url = entry.user.avatar_url
                            )

                            await log_channel.send(embed = embed)

    @commands.Cog.listener()
    async def on_guild_update(self, before, after):
        if self.log_check(after.guild):
            config = gconfig.get_config(after.guild.id)
            log_channel = self.bot.get_channel(config["LOG_CHANNEL"])

            log_title = ""
            log_content = ""
            log_color = self.color_change
            log_time = None

            executor_id = 0

            async for entry in after.guild.audit_logs(action = discord.AuditLogAction.guild_update, limit = 1):
                executor_id = entry.user.id
                log_time = entry.created_at

                flag = False

                if hasattr(entry.before, "name") and hasattr(entry.after, "name"):
                    flag = True
                    log_title = "Server Name Changed"
                    log_content = '''
                                    **Before:** %s
                                    **After:** %s
                                    ----------------------------
                                    Changed by: <@%d>
                                    ''' % (
                                        before.name,
                                        after.name,
                                        executor_id
                                    )
                elif hasattr(entry.before, "owner") and hasattr(entry.after, "owner"):
                    flag = True
                    log_title = "Server Owner Changed"
                    log_content = '''
                                    **Before:** <@%d>
                                    **After:** <@%d>
                                    ''' % (
                                        before.owner.id,
                                        after.owner.id,
                                    )
                
                if flag:
                    embed = discord.Embed(
                        title = log_title,
                        description = log_content,
                        color = log_color,
                        timestamp = log_time
                    )
                    embed.set_author(
                        name = str(entry.user),
                        icon_url = entry.user.avatar_url
                    )
                    embed.set_footer(
                        text = str(entry.user),
                        icon_url = entry.user.avatar_url
                    )

                    await log_channel.send(embed = embed)

    @commands.Cog.listener()
    async def on_guild_role_create(self, role):
        guild = role.guild
        if self.log_check(guild):
            config = gconfig.get_config(guild.id)
            log_channel = self.bot.get_channel(config["LOG_CHANNEL"])

            log_title = "Role Created"
            log_content = ""
            log_color = self.color_create
            log_time = None

            executor_id = 0

            async for entry in guild.audit_logs(action = discord.AuditLogAction.role_create, limit = 1):
                log_time = entry.created_at
                executor_id = entry.user.id

                role_perm = []
                
                if role.permissions.administrator:
                    role_perm.append("Administrator")
                if role.permissions.view_audit_log:
                    role_perm.append("View Audit Log")
                if role.permissions.manage_guild:
                    role_perm.append("Manage Server")
                if role.permissions.manage_roles:
                    role_perm.append("Manage Roles")
                if role.permissions.manage_channels:
                    role_perm.append("Manage Channels")
                if role.permissions.kick_members:
                    role_perm.append("Kick Members")
                if role.permissions.ban_members:
                    role_perm.append("Ban Members")
                if role.permissions.create_instant_invite:
                    role_perm.append("Create Invite")
                if role.permissions.change_nickname:
                    role_perm.append("Change Nickname")
                if role.permissions.manage_nicknames:
                    role_perm.append("Manage Nicknames")
                if role.permissions.manage_emojis:
                    role_perm.append("Manage Emojis")
                if role.permissions.manage_webhooks:
                    role_perm.append("Manage Webhooks")
                if role.permissions.send_messages:
                    role_perm.append("Send Messages")
                if role.permissions.send_tts_messages:
                    role_perm.append("Send TTS Messages")
                if role.permissions.embed_links:
                    role_perm.append("Embed Links")
                if role.permissions.attach_files:
                    role_perm.append("Attach Files")
                if role.permissions.read_message_history:
                    role_perm.append("Read Message History")
                if role.permissions.mention_everyone:
                    role_perm.append("Mention Everyone")
                if role.permissions.external_emojis:
                    role_perm.append("Use External Emojis")
                if role.permissions.add_reactions:
                    role_perm.append("Add Reactions")
                if role.permissions.connect:
                    role_perm.append("Connect")
                if role.permissions.speak:
                    role_perm.append("Speak")
                if role.permissions.mute_members:
                    role_perm.append("Mute Members")
                if role.permissions.deafen_members:
                    role_perm.append("Deafen Members")
                if role.permissions.move_members:
                    role_perm.append("Move Members")
                if role.permissions.use_voice_activation:
                    role_perm.append("Use Voice Activity")
                if role.permissions.priority_speaker:
                    role_perm.append("Priority Speaker")
                if role.permissions.stream:
                    role_perm.append("Go Live")
                
                str_role_perm = ""
                for perm in role_perm:
                    str_role_perm += "`%s` " % perm

                log_content = '''
                                Role: <@&%d>
                                Name: %s
                                Created by: <@%d>
                                Granted Permissions: %s
                                ----------------------------
                                Is separated: %s
                                Is mentionable: %s
                                Color: %s
                                ''' % (
                                    role.id, 
                                    role.name, 
                                    executor_id, 
                                    str_role_perm,
                                    "Yes" if role.hoist else "No",
                                    "Yes" if role.mentionable else "No",
                                    str(role.color)
                                )

                embed = discord.Embed(
                    title = log_title,
                    description = log_content,
                    color = log_color,
                    timestamp = log_time
                )
                embed.set_author(
                    name = str(entry.user),
                    icon_url = entry.user.avatar_url
                )
                embed.set_footer(
                    text = str(entry.user),
                    icon_url = entry.user.avatar_url
                )

                await log_channel.send(embed = embed)
    
    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):
        guild = role.guild
        if self.log_check(guild):
            config = gconfig.get_config(guild.id)
            log_channel = self.bot.get_channel(config["LOG_CHANNEL"])

            log_title = "Role Deleted"
            log_content = ""
            log_color = self.color_delete
            log_time = None

            executor_id = 0

            async for entry in guild.audit_logs(action = discord.AuditLogAction.role_delete, limit = 1):
                log_time = entry.created_at
                executor_id = entry.user.id
            
                log_content = '''
                                Name: `%s`
                                Deleted by: <@%d>
                                ----------------------------
                                Was separated: %s
                                Was mentionable: %s
                                Color: %s
                                ''' % (
                                    role.name,
                                    executor_id,
                                    "Yes" if role.hoist else "No",
                                    "Yes" if role.mentionable else "No",
                                    str(role.color)
                                )
                
                embed = discord.Embed(
                    title = log_title,
                    description = log_content,
                    color = log_color,
                    timestamp = log_time
                )
                embed.set_author(
                    name = str(entry.user),
                    icon_url = entry.user.avatar_url
                )
                embed.set_footer(
                    text = str(entry.user),
                    icon_url = entry.user.avatar_url
                )


                await log_channel.send(embed = embed)

    @commands.Cog.listener()
    async def on_guild_role_update(self, before, after):
        guild = before.guild
        if self.log_check(guild):
            config = gconfig.get_config(guild.id)
            log_channel = self.bot.get_channel(config["LOG_CHANNEL"])

            log_title = ""
            log_content = ""
            log_color = self.color_change
            log_time = None

            executor_id = 0

            async for entry in guild.audit_logs(action = discord.AuditLogAction.role_update, limit = 1):
                log_time = entry.created_at
                executor_id = entry.user.id

                if before.name != after.name:
                    log_title = "Role Name Changed"
                    log_content = '''
                                    Role: <@&%d>
                                    **Before:** %s
                                    **After:** %s
                                    ----------------------------
                                    Changed by: <@%d>
                                    ''' % (
                                        after.id,
                                        before.name,
                                        after.name,
                                        executor_id
                                    )
                    
                    embed = discord.Embed(
                        title = log_title,
                        description = log_content,
                        color = log_color,
                        timestamp = log_time
                    )
                    embed.set_author(
                        name = str(entry.user),
                        icon_url = entry.user.avatar_url
                    )
                    embed.set_footer(
                        text = str(entry.user),
                        icon_url = entry.user.avatar_url
                    )

                    await log_channel.send(embed = embed)
                if before.color != after.color:
                    log_title = "Role Color Changed"
                    log_content = '''
                                    Role: <@&%d>
                                    **Before:** %s
                                    **After:**
                                    ----------------------------
                                    Changed by: <@%d>
                                    ''' % (
                                        after.id,
                                        before.color, 
                                        after.color,
                                        executor_id
                                    )
                    
                    embed = discord.Embed(
                        title = log_title,
                        description = log_content,
                        color = log_color,
                        timestamp = log_time
                    )
                    embed.set_author(
                        name = str(entry.user),
                        icon_url = entry.user.avatar_url
                    )
                    embed.set_footer(
                        text = str(entry.user),
                        icon_url = entry.user.avatar_url
                    )

                    await log_channel.send(embed = embed)
                # The next 2 seems unimportant, so skip those for now.
                if before.mentionable != after.mentionable:
                    pass
                if before.hoist != after.hoist:
                    pass
                # Quite similar to on_guild_channel_update
                if before.permissions != after.permissions:
                    action = ""
                    permission = None
                    
                    iter_before = iter(before.permissions)
                    iter_after = iter(after.permissions)

                    while True:
                        try:
                            i_before = next(iter_before)
                            i_after = next(iter_after)

                            if i_before != i_after:
                                permission = self.role_dpyperms_to_dperms(i_after[0])
                                
                                if i_after[1]:
                                    action = "Granted"
                                else:
                                    action = "Denied"
                                
                                log_title = "Role Permission %s" % action
                                log_content = '''
                                                Permission: `%s`
                                                Target: <@&%d>
                                                ----------------------------
                                                Executor: <@%d>
                                                ''' % (
                                                    permission,
                                                    after.id,
                                                    executor_id
                                                )
                                
                                embed = discord.Embed(
                                    title = log_title,
                                    description = log_content,
                                    color = log_color,
                                    timestamp = log_time
                                )
                                embed.set_author(
                                    name = str(entry.user),
                                    icon_url = entry.user.avatar_url
                                )
                                embed.set_footer(
                                    text = str(entry.user),
                                    icon_url = entry.user.avatar_url
                                )

                                await log_channel.send(embed = embed)

                        except StopIteration:
                            break

    @commands.Cog.listener()
    async def on_command_error(self, error):
        pass


def setup(bot):
    bot.add_cog(Logging(bot))