
import discord
from redbot.core import commands, bank, checks
from redbot.core.config import Config
from redbot.core.utils import AsyncIter
from redbot.core.utils.chat_formatting import pagify
from redbot.core.utils.predicates import MessagePredicate
from colour import Color


author = "Jay_"
version = "1.0.0"

class Rainbow(commands.Cog):
    '''Make yo peoples gay and fabulous
        written by Jay_'''
    

    def __init__(self, bot):
        self.bot = bot
        self.individuals = {}
        self.color_interval = 5000
        self.color_list = {}
        self.patterns = {'catlady': {'pattern':[],
                                    'users':[]},
                        'rainbow': {'pattern':[Color('red').hex, Color('orange').hex, Color('yellow').hex, Color('green').hex, Color('blue').hex, Color('indigo'), Color('violet').hex],
                                    'users':[]}}



    def color_util(self, ctx: commands.Context, pattern = 'rainbow'):
        tmp = []
        if pattern in list(self.patterns.keys()):
            for i in self.patternns[pattern]:
                tmp.append(Color(i))
            return tmp
        else:            
            return None

    def hex_math(self, user):        
        us = str(user)
        if us in list(self.individuals.keys()):
            print('us ---- ' + str(us))         
            temp_color = self.individuals[us]
            print('-------------------------' + str(self.individuals[us]))
            tcol = self.color_util()
            prnt= tcol + int(str(self.individuals[us]), 16)
            print(str(tcol) + ' vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv')
            tcol += self.color_interval
            if tcol >= 16777215:
                news = tcol - 16677215
            else:
                news = tcol
            h_val = hex(news)

            print('hval ' + str(h_val))
            return tcol
        else:

            us = user
            self.individuals.update({us: 0})
                    
            return 0

    def is_rainbow(self, user):

        if str(user) in list(self.individuals.keys()):
            return True
        else:
            return False

    @commands.command()
    @checks.is_owner()
    async def setrainbow(self,ctx, user):
        uid = user[2:-1]
        print('uid ' + str(uid))
        if not self.is_rainbow(uid):           
            self.individuals.update({uid:'000000'})
            names = ctx.guild.get_member(int(uid))
            
            colour = int('000000', 16)
            role = await ctx.guild.create_role(name=names.name, )
            await role.edit(color=discord.Colour(colour))
            position = {role: self.get_position(ctx)}
            await ctx.guild.edit_role_positions(positions = position)
        

    @commands.command()
    async def rainbowcolors(self,ctx, *args):
        templist = []
        for a in args:
            templist.append(a)
        self.color_list.update({ctx.author: {
                                        'data':templist,
                                        'index': 0}})
        print(self.color)

    @commands.command()
    @checks.is_owner()
    async def testy(self, user: discord.User):
        print(self.individuals)
        print(self.color_interval)



        

    def get_position(self, ctx):
        role_id = 1064451271295258624
        roles = ctx.guild.roles
        for i in range(len(roles)):
            if roles[i].id == role_id:
                print('get position ' + str(roles[i]))
                return i
        return -1

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):

        if str(message.author.id) in list(self.individuals.keys()):

            nval = hex(self.hex_math(str(message.author.id)))
            print(nval + ' nval')
            print(self.individuals)
            self.individuals[str(message.author.id)] = nval
            c = self.individuals[str(message.author.id)]
            
            usr = message.author
            uid = message.author.id
            role = None
            for f in usr.roles:
                print('f - '  + str(f))
                if f.name == usr.name:
                    print('role = f ' + f.name)
                    role = f
            if role is not None:
                if str(message.author.id) in list(self.color_list.keys()):
                    num = self.color_list[message.author.id]['index']
                    if num + 1 > len(self.color_list[message.author.id]['data']):
                        self.color_list[message.author.id]['index'] = 0                
                v = self.hex_math(uid)                
                new_val =self.individuals[str(uid)]
                nval = int(new_val, 16)                
                nval += self.color_interval
                self.individuals.update({str(uid): hex(nval)})
                color = int(str(hex(nval)), 16)
                print(str(color) + ' color')
                if color > 16777215:
                    color -= 16777215
                print('color ' + str(color))
                await role.edit(colour=discord.Colour(color))
            else:
                if not self.is_rainbow(uid):           
                    self.iandividuals.update({uid:'FFFFFF'})
                    names = message.guild.get_member(int(uid))
                    print(names.name + 'kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk')
                    colour = int('FFFFFF', 16)
                    role = await message.guild.create_role(name=names.name)
                    await role.edit(color=discord.Colour(colour))
                    position = {role: self.get_position(message)}
                    await message.guild.edit_role_positions(positions = position)
                    uid = message.author.id
                    v = self.hex_math(uid)
                    print(v)
                    new_val = 000000
                    nval = int(str(nval), 16)
                    print(nval)                
                    nval += self.color_interval
                    self.individuals.update({str(uid): nval})

            

                
                






            
        

        
            

        
            

        



