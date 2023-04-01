
import os
from redbot.core.bot import Red
from redbot.core import commands, checks
import asyncio
import builtins
import math

def print(*args, **kwargs):
        with open('/home/jay/redenv/terminal.log','a') as logfile:
            temp = ""
            for a in args:
                temp += str(a)
            logfile.write(temp)
            builtins.print(temp)


class ConsoleStream(commands.Cog):
    '''This cog streams the output of the console to a specified channel (set self.channel to the id)
    Be sure to run the accompanying bash script to correctly launch Redbot so that it is streaming the console output to the file.
    Set the filepath of your output in self.file_path.'''

    __author__ = "Jay_"
    __version__ = "0.0.1"

    def __init__(self, bot):
        self.bot = bot
        self.enabled = True
        self.file_path = '/home/jay/redenv/terminal.log' #file path to the log file, this needs to match up with the file path in the bash script
        self.channel = 1084000224491602010 #channel id of the channel you want the output streamed to
        self.length = 0
     


    @commands.command()
    @checks.is_owner()
    async def stream(self, ctx:commands.Context, num: int = 10):        
        self.enabled = True
        print('something')
        with open(self.file_path, 'a+') as file:
            lines = file.readlines()
            
            
            
