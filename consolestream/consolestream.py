
import os

from redbot.core import commands, checks
import asyncio
import builtins

def print(*args, **kwargs):
        with open('/home/jay/redenv/terminal.log','a') as logfile:
            temp = ""
            for a in args:
                temp += str(a)
            logfile.write(temp)
            logfile.close()
        builtins.print(*args, **kwargs)

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
        last_utc = 0 #last time file was modified
        end_str = [] #list for keeping track of the lines added
        chan = ctx.guild.get_channel(self.channel)
        with open(self.file_path, 'r') as f:  
            last_utc = os.path.getmtime(self.file_path)
            for r in f.readlines():
                if not self.enabled:
                    return
                if r not in end_str: #to avoid duplicate entries
                    try:
                        if r is None:
                            end_str.append('-\n')                           

                        else:
                            end_str.append(r)    

                    except:

                        end_str.append('-\n')    
            print(end_str)
            for fj in range(len(end_str) -  num,len(end_str)):
                if len(end_str[fj]) > 2000:
                    while(len(end_str[fj]) > 2000):
                        await ctx.send(end_str[fj][:1999])
                        end_str[fj] = end_str[fj][2000:]
                await ctx.send(end_str[fj])
                await asyncio.sleep(1)
            while(self.enabled):
                if os.path.getmtime(self.file_path) != last_utc: #checks for the file being modified
                    for fi in f.readlines():
                        if fi not in end_str:
                            if not self.enabled: #exit on self.enabled = False
                                return      
                            #await chan.send(fi) 
                        await asyncio.sleep(1)            
                             
                last_utc = os.path.getmtime(self.file_path) #update modified time
                await asyncio.sleep(1)
            f.close()       
            

      

    @commands.command()
    @checks.is_owner()
    async def stopstream(self, ctx: commands.Context):
        self.enabled = False
            
