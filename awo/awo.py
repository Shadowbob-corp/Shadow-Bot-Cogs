import random
import asyncio
import discord
from redbot.core.bot import Red
from redbot.core import commands, bank, checks, Config
from redbot.core.utils.predicates import MessagePredicate
from redbot.core.utils import AsyncIter
import contextlib
import datetime
import builtins

def print(*args, **kwargs):
        with open('/home/jay/redenv/terminal.log','a') as logfile:
            temp = ""
            for a in args:
                temp += str(a)
            logfile.write(temp)
            builtins.print(temp)


author = "Jay_"
version = "2.1.1"
#prod
class Awo(commands.Cog):
    '''Custom Wolf Pack cog made by Jay_ for Blackout.
        Wolfpack or die
        '''
    

    def __init__(self, bot: Red):
        #bot and configs
        self.bot = bot
        self.config = Config.get_conf(self, 155552245)
        self.config.register_global(entries={"hiscore":0, "public": [],  "alive": 0, 'runner': 0}, handled_string_creator=False)
        self.config.register_member(entries={"link": '' , "history":[]})
        self.init = False
        self.awostamp = None
        #store variables
        self.publicp = False
        self.listen_for = []
        self.piclist = []#default pics
        self.channel = None #channel object so I can access it for functions later
        self.member_dict = {}#{716806759687258133: {'link': 'https://www.permaculturewomen.com/wp-content/uploads/2020/11/image-107.jpeg', 'history': []}} #initialize it with 1 to prevent errors and so I dont have to keep adding myself to test
        self.picind = 0
        self.cooldown = None


        #awo high score and betting vars
        self.paying = False
        self.betlist = {}
        self.history = {}
        self.payout_list = {}
        self.alive = 0
        self.streak_start = None
        self.high_Streak = 0
        self.runner = None
        self.reset = False
        self.bet_payout = {}
        self.main = None
        self.gamble = False      
        self.lock = asyncio.Lock()
        self.nums = {'0':'<a:0_:1044940344833347584>',
            '1':'<a:1_:1044940347014397974>',
            '2':'<a:2_:1044940349077991434>',
            '3':'<a:3_:1044940350772490382>',
            '4':'<a:4_:1044940353188417586>',
            '5':'<a:5_:1044940354874511411>',
            '6':'<a:6_:1044940356707422248>',
            '7':'<a:7_:1044940358523572296>',
            '8':'<a:8_:1044940360662659092>',
            '9':'<a:9_:1044940362390704148>'}
        self._init_task = self.bot.loop.create_task(self._initialize())


    async def _initialize(self):
        #print('init')
        await self.bot.wait_until_red_ready()
        pl = await self.config.public()
        self.piclist = pl
        if self.piclist is None:
            pb = await self.config.public()
            if pb is None:
                self.piclist = ['https://i.etsystatic.com/6992381/r/il/29de6b/1224835976/il_1140xN.1224835976_p9i2.jpg', 
                                      'https://www.publicdomainpictures.net/pictures/250000/velka/wolf-howling-moon-silhouette.jpg']#default pics
                await self.config.public.set(self.piclist)
            
            print('piclist is none')
        self.alive = await self.config.alive()
        #print(self.piclist)
        self.high_Streak = await self.config.hiscore()
        await self.config.runner.set(0)
        if self.high_Streak == None:
            self.high_Streak = 0
        its = await self.config.all_members()
        ind = 0
        orderlist = []     
        #print(len(orderlist))
        for gid, data in its.items():
            #print(data)          
            #print(ind, orderlist)
            for link, history in data.items():               
                #print('link  ---------- ' + str(history['link']))
                #print('hist ' + str(history['history']))

                self.history = history['history']
                self.member_dict.update({link:{'link':history['entries']['link'], 'history': history['history']}})
                #print(self.member_dict)
            
    @commands.command()
    @checks.is_owner()
    async def resetpic(self, ctx: commands.Context):
        self.piclist.clear()
        await self.config.public.set(['https://i.etsystatic.com/6992381/r/il/29de6b/1224835976/il_1140xN.1224835976_p9i2.jpg', 
                                      'https://www.publicdomainpictures.net/pictures/250000/velka/wolf-howling-moon-silhouette.jpg'])
        self.piclist = ['https://i.etsystatic.com/6992381/r/il/29de6b/1224835976/il_1140xN.1224835976_p9i2.jpg', 
                                      'https://www.publicdomainpictures.net/pictures/250000/velka/wolf-howling-moon-silhouette.jpg']
    @commands.command()
    @checks.is_owner()
    async def awocool(self, ctx: commands.Context, member:discord.Member = None):

        if self.cooldown is not None:
            self.cooldown.command.reset_cooldown(ctx)
            await ctx.send('Reset the awo cooldown!')
        else:
            await ctx.send('There\'s nothing to reset.')

    @commands.command()
    @checks.is_owner()
    async def awopay(self, ctx):
        if len(self.payout_list) <= 0:
            await ctx.send('No awos daddy')
            return
        await self.payout(ctx)
        if self.high_Streak < len(list(self.payout_list.keys())):
            self.high_Streak = len(list(self.payout_list.keys()))
            await ctx.send(f':wolf: NEW HIGH SCORE {str(self.high_Streak)} :wolf:')
        self.payout_list.clear()
        self.betlist.clear()
        await self.config.runner.set(0)
        self.last_num = 0
        self.streak_start = None
        self.runner = None
        self.main = None
        self.reset = True          
        await ctx.send(f'It\'s my money, and I want it now!!!!!!')
        
    def format_time(self, input: str):
        print(input)
        temp = input.split('-',2)
        print(temp)
        year = temp[0]
        month = temp[1]
        temp = temp[2].split(' ',1)
        day = temp[0]
        temp = temp[1].split(':', 2)
        hour = temp[0]
        minute = temp[1]
        second = temp[2].split('.')[0]
        return datetime.datetime(int(year),int(month),int(day),int(hour),int(minute),int(second))

   
    async def emoji_num(self, num):
        m_str = ""
        if len(str(num)) >1:
            for m in str(num):
                m_str += self.nums[m] + " "                  
        else:
            m_str = self.nums[str(num)]
        return m_str


    async def payout(self, ctx):
        if self.paying:
            msg = []
            dont_pay = []
            time = None
            print('lalal')
            print(self.payout_list)
            
            if len(list(self.payout_list.keys())) > 1:
                ###################change >= to > when done debug
                for i in list(self.payout_list.keys()):
                    if self.reset:
                        #print('reset')
                        self.reset = False
                        return
                    num = random.randrange(1000,3000)
                    print('num = ' + str(num))            
                    self.betlist[i] = self.payout_list[i]
                    self.currency = await bank.get_currency_name(ctx.guild)
                                
                    self.payout_list[i] = num
                    self.betlist[i] = num                                    
                    
                    print('no history ---------- ' + str(time)) 
                        
                        
                print(self.betlist)
                lst = list(self.betlist.keys())
                for b in range(len(lst)):
                    print('b' + str(b))
                    for d in range(0,b):
                        str('d ' + str(d))
                        self.betlist[lst[d]] += self.betlist[lst[b]]
                #print(self.betlist)             
                await ctx.send(f'If you wanna gamble your earnings type .betawo <multiplier>, you have 30 secs, bet as much as you want')
                self.gamble = True            
                await asyncio.sleep(30)            
                dontpay = []
                for f in list(self.betlist.keys()):
                    history = await self.config.member(ctx.guild.get_member(f)).history()
                    if datetime.datetime.now() - self.format_time(history) > datetime.timedelta(hours = 1):
                        await bank.deposit_credits(ctx.guild.get_member(f), self.betlist[f])     
                        await self.config.member(ctx.guild.get_member(f)).history.set(str(datetime.datetime.now()))             
                    else:
                        dontpay.append(f)
                for m in list(self.payout_list.keys()):
                    if m in dontpay:
                        msg.append(f'{ctx.guild.get_member(m).mention} has already gotten paid this hour\n')
                    else:                        
                        msg.append(f'{ctx.guild.get_member(m).mention} got {str(self.betlist[m])} {self.currency}\n')          
                mes = ""
                for m in msg:
                    mes += m
                if mes != "":
                    await ctx.send(mes)
                else:
                    print(self.payout_list)
                self.gamble = False
                self.payout_list = {}
                self.betlist = {}
                await self.config.awo.clear()
                self.last_num = 0
                self.streak_start = None
                self.runner = None
                self.main = None
                self.alive = 0
                self.paying = False
                await self.config.alive.set(0)

            else:
                await ctx.send(f'{ctx.author.mention} is a lone wolf right now :\'(')
                ctx.command.reset_cooldown(ctx)
                self.gamble = False
                self.payout_list = {}
                self.betlist = {}
                await self.config.awo.clear()
                self.last_num = 0
                self.streak_start = None
                self.runner = None
                self.main = None
                self.alive = 0
                self.paying = False
                await self.config.alive.set(0)
            
            

    @commands.command()
    async def betawo(self, ctx: commands.Context, multiplier: int):
        if not self.gamble:
            return
        if not ctx.author.bot:
            amt = self.payout_list[ctx.author.id]
            rand = random.random()
            cutoff = 100/multiplier
            if rand * 100 <= cutoff:    
                self.payout_list.update({ctx.author.id: amt * multiplier})
                self.betlist.update({ctx.author.id: amt * multiplier})
                await ctx.send(f'{ctx.author.mention} won a whopping {str(amt * multiplier)} {self.currency}')
                self.last_num = 0
            else:
                self.payout_list.update({ctx.author.id: 0})
                self.betlist.update({ctx.author.id: 0})
                await ctx.send(f'{ctx.author.mention} lost it all, sorry yo.')
    

    def has_pic(self, member: discord.Member): 
        mem = self.member_dict[member.id]['link']
        return mem is not None and mem != ''

    @commands.command()
    @commands.cooldown(1, 30, commands.BucketType.member)
    async def awo(self, ctx: commands.Context):
        try:
            if self.member_dict[ctx.author.id]['link'] is None or self.member_dict[ctx.author.id]['link'] == '':
                self.member_dict[ctx.author.id]['link'] = await self.config.member(ctx.author).link()
        except:
            self.member_dict[ctx.author.id] = {'link':None, 'history':None}
        if self.cooldown is None:
            self.cooldown = ctx
        if not self.paying:        
            runn = await self.config.alive()
            #print(runn)
            member = ctx.author  
            wolfp = ctx.guild.get_role(1048830223107506258)
            user_pic = self.piclist[self.picind % len(self.piclist)]
            self.picind += 1
            wolf = None
            if wolfp in member.roles:
                wolf = wolfp
            if wolf is None:
                await ctx.send(f'You ain\'t pack, wanna join?!\n :wolf: Type yes to join :wolf:')
                pred = MessagePredicate.yes_or_no(ctx)        
                event = "message"
                try:
                    await ctx.bot.wait_for(event, check=pred, timeout=60)
                except asyncio.TimeoutError:
                    with contextlib.suppress(discord.NotFound):
                        await query.delete()
                    return
                if pred.result:
                    mem = ctx.guild.get_member(ctx.author.id)                
                    await mem.add_roles(ctx.guild.get_role(1048830223107506258), reason=f"Welcome to Wolf Pack. >awo")
                    await ctx.send(f'{ctx.author.mention} welcome to Wolf Pack. {ctx.prefix}awo')  
                    return  
            if member.id not in list(self.member_dict.keys()):
                self.member_dict[member.id] = {'link': None, 'history': None}
            run = await self.config.runner()
            if run == 0:
                await self.config.runner.set(member.id)
            if runn == 0:
                await self.config.alive.set(member.id)       
            if member.id in list(self.member_dict.keys()):
                if self.member_dict[member.id]['link'] is None:
                    self.member_dict[member.id]['link'] = await self.config.member(member).link()
                    if self.member_dict[member.id]['link'] is None:
                        print('selfmemberlist ' + str(self.member_dict[member.id]))
                        user_pic =self.piclist[self.picind % len(self.piclist)]
                        self.picind += 1
                    else:
                         user_pic = self.member_dict[member.id]['link']
                else:
                    user_pic = self.member_dict[member.id]['link']
            else:
                self.member_dict[member.id] = {'link': None, 'history': None}
                user_pic =self.piclist[self.picind % len(self.piclist)]
                await self.config.member(member).link.set(None)
                await self.config.member(member).history.set(None)
                
            #print('in_list1 ' + str(self.member_dict))
            #print(user_pic)                       #they will have to have the wolfpack role to have an entry in self.member_dict    
            numm = len(self.payout_list) + 1
            #print(numm)                          
            num = "0"
            #print(num)
            if member.id not in list(self.payout_list.keys()):

                self.payout_list.update({member.id:0})
                self.streak_start = datetime.datetime.now()
                num = await self.emoji_num(numm)
                print(self.payout_list)
                if self.has_pic(member):
                    await ctx.send(user_pic)
                    if member.id == await self.config.runner():
                        await ctx.send(f'AWOOOOOOOOOoooooOOOOOOOOOOOOOOOOOOO  {str(num)} \n{wolfp.mention}')
                        
                    else:
                        await ctx.send(f'AWOOOOOOOOOoooooOOOOOOOOOOOOOOOOOOO  {str(num)}')
                    self.picind += 1              
                else:
                    await ctx.send(self.piclist[self.picind % len(self.piclist)])
                    await ctx.send(f'AWOOOOOOOOOoooooOOOOOOOOOOOOOOOOOOO ' + str(num))              
                    self.picind += 1
            else:
                await ctx.send('We heard you the first time')
            #for when I call cmduser
            alive = await self.config.alive()
            runner = await self.config.runner()
            self.runner = runner
            print(alive)
            if alive is None or alive == 0:
                alive = member.id
            while(alive != 0 ):
                print('self.alive ' + str(self.alive))            
                if member.id == runner:
                    print('member.is = runner ' + str(runner))
                    while(alive != 0):                    
                            ##print(str(datetime.datetime.now() - self.streak_start))
                        if datetime.datetime.now() - self.streak_start > datetime.timedelta(seconds =30):                        
                            await ctx.send('The awo streak has ended. :wolf:')
                            if self.high_Streak < len(list(self.payout_list.keys())):
                                self.high_Streak = len(list(self.payout_list.keys()))
                                await self.config.hiscore.set(self.high_Streak)                           
                                await ctx.send(f':wolf: NEW HIGH SCORE {str(self.high_Streak)} :wolf:')
                            alive = 0
                            await self.config.alive.set(0)
                            await self.config.runner.set(0)
                            self.paying = True
                            await self.payout(ctx)                            
                            break    
                        await asyncio.sleep(1)
                        alive = await self.config.alive()       
                    await asyncio.sleep(1)
                    print('alive')
                    alive = await self.config.alive()
                else:
                    print('return3')
                    return
            

    @commands.command()
    @checks.is_owner()
    async def clearhistory(self, ctx: commands.Context, member: discord.Member = None):
        if member is not None:
            if member.id in list(self.member_dict.keys()):
                self.member_dict[member.id]['history'] = datetime.datetime.now() - datetime.timedelta(hours=1, seconds=1)
        else:
            if ctx.author.id in list(self.member_dict.keys()):
                self.member_dict[ctx.author.id]['history'] = datetime.datetime.now() - datetime.timedelta(hours=1, seconds=1)


    @commands.command()
    @checks.is_owner()
    async def resetawo(self, ctx: commands.Context, member: discord.Member = None):
        await self.config.clear()
        self.runner = 0
        self.alive = 0
        if member is None:
            m = await self.config.all_members()
            for g_id, data in m.items():
                for id, otherdata in data.items():
                    await self.config.member(ctx.guild.get_member(id)).clear()
        else:
            await self.config.member(member).clear()
        self.gamble = False
        self.payout_list = {}
        self.betlist = {}
        await self.config.runner.clear()
        self.last_num = 0
        self.streak_start = None
        self.main = None

        await self.config.alive.set(0)

    @commands.command()
    @checks.is_owner()
    async def printawo(self, ctx: commands.Context):
        await ctx.send(f'self.payout_list {str(self.payout_list)}')
        await ctx.send(f'member_dict {str(self.member_dict)}')
        await ctx.send(f'pic list {str(self.piclist)}')
        await ctx.send(f'streak_start {str(self.streak_start)}')
        await ctx.send(self.alive)
        t = await self.config.runner()
        await ctx.send(f'runner = {str(t)} ')
        p = await self.config.public()
        await ctx.send(p)
        mem = await self.config.all_members()
        await ctx.send(mem)





    @commands.command()
    async def awostore(self, ctx):#open store
        
        print('awostore')
        #for asynchronous running on_message.  We want to complete the proess in this function
        #self.channel is used so I can pass along the object reference
        self.channel = ctx.channel
       # #print(self.channel)           
        extra = 0
        payamt = 0

        if ctx.author.id not in list(self.member_dict.keys()):
            self.member_dict[ctx.author.id] = {'link': "", 'history': None}
        
            #print('not in list') #if the author is not in the list of cusom pictures
        payamt = 50000
        await ctx.send(f"{ctx.author.mention}, do you want to upload your own picture for 50,000 {await bank.get_currency_name(ctx.guild)}\n (yes/no)")
        pred = MessagePredicate.yes_or_no(ctx)        
        event = "message"

        try:
            await ctx.bot.wait_for(event, check=pred, timeout=60)
        except asyncio.TimeoutError:
            await ctx.send("You took too long, you have 30 seconds to upload the file or link.")
            return
        if pred.result:     
               # print('pred.result')               #add the pic to the self.public list
            await ctx.send(f"{ctx.author.mention}, do you want to make it public for 25,000 more {await bank.get_currency_name(ctx.guild)}?\n (yes/no)")
            pred = MessagePredicate.yes_or_no(ctx)
            event = "message"
            try:
                await ctx.bot.wait_for(event, check=pred, timeout=60)
            except asyncio.TimeoutError:
                await ctx.send("You took too long, you have 30 seconds to reply.")
                return
            if pred.result:
                  #  print('extra ')
                self.publicp = True
                b = await bank.get_balance(ctx.author)
                if b >= payamt + extra:                                                   
                    await bank.set_balance(ctx.author,b - (payamt + extra))
                    if ctx.author.id in list(self.member_dict.keys()):
                        history = self.member_dict[ctx.author.id]['history'] #save their history for payout                            
                        self.member_dict.update({ctx.author.id: {'link': None, 'history': history}})
                        await self.config.member(ctx.author).history.set(history)
                    else: 
                        self.member_dict[ctx.author.id] = {'link': None, 'history': None}

                    await ctx.send("Upload a file or paste a link to set your picture. You have 60 seconds")
                    self.listen_for.append(ctx.author.id)
                        
                else:
                    await ctx.send("You are a broke ass mfer, you can\'t afford it.")
            else:                
                b = await bank.get_balance(ctx.author)
                print(ctx.author.name + ' ' + str(b))
                if b >= payamt:                                                   
                    await bank.set_balance(ctx.author,b - (payamt))
                    if ctx.author.id in list(self.member_dict.keys()):
                        history = self.member_dict[ctx.author.id]['history'] #save their history for payout                            
                        self.member_dict.update({ctx.author.id: {'link': None, 'history': history}})
                        await self.config.member(ctx.author).history.set(history)
                        
                    else: 
                        self.member_dict[ctx.author.id] = {'link': None, 'history': None}
                    await ctx.send("Upload a file or paste a link to set your picture. You have 60 seconds")
                    self.listen_for.append(ctx.author.id)
                
        
                else:
                    await ctx.send("You are a broke ass mfer, you can\'t afford it.")

    def time_from_awo(self):
        if len(list(self.payout_list.keys())) == 0 and self.streak_start == None:
            #print('ffffffffffff' + str(self.streak_start))
            
            return datetime.timedelta(seconds=0)
        else:
            time = datetime.datetime.now() - self.streak_start
            #print(time)
            return time

    
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        ctx = self.channel
        added = False
        url = ""
        history = ""       
        if len(self.listen_for) > 0 and not message.author.bot:            
            url = ""
            if message.author.id in self.listen_for:                        
                if len(message.attachments) > 0:
                    if self.member_dict[message.author.id]['link'] is None or self.member_dict[message.author.id]['link'] == '':                      
                                
                        member = message.attachments[0].url
                        print(member, "member")
                        if member.find('http') > -1 or member.find('www') > -1:
                               
                            url =message.attachments[0].url  
                            print('url ------------------------------------- ' + url)                    
                            self.member_dict[message.author.id]['link'] = url
                            await self.config.member(message.author).link.set(url)
                            self.listen_for.remove(message.author.id)                        
                            await ctx.send(f"{message.author.mention} has added a custom pic!")
                        else:
                            await ctx.send("Please use a valid link.")
                            self.listen_for.remove(message.author.id) 
                            return                   
                    else:
                        ctx.send('Are you sure you want to overwrite your previous picture? (yes/no)')
                        pred = MessagePredicate.yes_or_no(ctx)        
                        event = "message"
                        try:
                            await ctx.bot.wait_for(event, check=pred, timeout=60)
                        except asyncio.TimeoutError:
                            await ctx.send("You took too long, you have 30 seconds to reply.")
                        if pred.result:
                            self.member_dict[message.author.id]['link']  = url 
                            self.piclist.append(url)
                            await self.config.member(message.author).link.set(url)
                            self.listen_for.remove(message.author.id)
                            await ctx.send(f"{message.author.mention}has added a custom pic!")
                        else:
                            print('else')
                else:
                    member = message.content
                    if member.find('http') > -1 or member.find('www') > -1:
                        
                        # print('pic' + str(message.attachments))                
                        url = str(message.content)
                        self.member_dict.update[message.author.id]['link'] = url    
                        
                        print("gggggggggggg " +self.member_dict[message.author.id]['link'])                
                        self.listen_for.remove(message.author.id)

    
                                #print('added ' + url)
                        if message.author.id in list(self.member_dict.keys()):
                            history = self.member_dict[message.author.id]['history']
    
                        if self.publicp:
                            self.piclist.append(url)
                            await self.config.public.set(self.piclist)
                        await self.config.member(message.author).link.set(url)
                        await self.config.member(message.author).history.set(history)
                            

                                ##print(h)
                        await ctx.send(f"{message.author.mention} has added a custom pic!")
                        self.member_dict[message.author.id]['link']  = url 

                        
                if url is not None:
                    await self.config.member(message.author).link.set(url)
                    if url not in self.piclist and self.publicp:
                        self.piclist.append(url)

                        await self.config.public.set(self.piclist)



                
                
















'''

        else:
            await message.channel.send("You can only have 1 picture for awo. Do you want to overwrite it for 40,000? (yes or no).")
            pred = MessagePredicate.yes_or_no(message)        
            event = "message"
            try:
                await self.bot.wait_for(event, check=pred, timeout=60)
            except asyncio.TimeoutError:
                await ctx.send("You took too long, you have 60 seconds to upload the file or link.")
            if pred.result:
                b = await bank.get_balance(message.author)
                if b >= 40000:
                    await bank.set_balance(message.author, b - 40000)

                    self.waiting.update({message.author.id: True})
                    self.listen_for.append(message.author.id)

                    #print(self.listen_for)
                    while(self.waiting[message.author.id] == True):
                        await asyncio.sleep(1)
                        #print('sleep1')
                    await message.send("added image")
                    self.listen_for.remove(message.author.id)
                else:
                    await message.send("You are a broke ass mfer, you can\'t afford it.")
    @commands.command()
    @checks.is_owner()
    async def clear_awos(self, message, member: discord.Member = None):
        
        if member is None:
            self.config.clear()
        else:
            self.config.member(member).clear()


    @commands.command()
    @checks.is_owner()
    async def printawo(self, ctx: commands.Context):
        await ctx.send(f'{str(await self.config.all_members())} \n {str(await self.config.entries())} ')
        await ctx.send(f'\n me --{str(await self.config.member(ctx.author).link())} \n {str(self.ids)} \n')

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):

        if message.author.id != self.member[0]:
            return
        if len(self.listen_for) > 0 or message.author.bot:
            url = ""
            if message.author.id in self.listen_for:    
                #print('in ---------' + str(self.listen_for)) 
                #print(message.attachments[0].url.find('http'))
                #print(message.attachments[0].url.find('www'))
            
                #print(message.attachments)           
                if len(message.attachments) == 0:
                    #print('len == 0')
                    
                    if message.attachments[0].url.find('http') > -1 or message.attachments[0].url.find('www') > -1:
                        url = message.content
                        self.member = (message.author.id, url)
                        await self.config.member(message.author).link.set(url)
                        self.listen_for.remove(message.author.id)
                    else:
                        await message.channel.send("Please use a valid link.")                        
                elif len(message.attachments) >= 1:                    
                    url = message.attachments[0].url
                    await self.config.member(message.author).link.set(url)
                    self.listen_for.remove(message.author.id)
                    #print(self.member)
                    #print(self.config.member(message.author))                    
                if self.public:        
                    k = await self.config.public()
                    #print('k-------' + str(k))
                    k.append(url)
                    await self.config.public.set(k)
                    l = await self.config.member(message.author).link()
                    await message.channel.send(l)
                    

                        

                    
                        
                    
                    
'''
                    
            
        
            
        
