import random
import asyncio
import discord
from redbot.core import commands, bank, checks
from redbot.core.config import Config
from redbot.core.utils import AsyncIter
from redbot.core.utils.chat_formatting import pagify
from redbot.core.utils.predicates import MessagePredicate
import datetime
import builtins

def print(*args, **kwargs):
        with open('/home/jay/redenv/terminal.log','a') as logfile:
            temp = ""
            for a in args:
                temp += str(a)
            logfile.write(temp)
        builtins.print(*args, **kwargs)

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
        self.random = True
        
        self.userlist = {716806759687258133: 'red'}
        self.current = [716806759687258133]

                                        
        self.colors = {'red' : 'FF0000',
            'r2':'FF3900',
            'orange':'FF8000',
            'o1':'F9B606',
            'yellow':'F0FF00',
            'y1':'F0FF00',
            'g':'92FF00',
            'green':'14FF00',
            'gb':'00FF90',
            'b':'00C2FF',
            'blue':'0090FF',
            'b1':'3B00FF',
            'indigo':'6800FF',
            'violet':'B800FF',
            'vp':'F400FF',
            'pink': 'FF00F8',
            'pinker':'FF00B5'}
        self.color_list = list(self.colors.keys())

    async def find_user_role(self, ctx:commands.Context, user:discord.Member):
        rl = ctx.guild.fetch_roles()
        for f in rl:
            if f.name == user.nick:
                self.userlist.update({user.id: f.id})
                print('f.id = ' + str(f.id))
                return  f.id
        return 0

    

    @checks.is_owner()
    @commands.command()
    async def setrainbow(self, ctx:commands.Context, user: discord.User):
        u = ctx.guild.get_member(user.id)
        if u.id in self.current:
            await ctx.send(f'{user.mention} is already gay.')
            return
        self.current.append( u.id)

        if user.id not in list(self.color_index.keys()):
            r = self.find_user_role(ctx, u)
            rle = await ctx.guild.get_role(r)
            print(rle.name)
            if  rle is  None:
                colour = int(self.colors['red'], 16)
                role = await ctx.guild.create_role(name = u.name)
                nrole = await ctx.guild.edit_role_positions(position={rle: 100})
                print('nrole '  + str(nrole) )
            else:
                nrole = rle

            
            self.userlist[u.id] = nrole
            self.color_index.update({u.id: rle})
            print('userlist ' +str( self.color_index[u.id]) )
            self.color_index[u.id] = 0
        await ctx.send(f'{u.mention} is now gay')
        print(u)
        mem = ctx.guild.get_member(u.id)
        print('mem ' + str(mem ))
        tt = self.find_user_role(ctx, u)
        print(tt)
        r = ctx.guild.get_role(tt)
        


        await mem.add_roles(r, reason=f"rainbow fag shit")

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
            await ctx.send('You ain\' rainbow gang chill')      
            
    def cog_unload(self):
        self.bot.loop.create_task(self.session.close())


    async def refresh_user(self, ctx, user):
        for f in self.roles.values():
                ctx.guild.get_member(user).add_roles(ctx.guild.get_role(f), reason=f"rainbow fag shit")

    @commands.command()
    async def refreshuser(self, ctx, user: discord.User):
        await self.refresh_user(ctx, user.id)
        self.userlist.update({user.id: 'red'})
        
        await ctx.send(f'{user.mention} has been refreshed')


    @commands.command()
    async def unrandom(self, ctx):
        self.random = not self.random
        for p in self.current:
            mem = ctx.guild.get_member(ctx.author.id)
            if 1061777626286526555 in self.roles:
                 await mem.remove_roles(ctx.guild.get_role(1061777626286526555))

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if self.current is None:
            return
        if self.random:
            if message.author.id in self.current:
                if message.author.id not in list(self.color_index.keys()):
                    print('adding ' + str(message.author.name))
                    self.color_index[message.author.id] = 0
                else:
                    self.color_index[message.author.id] += 1
                    p = self.color_index[message.author.id] % len(self.color_index)-1
                    print(p)
                print(self.color_index)
                if message.author.id in list(self.color_index.keys()):
                    colour = int(self.colors['red'], 16)
                    role = await message.guild.create_role(name = message.author.name,  color=discord.Colour(colour))
                    nrole = await role.edit(position=102)
                    self.userlist.update({message.author.id: nrole})
                    gm = message.guild.get_member(message.author.id)
                    print(gm)
                    await  gm.add_roles(self.userlist[message.author.id], reason=f"rainbow fag shit")
                else:
                    print('color ' +str(self.userlist[message.author.id]) )
                    temp = list(self.colors.values())
                    color = int(temp[self.color_index[message.author.id]], 16)
                    message.guild.get_role(self.find_user_role(message.guild, message.author)).edit(colour=color)

                
                    return
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
                        await mem.add_roles(message.guild.get_role(self.userlist[message.author.id]), reason=f"rainbow fag shit")
                        self.userlist.update({message.author.id: 'red'})
                        print('c[0] ' + clist[0])
                        break
                    else:
                        if role is not None:
                            await mem.remove_roles(message.guild.get_role(self.roles[self.userlist[message.author.id]]))
                            colo = clist[i+1]
                            self.userlist.update({message.author.id: colo})
                            print('c[i+1] ' + clist[i+1])
                            break
            
            
            

        



