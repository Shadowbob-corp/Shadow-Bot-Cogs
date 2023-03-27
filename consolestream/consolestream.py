
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
     
    #this function splits a string into 4000 char blocks to be sent to discord 
    def split_string(self,string):
        ret = []
        if len(string) < 3999:
            return [string]
        l = len(string)/3999
        for n in range(math.ceil(l)):
            if (n+1) * 1999 > len(string):
                ret.append(string[(n)*1999:])
            else:
                ret.append(string[n*1999:(n+1)*3999])
        return ret            
    
    def difference(self, string1, string2):
        one = set(string1)
        two = set(string2)
        diff = one.symmetric_difference(two)
        output = ""
        for o in diff:
            output += o
        return output

    @commands.command()
    @checks.is_owner()
    async def stream(self, ctx:commands.Context, num: int = 10):        
        self.enabled = True
        last_utc = 0 #last time file was modified
        end_str = [] #list for keeping track of the lines added
        chan = ctx.guild.get_channel(self.channel)
        current_text = ""
        with open(self.file_path, 'r') as f:  
            last_utc = os.path.getmtime(self.file_path)
            current_text = f.readlines()
            print(current_text)
            for r in current_text:
                print(r)
                if not self.enabled:
                    return
                if r not in end_str: #to avoid duplicate entries
                    try:
                            end_str.append(r)    
                
                    except:

                        end_str.append('\n') 
                          
            p_string = []
            ind = 0
            print('len = ' + str(len(end_str)))
            print(end_str)
            if end_str is not None:
                for fj in range(len(end_str) -  num,len(end_str)-1):
                    p_string= self.split_string(end_str[fj])
                    
                    for p in p_string:
                        await chan.send(p)
                        await asyncio.sleep(1)
                while(self.enabled):
                    if os.path.getmtime(self.file_path) != last_utc: #checks for the file being modified
                        dif = self.difference(current_text, f.read())
                        current_text = f.read()
                        print(dif)
                        fi = dif
                        sstr = ""
                        
                        if not self.enabled: #exit on self.enabled = False
                            return      
                        for f in self.split_string(dif):
                            await chan.send(f)
                            await asyncio.sleep(1)
                        await chan.send(self.split_string(fi))
        
                    await asyncio.sleep(1)            
                            
                    last_utc = os.path.getmtime(self.file_path) #update modified time

            f.close()       
            

      

    @commands.command()
    @checks.is_owner()
    async def stopstream(self, ctx: commands.Context):
        self.enabled = False
            
