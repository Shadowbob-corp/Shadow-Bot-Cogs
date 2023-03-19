
import os
import math
from redbot.core.bot import Red
from redbot.core import commands, checks, Config
import asyncio
class ConsoleStream(commands.Cog):
    

    __author__ = "jay_"
    __version__ = "0.0.1"

    def __init__(self, bot):
        self.bot = bot
        self.enabled = True
        self.file_path = '/home/jay/redenv/terminal.log'
        self.channel = 1084000224491602010
        self._init_task = self.bot.loop.create_task(self._initialize())
        self.config = Config.get_conf(self, 155552245)
        self.config.register_global(entries={'length':0}, handled_string_creator=False)
        self.length = 0

    async def _initialize(self):
        
        """ Should only ever be a task """
        await self.bot.wait_until_red_ready()
        self.length = await self.config.length()

    @commands.command()
    @checks.is_owner()
    async def stream(self, ctx:commands.Context):
        
        self.enabled = True

        last_utc = os.path.getmtime(self.file_path)
        end_str = []
        lenf = 0
        ind = 0
        chan = ctx.guild.get_channel(self.channel)
        with open(self.file_path, 'r') as f:  
            for r in f.readlines():
                if r not in end_str:
                    try:
                        if r is None:                           
                            await chan.send('-\n')
                        else:
                            await chan.send(r)
                    except:
                        await chan.send('-\n')
                    await asyncio.sleep(1)
                    end_str.append(r)
                    ind += 1               
            while(self.enabled):
                if os.path.getmtime(self.file_path) != last_utc:
                    nind = 0
                    for fi in f.readlines():
                        if fi not in end_str:
                            await chan.send(fi)                    
                last_utc = os.path.getmtime(self.file_path)
                await asyncio.sleep(3)

            f.close()

            
            
      

    @commands.command()
    @checks.is_owner()
    async def stopstream(self, ctx: commands.Context):
        self.enabled = False
            
