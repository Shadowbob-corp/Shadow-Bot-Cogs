import random
import asyncio
import discord
from redbot.core.bot import Red
from redbot.core import commands, bank, checks, Config
from redbot.core.utils.predicates import MessagePredicate

import datetime


author = "Jay_"
version = "2.1.0"
#prod
class Awo(commands.Cog):
    '''Custom Wolf Pack cog made by Jay_ for Blackout.
        Wolfpack or die
        '''
    

    def __init__(self, bot: Red):
        self.bot = bot
        self.config = Config.get_conf(self, 155552245)
        self.config.register_global(entries={"hiscore":0, "custom": 0, "public": ['https://i.etsystatic.com/6992381/r/il/29de6b/1224835976/il_1140xN.1224835976_p9i2.jpg','https://www.publicdomainpictures.net/pictures/250000/velka/wolf-howling-moon-silhouette.jpg']}, handled_string_creator=False)
        self.config.register_member(entries={"link": ''})

        self.picind = 0
        self.betlist = {}
        self.cur_streak = []
        self.custom = {}
        self.payout_list = {}
        self.history = {}
        self.alive = True
        self.streak_start = None
        self.high_Streak = 0
        self.runner = None
        self.reset = False
        self.bet_payout = {}
        self.main = None
        self.gamble = False
        self.currency = ""
        self.listen_for = []
        self.waiting = {}  
        self.last_num = 0
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





    @commands.command()
    @checks.is_owner()
    async def awopay(self, ctx):
        if self.runner == None:
            await ctx.send('No awos daddy')
            return
        await self.payout(ctx)
        if self.high_Streak < len(self.cur_streak):
            self.high_Streak = len(self.cur_streak)
            await ctx.send(f':wolf: NEW HIGH SCORE {str(self.high_Streak)} :wolf:')
        self.cur_streak.clear()
        self.payout_list.clear()
        self.betlist.clear()
        self.last_num = 0
        self.streak_start = None
        self.runner = None
        self.main = None
        self.reset = True     
         
        await ctx.send(f'It\'s my money, and I want it now!!!!!!')
        
    @commands.command()
    @checks.is_owner()
    async def awoolist(self, ctx):
        st = ""
        for i in self.payout_list.keys():
            st = st +'\n'+ str(self.bot.get_user(i)) + str(self.payout_list[i]) + '\n'
        if len(st) > 0:
            await ctx.send(st)
        else:
            await ctx.send('Nobody got paid yet.')

    def time_from_start(self, start = datetime.datetime.now()):
        diff = start - self.streak_start
        return diff.seconds

   
    async def emoji_num(self, num):
        m_str = ""
        if len(str(num)) >1:
            for m in str(num):
                m_str += self.nums[m] + " "                  
        else:
            m_str = self.nums[str(num)]
        return m_str

    def time_str(self, datetim):
        return f'{str(datetim.hour)}:{str(datetim.minute)}:{str(datetim.second)}  MST'

    async def payout(self, ctx):
        msg = []
        if len(self.cur_streak) > 1: ###################change >= to > when done debug
            for i in range(len(self.cur_streak)):
                if self.reset:
                    self.reset = False
                    return
                num = random.randrange(1000,3000)  
                print('num = ' + str(num))
                if i == 0:
                    self.payout_list.update({self.cur_streak[i].id: num})
                else:                   
                    for j in range(i+1):
                        t_num = self.payout_list[self.cur_streak[j].id] + num
                        print('t_num' + str(t_num))
                        self.payout_list.update({self.cur_streak[j].id: t_num})                
            self.currency = await bank.get_currency_name(ctx.guild)
            ind = 0
            for f in self.cur_streak:
                if self.reset:
                    self.reset = False
                    return
                inlist = False
                if self.history.get(f.id) is not None:                
                    if datetime.datetime.now() - self.history.get(f.id) < datetime.timedelta(hours=1):
                        msg.append(f'{f.mention} can get paid again at {str(self.time_str(self.history[f.id] + datetime.timedelta(hours=1)))}.\n')
                        continue               
                self.betlist.update({f.id: self.payout_list[f.id]})
                self.history.update({f.id: datetime.datetime.now()})
            await ctx.send(f'If you wanna gamble your earnings type .betawo <multiplier>, you have 30 secs, bet as much as you want')
            self.gamble = True
            await asyncio.sleep(30)            
            for m in self.cur_streak:
                msg.append(f'{m.mention} got {str(self.betlist[m.id])} {self.currency}\n')
            for f in list(self.betlist.keys()):
                await bank.deposit_credits(ctx.guild.get_member(f), self.betlist[f])                    
            mes = ""
            for m in msg:
                mes += m

            if mes != "":
                await ctx.send(mes)
            else:
                print(self.payout_list)
                print(self.cur_streak)
                print(self.runner)
                print(str(self.main) + ' -main')
            self.gamble = False
            self.cur_streak.clear()
            self.payout_list.clear()
            self.last_num = 0
            self.streak_start = None
            self.runner = None
            self.main = None

        else:
            await ctx.send(f'{ctx.author.mention} is a lone wolf right now :\'(')
            self.gamble = False
            self.cur_streak.clear()
            self.payout_list.clear()
            self.last_num = 0
            self.streak_start = None
            self.runner = None
            self.main = None

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

    def in_list(self, user):
        for f in self.cur_streak:
            if user.id == f.id:
                return True
        return False

    async def add_data(self, data=None):
        if data is not None:
            l = await self.config.entries()
            l.update(data)
            await self.config.entries.set(l)

        
    async def awoo(self, ctx):    
        print(await self.config.entries())
        ids = []
        user = 0
        for c in list(self.custom.keys()):
            ids.append(c)
        if ctx.author.id in ids:
            if self.custom[c] is not None:
                mem = await self.config.all_members()
                for p in mem:
                    mem_id =  await self.config.member(ctx.author).link()
                    self.custom.update({ctx.author.id: mem_id})
                    
                    print('yyyyyyyyyyy' +str(self.custom))
        else:
            self.custom.update({ctx.author.id: None})
        
        rid = []
        
        for i in ctx.author.roles:
            rid.append(i.id)            
        if 1048830223107506258 in rid:
            ind = self.picind 
            pic = await self.config.public()

            num = await self.emoji_num(len(self.payout_list)+1)
            if self.runner is None:                
                wolfg = ctx.guild.get_role(1048830223107506258)
                print(self.custom)
                mem = self.custom[ctx.author.id]
                print('mem ---- ' +str(mem))
                if mem is not None:
                    await ctx.send(mem)
                else:
                    print(str(pic) +" "+ str(ind))
                    await ctx.send(pic[ind % len(pic)])                
                self.picind += 1            
                
                await ctx.send(f'AWOOOOOOOOOoooooOOOOOOOOOOOOOOOOOOO ' + str(num) + '\n' + str(wolfg.mention)) 
                self.last_num = num
            
                if self.reset:
                    self.reset = False
                    return
                #print('self.main is true')
                self.main=ctx.author.id
                self.runner = ctx.author
                if self.streak_start is None:
                   # print('self.streak_start')
                    self.streak_start = datetime.datetime.now()

                self.cur_streak.append(ctx.author)
                self.payout_list.update({ctx.author.id: 0})    
       

                while(self.alive):
                    if self.reset:
                        self.reset = False
                        return
                    if datetime.datetime.now() - self.streak_start > datetime.timedelta(seconds = 30):                        
                        await ctx.send('The awo streak has ended. :wolf:')
                        self.config.entries()
                        print(await self.config.entries())
                        if int(await self.config.entries.hiscore()) < len(self.payout_list):
                            self.high_Streak = len(self.payout_list)

                            await self.config.entries.hiscore.set(self.high_Streak)                           
                            print("hiscore" + str(await self.config.entries.hiscore.set(self.high_Streak)))
                            await ctx.send(f':wolf: NEW HIGH SCORE {str(self.high_Streak)} :wolf:')
                        await self.payout(ctx)
                        self.cur_streak.clear()
                        self.payout_list.clear()
                        self.last_num = 0
                        self.streak_start = None
                        self.runner = None
                        self.main = None
                        break
                    await asyncio.sleep(1)
            else:
                if self.reset:
                    self.reset = False
                    return
                
                if not self.in_list(ctx.author):
                    st = await self.emoji_num(len(self.cur_streak) + 1)
                    await ctx.send(self.pics[self.picind % len(self.pics)])                    
                    self.picind += 1
                    await ctx.send(f'AWOOOOOOOOOoooooOOOOOOOOOOOOOOOOOOO ' + str(st))
                    self.streak_start = datetime.datetime.now()
                    self.cur_streak.append(ctx.author) 
                    self.payout_list.update({ctx.author.id: 0}) 
                    return 
                else:
                    await ctx.send(self.pics[self.picind % len(self.pics)])                    
                    self.picind += 1                      
                    await ctx.send(f'AWOOOOOOOOOoooooOOOOOOOOOOOOOOOOOOO ' + str(num))
        else:
            await ctx.send(f'You ain\'t pack, wanna join?!\n :wolf: Type yes to join :wolf:')
            pred = MessagePredicate.yes_or_no(ctx)        
            event = "message"
            try:
                await ctx.bot.wait_for(event, check=pred, timeout=30)
            except asyncio.TimeoutError:
                with contextlib.suppress(discord.NotFound):
                    await query.delete()
                return
            if pred.result:
                mem = ctx.guild.get_member(ctx.author.id)                
                await mem.add_roles(ctx.guild.get_role(1048830223107506258), reason=f"Welcome to Wolf Pack. >awo")
                await ctx.send(f'{ctx.author.mention} welcome to Wolf Pack. {ctx.prefix}awo')



   # @commands.cooldown(1, 27, commands.BucketType.user)
    @commands.command()
    async def awo(self, ctx):
        if self.alive:
            
            await self.awoo(ctx)                           
        else:
            self.cur_streak = []
            self.payout_list = {}
            self.alive = True
            self.last_num = 0
            self.streak_start = None
            self.runner = None
            self.main = None

    @commands.command()
    async def resetawo(self, ctx: commands.Context, member: discord.Member = None):
        mem = ctx.author
        if member == None:
            await ctx.send("Clear your awo picture, it can not be undone? (yes/no)")
            
            pred = MessagePredicate.yes_or_no(ctx)        
            event = "message"
            try:
                await ctx.bot.wait_for(event, check=pred, timeout=60)
            except asyncio.TimeoutError:
                await ctx.send("You took too long, you have 60 seconds to answer.")
            if pred.result:
                await self.config.member(mem).clear()
                if mem.id in list(self.custom.keys()):
                    self.custom.pop(mem.id)
                if mem.id in self.listen_for:
                    self.listen_for.remove(mem.id)
        elif ctx.bot.is_owner(ctx.author):
            await ctx.send("Clear your awo picture, it can not be undone? (yes/no)")
            mem = member
            pred = MessagePredicate.yes_or_no(ctx)        
            event = "message"
            try:
                await ctx.bot.wait_for(event, check=pred, timeout=60)
            except asyncio.TimeoutError:
                await ctx.send("You took too long, you have 60 seconds to answer.")
            if pred.result:
                await self.config.member(mem).clear()
                if mem.id in list(self.custom.keys()):
                    self.custom.pop(mem.id)
                if mem.id in self.listen_for:
                    self.listen_for.remove(mem.id)
        else:
            await ctx.send("Some weird ass error")

    @commands.command()
    async def awostore(self, ctx):
        ids = []
        mem = await self.config.all_members()
        for p in mem:
            mem_id =  await self.config.member(ctx.author).link()
            if mem_id is not None:
                self.custom.update({ctx.author.id: str(mem_id)})
                print('yyyyyyyyyyy' +str(self.custom))
        if len(list(self.custom.keys())) == 0:
            print("not 0")
            
        for c in list(self.custom.keys()):
            ids.append(c)
            print("id - " + str(c))
        if ctx.author.id not in ids:
            print("not in ids")

        
            await ctx.send(f"{ctx.author.mention}, do you want to upload your own picture for 50,000 {await bank.get_currency_name(ctx.guild)} (type yes then post or link)")
            pred = MessagePredicate.yes_or_no(ctx)        
            event = "message"
            try:
                await ctx.bot.wait_for(event, check=pred, timeout=60)
            except asyncio.TimeoutError:
                await ctx.send("You took too long, you have 60 seconds to upload the file or link.")
            if pred.result:
                b = await bank.get_balance(ctx.author)
                if b >= 50000:
                    await bank.set_balance(ctx.author, b - 50000)
                    self.waiting.update({ctx.author.id: True})
                    self.listen_for.append(ctx.author.id)
                    print(self.listen_for)
                    while(self.waiting[ctx.author.id] == True):
                        await asyncio.sleep(1)
                    await ctx.send("added image")
                    self.listen_for.remove(ctx.author.id)
                else:
                    await ctx.send("You are a broke ass mfer, you can\'t afford it.")
        else:
            await ctx.send("You can only have 1 picture for awo. Do you want to overwrite it for 40,000? (yes or no).")
            pred = MessagePredicate.yes_or_no(ctx)        
            event = "message"
            try:
                await ctx.bot.wait_for(event, check=pred, timeout=60)
            except asyncio.TimeoutError:
                await ctx.send("You took too long, you have 60 seconds to upload the file or link.")
            if pred.result:
                b = await bank.get_balance(ctx.author)
                if b >= 40000:
                    await bank.set_balance(ctx.author, b - 40000)

                    self.waiting.update({ctx.author.id: True})
                    self.listen_for.append(ctx.author.id)
                    print(self.listen_for)
                    while(self.waiting[ctx.author.id] == True):
                        await asyncio.sleep(1)
                    await ctx.send("added image")
                    self.listen_for.remove(ctx.author.id)
                else:
                    await ctx.send("You are a broke ass mfer, you can\'t afford it.")
                

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if len(self.listen_for) > 0 or message.author.bot:
            url = ""
            if message.author.id in self.listen_for:                
                if len(message.attachments) == 0:
                    if message.content.find('http') > -1 or message.content.find('www') > -1:
                        url = message.content
                    else:
                        await message.send("Please use a valid link.")
                        
                elif len(message.attachments) == 1:
                    url = message.attachments[0].url
                else:
                    await message.guild.send("Please only upload 1 image.")
                    self.waiting[message.author.id] = False
                    return
                self.waiting[message.author.id] = False
                await self.config.member(message.author).link.set(url)
                self.custom.update({message.author.id: url})
                print('mem - ' +str(await self.config.member(message.author).link()))
                await message.channel.send(url)
                    

                        

                    
                        
                    
                    

                    
            
        
            
        
