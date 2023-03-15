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
        self.roles = {'red' :1059593340032659456,
            'orange':1059593689816645713,
            'yellow':1059593669843357737,
            'green':1059593811505987734,
            'blue':1059594036035465276,
            'indigo':1059594131640418324,
            'violet':1059594418367250564,
            'pink': 1061330463609860166,
            'pinker':1061512886616334346,
            'invisible':1041909802508496947,
            'random':1061777626286526555}
        self.random = True
        
        self.userlist = {716806759687258133: 'red'}
        self.current = [716806759687258133]
        default_member= {716806759687258133: {
                                            "theme": "rainbow",
                                            "color": "red",
                                            "random":True}}
                                        
                        
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
        if self.random:
            roles = []
            roles.count()
            if message.author.roles.count(self.roles['random'])
        role = None
        mem = message.guild.get_member(message.author.id)
        if message.author.id in self.current:
            for r in message.author.roles:
                for f in self.roles.values():
                    
                    if r.id == f:
                        role = r
                        print(str(r) + ' ------------------')
                        break
                if role is not None:
                    break                           
                
            clist = list(self.roles.keys())
            for i in range(len(clist)):
                if self.userlist[message.author.id] == clist[i]:                    
                    if len(clist) == i + 1:
                        self.color = clist[0]
                        for f in self.roles.values():
                            await mem.add_roles(message.guild.get_role(f), reason=f"rainbow fag shit")
                        self.userlist.update({message.author.id: 'red'})
                        self.config.
                        print('c[0] ' + clist[0])
                        break
                    else:
                        if role is not None:
                            await mem.remove_roles(message.guild.get_role(self.roles[self.userlist[message.author.id]]))
                            colo = clist[i+1]
                            self.userlist.update({message.author.id: colo})
                            print('c[i+1] ' + clist[i+1])
                            break
            
            
            

        



