import asyncio
import discord
import os
from redbot.core.bot import Red
from redbot.core import commands, checks, Config
class ConsoleStream():
    

    __author__ = "jay_"
    __version__ = "0.0.1"

    def __init__(self, bot):
        self.bot = bot
        self.enabled = True
        self.file_path = '/home/jay/redenv/terminal.log'
        self.channel = 1084000224491602010

    

    @commands.command()
    @checks.is_owner()
    async def stream(self, ctx:commands.Context):
        self.enabled = True
        end_str = ""
        

        last_utc = os.path.getmtime(self.file_path)    
        with open(self.file_path) as f:    
            len = 0
            for console in f.readlines():
                if console is None:
                    break
                if len + len(console) > 2000:
                    i = console.find('\n')
                    if len + i > 2000:
                        await ctx.send(end_str)
                        end_str = ""
                        continue
                else:
                    len += len(console)

                    end_str += console


            self.last_utc = os.path.getmtime(self.file_path)
            f.close()

            await asyncio.sleep(2)
            
        while(self.enabled):                
            with open(self.file_path) as f:    
                
                for console in f.readlines():
                    end_str += console + '\n'
                last_version = os.path.getmtime(self.file_path)
                f.close()

                await asyncio.sleep(5)


    @commands.command()
    @checks.is_owner()
    async def stopstream(self, ctx: commands.Context):
        self.enabled = False
            
