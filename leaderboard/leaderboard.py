import asyncio
import datetime
import os

import discord
from redbot.core import Config, commands, checks


from redbot.core.bot import Red



class Leaderboard(commands.Cog):
    
    def __init__(self,bot:Red):

        self.bot = bot
        self.mod_dict = {} #store the last modified date for each fileS
        self._init_task = self.bot.loop.create_task(self._initialize())
        self.config = Config.get_conf(self, identifier=2248675723)
        self.default_member = {'score': 0}
        self.default_guild = {'list': []}#make sure we keep ordered
        self.config.register_member(**self.default_member)
        self.leaderboard = []
        
    def get_score(self,e):
        return  e[1]
    
    
    async def _initialize(self):
        mem_list = await self.config.all_members()
        mem_list = [(1090592618406227989,5), (2354252,3), (23423423424,9),  (5434,1)]
        mem_list.sort(reverse = True,key=self.get_score)
        self.leaderboard = mem_list
        print( mem_list)

    @commands.command()
    @checks.is_owner()
    async def point(self, ctx: commands.Context, member: discord.Member, points: int = 1):
        if member.id in self.leaderboard:
            cur = await self.config.member(member).score() + points
            await self.config.member(member).set(cur)
            mem_list = await self.config.all_members()
            for m in mem_list:
                if m[0] == member.id:
                    mem_list.remove(m)
                    mem_list.append((member.id, cur))
                mem_list.sort(reverse=True, key=self.get_score)
            await ctx.send(f'{member.mention} now has {str(cur)} points.')
            
            

    @commands.command()
    async def checklb(self, ctx: commands.Context):
        await ctx.send(str(self.leaderboard))
            