import discord
from discord.ext import commands, tasks
from datetime import datetime, timedelta

author = "GeeterSkeeter#8008"

class VCDeafenMuteCheck(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.users = {}
        self.check_users.start()

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if before.channel != after.channel:
            if after.channel and after.deaf and after.mute:
                self.users[member.id] = {
                    'member': member,
                    'start_time': datetime.utcnow(),
                    'alert_sent': False
                }
            else:
                if member.id in self.users:
                    del self.users[member.id]

    @tasks.loop(seconds=60)
    async def check_users(self):
        for user_id, user_data in list(self.users.items()):
            if datetime.utcnow() - user_data['start_time'] >= timedelta(hours=1):
                if not user_data['alert_sent']:
                    try:
                        dm_channel = await user_data['member'].create_dm()
                        await dm_channel.send("Hi, are you still online? Reply with 'yes' if you are.")
                        user_data['alert_sent'] = True
                    except discord.errors.Forbidden:
                        del self.users[user_id]
                elif datetime.utcnow() - user_data['start_time'] >= timedelta(hours=1, minutes=10):
                    del self.users[user_id]
                    guild = user_data['member'].guild
                    afk_channel = guild.afk_channel or discord.utils.get(guild.voice_channels, name='AFK')
                    if afk_channel:
                        await user_data['member'].move_to(afk_channel)
                        
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.id in self.users and message.content.lower() == 'yes':
            if isinstance(message.channel, discord.DMChannel):
                del self.users[message.author.id]

    def cog_unload(self):
        self.check_users.cancel()
