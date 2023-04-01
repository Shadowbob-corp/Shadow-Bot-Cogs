import asyncio
import datetime
import os

import discord
from redbot.core import Config, commands, checks


from redbot.core.bot import Red



class Dev(commands.Cog):
    
    def __init__(self,bot:Red):

        self.bot = bot
        self.mod_dict = {} #store the last modified date for each fileS
        self._init_task = self.bot.loop.create_task(self._initialize())
        self.cogpath = '/home/jay/redenv/lib/python3.9/site-packages/redbot/cogs/'
        self.context = None
        self.active = False

    async def _initialize(self, ):
        dirs = os.listdir(self.cogpath)
        #print(dirs)
        for d in dirs:
            #print('d ---- ' + str(d))
            tempdir = os.listdir(self.cogpath + d)
            print(d)
           
            try:
                num_dir = os.listdir(self.cogpath + d)
                for f in num_dir:
                    #print('num_dir 9999999999999999999999999 ' + str(num_dir) )
                    looping = True
                    #print(d)
                    print(f)
                    if f[:-3] == '.py':
                        self.mod_dict[f] = os.path.getmtime(f)
                        print('----------------------------------fff ' + str(f))
                    
                    

               # print(self.mod_dict)
            except Exception as e:
                print('aaahhhhhhhhhhhhhhhh' + str(e))
            
    @commands.command()
    @checks.is_owner()
    async def devmode(self, ctx: commands.Context):
        await ctx.send("Activating devmode.")
        if self.active == False:
            self.active = True
        if self.context != ctx:
            self.context = ctx
        while(self.active):
            for c in self.mod_dict.keys():
                print('c - ' + str(c))
                compare = os.path.getmtime(c)
                print('compare ----------------------- '+str(compare))
                if compare != self.mod_dict[c]: 

                    self.mod_dict[c] = compare
                    #print(compare)
                    await ctx.send('loaded ' + c)
            await asyncio.sleep(2)
            
            print('@@@@@@@@@@@@@@@@' + str(self.mod_dict))
        
    @commands.command() 
    @checks.is_owner() 
    async def devoff(self, ctx):
        self.active = False
                    
                    