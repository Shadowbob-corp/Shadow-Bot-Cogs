"""
MIT License

Copyright (c) 2021-present Obi-Wan3

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from datetime import datetime
import random
import asyncio
import discord
from redbot.core.bot import Red
from redbot.core import commands, bank, checks
from redbot.core.utils.predicates import MessagePredicate


class Zombies(commands.Cog):
    """
    A game of Zombies.  Be the last one standing to win.
    """

    def __init__(self, bot):
        self.bot = bot
        self.zombies = []
        self.zplayer = 1084782445339082752
        self.zrole = 1084787982290141264
        self.zchannel = 1084788526861783060
        self.infected = {}
        self.round = 0

    @commands.command()
    async def zombies(self, ctx: commands.Context):
        zombie = False
        for a in ctx.author.roles:
            if self.zplayer == a.id:
                
                zombie = True
                break
        if not zombie:
            await ctx.send(f"{ctx.author.mention} do you want to join the Zombies game? (yes/no)")
            pred = MessagePredicate.yes_or_no(ctx)        
            event = "message"

            try:
                await ctx.bot.wait_for(event, check=pred, timeout=60)
            except asyncio.TimeoutError:
                await ctx.send("You took too long, you have 30 seconds to upload the file or link.")
                return
            if pred.result:     
                await ctx.author.add_roles(ctx.g.get_role(self.zplayer))
                await ctx.send(f"Congrats {ctx.ar.mention}, you will be notified when the game starts!")
    
    def make_str(self, ctx,):
        r = ctx.get_role(self.zplayer)
        tot = ""
        for m in r.members:
            tot += " " + m.name + ', '
        return tot

    @commands.command()
    @checks.is_owner()
    async def startzombies(self, ctx: commands.Context):
        print('starting')
        role = ctx.guild.get_role(self.zplayer)
        zrole = ctx.guild.get_role(self.zrole)
        self.round += 1
        zmems = zrole.members
        if len(zmems) > 0:
            for z in zmems:
                await z.remove_roles(zrole)
                await z.add_roles(role)
        print(zrole)
        members = role.members
        print(members[0])
        if len(members) < 1: #if len(members) < 4
            await ctx.send("There are not enough people to play.")
            return
        else:
            length = len(members)
            print(members, length)
            num = random.randrange(0,length)
            print('members[num] - ' + str(members[num].id))
            self.zombies.append(members[num].id)
            print(members[num])
            await ctx.send(f'{members[num].mention} is the first zombie, better be nice to them.\nYou have 10 mins to convince them not to bite you.')            
            await members[num].add_roles(zrole)
            await members[num].remove_roles(role)
            while(len(self.zombies) < (len(members)/2)):
                await asyncio.sleep(600) # Wait 10 mins
                await ctx.send(f'Round {str(self.round)}, there are {str(len(self.zplayer) - len(self.zombies))} players not infected left. \n They are {str(self.make_str(ctx))}') # If the amount of Zombies is less than half the total players, there isn't the possibility for the round to end early
                self.round += 1
                self.infected = {} # Reset the infected list

            while(len(members) > 1): #go until there is only 1 player left
                
                await ctx.send("Half of the players are now zombies, there are now no limits to the game.\n Infect away, the game will end when there is only 1 person uninfected.")
                await asyncio.sleep(3)
                members = role.members
            winner = role.members[0]
            await ctx.send(f'{winner.mention} has won, congratulations!')

    def is_player(self,ctx, member):
        role = ctx.guild.get_role(self.zplayer)
        for r in role.members:
            if member.id == r.id:
                return True        
        return False
    
    def is_zombie(self, ctx, member):
        role = ctx.guild.get_role(self.zrole)
        for r in role.members:
            if member.id == r.id:
                return True        
        return False

    def clear_bites(self):
        for f in list(self.infected.keys()):
            self.infected[f] = False

    @commands.command()
    async def infect(self, ctx, member: discord.Member):
        channel = ctx.guild.get_channel(self.zchannel)
        if ctx.author.id in list(self.infected.keys()):           
            if self.infected[ctx.author.id]:
                await channel.send(f'{ctx.author.mention} you already used your infection this round.')
                return
            if self.is_zombie(ctx, ctx.author): # If their ID is in is_zombie
                if self.is_player(ctx, member): # If they have the role to play the game
                    await channel.send(f'{ctx.author.mention} infected {member.mention}')
                    self.zombies.append(member.id) # Add ID to zombies list
                    self.infected[ctx.author.id] = True #Use the member's bite for the round
                    self.infected[member.id] = True # Freshly bitten player doesn't get a bite this round
                    await member.add_roles(ctx.guild.get_role(self.zrole))
                    await member.remove_roles(ctx.guild.get_role(self.zplayer))
                else:
                    await ctx.send(f'{member.mention} is not playing the game')
        else:
            await ctx.send('f{ctx.author.mention} you are not a zombie')
            
