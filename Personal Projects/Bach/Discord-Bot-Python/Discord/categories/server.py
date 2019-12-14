import discord
from discord.ext import commands

import gconfig

class Server(commands.Cog, name = "Settings", command_attrs = {"cooldown_after_parsing": True}):
    '''Commands related to the bot setting in the server.'''
    def __init__(self, bot):
        self.bot = bot
        self.emoji = '🛠'
    
    @commands.command(name = "log-enable")
    @commands.has_permissions(manage_guild = True)
    @commands.bot_has_permissions(view_audit_log = True, send_messages = True)
    async def enable_log(self, ctx):
        '''
        Enable logging in your server.
        **Usage:** <prefix>**{command_name}**
        **Example:** {prefix}{command_name}

        You need: manage_guild.
        I need: view_audit_log, send_messages.
        '''
        config = gconfig.get_config(ctx.guild.id)
        if config["STATUS_LOG"] == 1:
            await ctx.send("Logging is already enabled for this server.")
        else:
            config["STATUS_LOG"] = 1
            gconfig.save_config(config)
            await ctx.send("Logging is enabled for this server. You should setup a log channel." % ctx.prefix)

    @commands.command(name = "log-setup")
    @commands.has_permissions(manage_guild = True)
    @commands.bot_has_permissions(view_audit_log = True, send_messages = True)
    async def set_log_channel(self, ctx, log : discord.TextChannel = None):
        '''
        Set or view a log channel in your server.
        If this command is invoked but you haven't enabled logging, it'll automatically be enabled.
        **Usage:** <prefix>**{command_name}** [text channel mention/ID/name]
        **Example 1:** {prefix}{command_name} 649111117204815883
        **Example 2:** {prefix}{command_name} a-random-log-channel
        **Example 3:** {prefix}{command_name}

        You need: manage_guild.
        I need: view_audit_log, send_messages.
        '''
        config = gconfig.get_config(ctx.guild.id)
        if log is None:
            await ctx.send("Current logging channel ID: `%d`" % config["LOG_CHANNEL"])
        else:
            config["STATUS_LOG"] = 1
            config["LOG_CHANNEL"] = log.id
            gconfig.save_config(config)
            
            embed = discord.Embed(title = "Logging Enabled", description = "This is now a logging channel.", color = discord.Color.green())
            embed.set_author(name = self.bot.user.name, icon_url = self.bot.user.avatar_url)
            import datetime
            embed.timestamp = datetime.datetime.utcnow()

            await log.send(embed = embed)
    
    @commands.command(name = "log-disable")
    @commands.has_permissions(manage_guild = True)
    @commands.bot_has_permissions(send_messages = True)
    async def disable_log(self, ctx):
        '''
        Disable logging in your server.
        **Usage:** <prefix>**{command_name}**
        **Example:** {prefix}{command_name}

        You need: manage_guild.
        I need: send_messages.
        '''
        config = gconfig.get_config(ctx.guild.id)
        config["STATUS_LOG"] = 0
        gconfig.save_config(config)
        await ctx.send("Logging is disabled for this server.")

    @commands.command(name = "welcome-enable")
    async def enable_welcome(self, ctx):
        '''
        Enable welcoming new members in your server.
        **Usage:** <prefix>**{command_name}**
        **Example:** {prefix}{command_name}

        You need: manage_guild.
        I need: send_messages.
        '''
        config = gconfig.get_config(ctx.guild.id)
        if config["STATUS_WELCOME"] == 1:
            await ctx.send("Welcoming system is already enabled for this server.")
        else:
            config["STATUS_WELCOME"] = 1
            gconfig.save_config(config)
            await ctx.send("Welcoming is enabled for this server. You should setup the welcome channel and message.")
    
    @commands.command(name = "welcome-setup")
    async def set_welcome_channel(self, ctx, welcome_chan : discord.TextChannel = None, *, welcome_text : str = None):
        '''
        Set or view the welcome channel and message in your server.
        If this command is invoked but you haven't enabled welcoming, it'll automatically be enabled.
        **Usage:** <prefix>{command_name} [text channel mention/ID/name] [welcome text]
        **Argument:** `[user.mention]`, `[user.name]`, `[guild.name]`, `[guild.count]`
        **Example 1:** {prefix}{command_name} 644336991135072261 Welcome [user.mention] to [guild.name]!
        **Example 2:** {prefix}{command_name} a-random-welcome-channel You are the [guild.count]th member!
        **Example 3:** {prefix}{command_name} #another-random-channel
        **Example 4:** {prefix}{command_name}

        You need: manage_guild.
        I need: send_messages.
        '''
        config = gconfig.get_config(ctx.guild.id)
        if welcome_chan is None:
            await ctx.send("Current welcome channel ID: `%d`"  % config["WELCOME_CHANNEL"])
            await ctx.send("Current welcome message: ", embed = discord.Embed(description = config["WELCOME_TEXT"]))
        else:
            config["STATUS_WELCOME"] = 1
            config["WELCOME_CHANNEL"] = welcome_chan.id
            await ctx.send("Channel <#%d> is now a welcome channel." % welcome_chan.id)

            if welcome_text == "":
                welcome_text = "Hello [user.mention]! Welcome to **[guild.name]**! You're the [guild.count]th member in this server! Enjoy the fun!!! :tada:"

            config["WELCOME_TEXT"] = welcome_text
            gconfig.save_config(config)
            await ctx.send("Your welcome message is: %s" % welcome_text)

    @commands.command(name = "welcome-disable")
    async def disable_welcome(self, ctx):
        '''
        Disable welcoming in your server.
        **Usage:** <prefix>**{command_name}**
        **Example:** {prefix}{command_name}**

        You need: manage_guild.
        I need: send_messages.
        '''
        config = gconfig.get_config(ctx.guild.id)
        config["STATUS_WELCOME"] = 0
        gconfig.save_config(config)
        await ctx.send("Welcoming is disabled for this server.")
    

def setup(bot):
    bot.add_cog(Server(bot))