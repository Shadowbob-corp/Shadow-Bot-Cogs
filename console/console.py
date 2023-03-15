import asyncio
import asyncore
import discord
import sys
import math

from redbot.core import commands



class Console(commands.Cog):
    """Clear your console."""

    __author__ = "jay_"
    __version__ = "0.0.1"

    def __init__(self, bot):
        self.bot = bot
        self.enabled = True
        self.file_path = '/root/redenv/data/core/logs/latest.log'

    

    @commands.is_owner()
    @commands.command()
    async def console(self, ctx: commands.Context, lines:int = 10):
        
        
        nlines = lines
        with open(self.file_path, 'r+') as logf:            
            line = logf.readlines()
               
            msg_list = []           
            num_lines = len(line)
            if nlines > num_lines or nlines == 0:
                nlines = num_lines
            total_str = ""
            msg = line[num_lines - int(nlines):]
            chars = 0
            last_ind = num_lines - int(nlines)
            first_index =  num_lines  -  int(nlines)
            lin = 0

            for m in msg:      
                in_line = True
                while in_line:
                    if  m == "" or m == None or m=="\\n" or len(m) == 0: 
                        if len(line) > len(line) - lin:
                            msg_list.insert(0, line[first_index-1])
                            lin += 1
                            first_index -= 1   
                        break
                    elif chars + len(m) > 2000:

                        total_str = total_str + m[last_ind:last_ind + 1999] 
                        last_ind += 1999
                        chars = 0
                        msg_list.append(f'<>{total_str}')
                        total_str = ""                    
                    else:                                              
                        msg_list.append(f'<>{m}')
                        total_str = ""
                        break                
                lin += 1
            totalstr = ""
            print(msg_list)
            for m in msg_list:
                if m == "" or m==None or m=='\\n':
                    print('skip ' + m)
                    continue
                print('totalstr = ' + totalstr)
                totalstr += m  + '\n'  
                print('totalstr now = ' + totalstr)
            await ctx.send(totalstr)

            logf.close()
        
                

            
            
            
            

