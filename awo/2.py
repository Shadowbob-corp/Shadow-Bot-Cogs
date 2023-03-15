import random
import asyncio
import discord
from redbot.core import commands, bank, checks
from redbot.core.config import Config
from redbot.core.utils.chat_formatting import pagify
from redbot.core.utils.predicates import MessagePredicate
import datetime

author = "Jay_"
version = "1.0.0"

class Awo(commands.Cog):
    '''Custom Wolf Pack cog made by Jay_ for Blackout.
        Wolfpack or die
        '''
    

    def __init__(self, bot):
        self.bot = bot
        self.pic = 'https://cdn.pixabay.com/photo/2022/04/01/15/41/wolf-7105065_960_720.jpg'
        self.image = ""
        self.pic_path ='C:\\Users\\justm\\redenv\\Lib\\site-packages\\redbot\\cogs\\awo\\wolf.jpg'
        self.last_awo = None
        self.payout_list = {}
        self.second_half = '. Here\'s {str(num)} {await bank.get_currency_name(ctx.guild)}.'
        self.message_list = [f'You answered the awo, I seent it',f'Shake that bussy, awoooo, awooooo.']
        self.awo_index = 0
        self.current_chain = []
        

  
    async def prune(self, ctx):

        amt = 0

        for i in self.current_chain:
            if i[1] - datetime.datetime.now() > datetime.timedelta(seconds=30):
                amt = self.payout_list[i[0].id]
                del self.payout_list[i[0].id]
                self.current_chain.remove(i)
                for k in self.payout_list.keys():
                    m = self.payout_list[k] - amt
                    self.payout_list[k] = m
                print('removed' + str(i))
                
        return amt

        
    @commands.command()
    @checks.is_owner()
    async def awolist(self, ctx):
        st = ""
        for i in self.payout_list.keys():
            st = st +'\n'+ str(self.bot.get_user(i)) + str(self.payout_list[i]) + '\n'
        if len(st) > 0:
            await ctx.send(st)
        else:
            await ctx.send('Nobody got paid yet.')
        
    @commands.(1, 30, commands.BucketType.user)
    @commands.command()
    async def awo(self, ctx):
        self.prune(ctx)
        inwolf = False
        print(str(ctx.author.roles))
        for r in ctx.author.roles:
            print(r)
            if r.id == 1048830223107506258:
                
                inwolf = True
                break
                
        if not inwolf:               
            await ctx.send(f'You ain\'t pack yet, wanna join :wolf:\nType yes to join')
            pred = MessagePredicate.yes_or_no(ctx)       
            event = "message"
            try:
                await ctx.bot.wait_for(event, check=pred, timeout=30)
            except asyncio.TimeoutError:
                print('errpor')
                with contextlib.suppress(discord.NotFound):
                    await query.delete()
                
            if pred.result:
                mem = ctx.guild.get_member(ctx.author.id)                
                await mem.add_roles(ctx.guild.get_role(1048830223107506258), reason=f"Welcome to Wolf Pack. >awo")
                await ctx.send(f'{ctx.author.mention} welcome to Wolf Pack. .awo')
                inwolf = True
        print(str(inwolf))
        current_amount = random.randrange(1000, 3500)    
        if inwolf:            
            await ctx.send(file=discord.File(self.pic_path, 'wolf.jpg'))
            await ctx.send(f'AWOOOOOOOOOoooooOOOOOOOOOOOOOO')
            self.last_awo = (ctx.author, datetime.datetime.now())
            self.current_chain.append((ctx.author, datetime.datetime.now()))
            print(str('self.current_chain[0][0]: current_amount}' + str({self.current_chain[0][0].id: current_amount})))
            self.payout_list.update({self.current_chain[0][0].id: current_amount})
            for d in range(len(self.current_chain)):
                for i in range(d):
                    
                    if self.current_chain[i][0].id in self.payout_list.keys():
                        amt = self.payout_list[self.current_chain[i][0].id] + current_amount
                        self.payout_list.update({self.current_chain[i][0].id: amt})
                   
                        
                        print(self.payout_list[self.current_chain[i][0].id])
                    else:
                        self.current_chain.append((ctx.author, datetime.datetime.now()))
                        self.payout_list.update({self.current_chain[i][0].id: current_amount})
                    await bank.deposit_credits(ctx.author, current_amount)
            string = ""
            for p in self.payout_list.keys():
                print(f'{self.bot.get_user(p).mention} got {self.payout_list[p]}\n')
                print(self.payout_list)
                await bank.deposit_credits(ctx.author, self.payout_list[p])
                string = string + str(f'{self.bot.get_user(p)} got {self.payout_list[p]}\n')
                if len(string) > 0:
                    await ctx.send(string)
           
                    
