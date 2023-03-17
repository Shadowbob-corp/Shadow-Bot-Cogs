import asyncio
import contextlib
import datetime

import discord

from redbot.core import Config, checks, commands, modlog
from redbot.core.bot import Red



class ShareTheLove(commands.Cog):
    """ShareTheLove"""


    def __init__(self) -> None:
        super().__init__()
        self.current_member = None
        self.timestamp = None
        self.channel = 1084000224491602010
        self.listening = False

    @commands.command()
    @checks.is_owner()
    async def love(self, ctx: commands.Context, user: discord.member):
        if self.current_member is None:
            while(True):
                self.timestamp = datetime.datetime.now()
                self.current_member = user
                channel = ctx.guild.get_channel(self.channel)
                await channel.send(f'{user.mention} is the the share-the-love user for the day. \nLet them know how amazing they are!')
                await(43200)
                await user.send(f"You're day is up, please go to the {channel.name} channel and @ a user.")
    
    @commands.Cog.listener()
    async def on_message(self, ctx: commands.Context, message: discord.Message):
        if self.listening:
            
