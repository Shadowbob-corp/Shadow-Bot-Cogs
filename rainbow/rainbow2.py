import random
import asyncio
import discord
from redbot.core import commands, bank, checks
from redbot.core.config import Config
from redbot.core.utils import AsyncIter
from redbot.core.utils.chat_formatting import pagify
from redbot.core.utils.predicates import MessagePredicate
import datetime


author = "Jay_"
version = "1.0.0"

class Rainbow(commands.Cog):
    '''Make yo peoples gay and fabulous
        written by Jay_'''
    

    def __init__(self, bot):
        self.bot = bot

        #these to the roles you have setup in the server
        self.roles = {'red' :1085989948236251219,
            'redorange': 1085990443889733663,
            'orange':1085990177018740767,
            'orange/yellow': 1085990796970430484,
            'yellow':1085990282056716359,
            'yellow/green':1085991058791485521,
            'green':1085990799394738277,
            'green/blue': 1085990803123486810,
            'blue':1085990805686202480,
            'blurple':1085990808089530438,
            'indigo':1085990810094424184,
            'violet':1085991897945870356,
            'pink': 1085992135288946728,
            'pinker':1085992190305640499}

        
        self.userlist = {716806759687258133: 'red'}
        self.current = [716806759687258133]
                                        
                        
        self.config = Config.get_conf(self,  15975365421)
        self.config.register_member(**default_member)
        

    @checks.is_owner()
    @commands.command()
    async def setrainbow(self, ctx, user: discord.User):
        if user.id in self.current:
            await ctx.send(f'{user.mention} is already gay.')
            return
        self.current.append( user.id)
        self.userlist.update({user.id: 'red'})
        self.config.register_member({user.id: {
                                                'theme': 'rainbow'
                                                'color':'red'
        }})
        await ctx.send(f'{user.mention} is now gay')
        mem = ctx.guild.get_member(user.id)
        for f in self.roles.values():
            await mem.add_roles(ctx.guild.get_role(f), reason=f"rainbow fag shit")

    @checks.is_owner()
    @commands.command()
    async def removerainbow(self, ctx, user: discord.User):
        if user.id in self.current:
            for r in self.roles.values():
                await ctx.guild.get_member(user.id).remove_roles(ctx.guild.get_role(r))

            self.current.remove(user.id)
            self.userlist.pop(user.id)
            await ctx.send(f'{user.mention} is not rainbow.')
        else:
            await ctx.send(f'{user.mention} doesn\'t have the role')

    @checks.is_owner()
    @commands.command()
    async def listrainbow(self, ctx: commands.Context):
        message = ""
        for f in self.current:
            use = ctx.guild.get_member(f)
            message += f'{use.mention}\n'
        await ctx.send(message)

    @commands.command()
    async def unrainbow(self,ctx):
        if ctx.author.id in self.current:
            self.current.remove(ctx.author.id)
            for r in list(self.roles.keys()):
                print(r)
                await ctx.guild.get_member(ctx.author.id).remove_roles(ctx.guild.get_role(self.roles[r]))
            await ctx.send(f'{ctx.author.mention}\'s time in rainbow gang is up.')
        else:
            for r in list(self.roles.keys()):
                await ctx.guild.get_member(ctx.author.id).remove_roles(ctx.guild.get_role(self.roles[r]))   
            
    def cog_unload(self):
        self.bot.loop.create_task(self.session.close())


    async def refresh_user(self, ctx, user):
        for f in self.roles.values():
                await ctx.guild.get_member(user).add_roles(ctx.guild.get_role(f), reason=f"rainbow fag shit")

    @commands.command()
    async def refreshuser(self, ctx, user: discord.User):
        await self.refresh_user(ctx, user.id)
        self.userlist.update({user.id: 'red'})
        
        await ctx.send(f'{user.mention} has been refreshed')

    @commands.Cog.listener()
    async def on_message(self, message):
        if self.current is None:
            return


        mem = message.author
        if mem.id in self.current:
            for f in self.roles.values():               
                
                if f in mem.roles:
                    role = r
                    print(str(r) + ' ------------------')
                    break
                 
                
            clist = list(self.roles.keys())
            for i in range(len(clist)):
                if self.userlist[message.author.id] == clist[i]:                    
                    if len(clist) == i + 1:
                        self.color = clist[0]
                        for f in self.roles.values():
                            await mem.add_roles(message.guild.get_role(f), reason=f"rainbow fag shit")
                        self.userlist.update({message.author.id: 'red'})

                        print('c[0] ' + clist[0])
                        break
                    else:
                        if role is not None:
                            await mem.remove_roles(r)
                            colo = clist[i+1]
                            self.userlist.update({message.author.id: colo})
                            print('c[i+1] ' + clist[i+1])
                            break
            
            
            

        



