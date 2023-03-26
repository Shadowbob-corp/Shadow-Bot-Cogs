"""
MIT License

Copyright (c) 2020-present phenom4n4n

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

# original invoke hook logic from https://github.com/mikeshardmind/SinbadCogs/tree/v3/noadmin

 # Made by Jay_ for all the homies at Blackout

import shutil

import wget
import datetime
import discord
from redbot.core import commands, checks
from redbot.core.bot import Red
from os.path import exists
import asyncio
import os
from PIL import Image
from bs4 import BeautifulSoup
import requests
import builtins




def print(*args, **kwargs):
        with open('/home/jay/redenv/terminal.log','a') as logfile:
            temp = ""
            for a in args:
                temp += str(a)
            logfile.write(temp)
        builtins.print(*args, **kwargs)
class Homies(commands.Cog):
    """
    Lets make commands for all the homies
    """
   
    __version__ = "0.0.4"

    def __init__(self, bot: Red) -> None:
        self.bot = bot
        self.today = datetime.datetime.today()
        self.URL = 'https://svs.gsfc.nasa.gov/Gallery/moonphase.html'
        self.phases = ['New Moon', 'Waxing Crescent', 'First Quarter', 'Waxing Gibbous', 'Full', 'Waning Gibbous', 'Last Quarter', 'Waning Crescent']
        self.used = 0
        self.mol_ind = 0
        self.mol_num = ['1','2','3']
        self.mol_filepath = '/home/jay/redenv/lib/python3.9/site-packages/redbot/cogs/homies/molly'
        self.thrt_filepath = '/home/jay/redenv/lib/python3.9/site-packages/redbot/cogs/throat/throat'
        self.thrt_ind = 9
        self.thrt_num = ['1','2','3','4','5','6','7','8','9','10','11']
        self.braile_chars = ''' ⡴⠑⡄⠀⠀⠀⠀⠀⠀⠀⣀⣀⣤⣤⣤⣀⡀⠀⠀⠀⠀
⠸⡇⠀⠿⡀⠀⠀⠀⣀⡴⢿⣿⣿⣿⣿⣿⣿⣿⣷⣦⡀⠀⠀⠀
⠀⠀⠀⠀⠑⢄⣠⠾⠁⣀⣄⡈⠙⣿⣿⣿⣿⣿⣿⣿⣿⣆⠀⠀
⠀⠀⠀⠀⢀⡀⠁⠀⠀⠈⠙⠛⠂⠈⣿⣿⣿⣿⣿⠿⡿⢿⣆⠀
⠀⠀⠀⢀⡾⣁⣀⠀⠴⠂⠙⣗⡀⠀⢻⣿⣿⠭⢤⣴⣦⣤⣹⠀
⠀⠀⢀⣾⣿⣿⣿⣷⣮⣽⣾⣿⣥⣴⣿⣿⡿⢂⠔⢚⡿⢿⣿⣦
⠀⢀⡞⠁⠙⠻⠿⠟⠉⠀⠛⢹⣿⣿⣿⣿⣿⣌⢤⣼⣿⣾⣿⡟
⠀⣾⣷⣶⠇⠀⠀⣤⣄⣀⡀⠈⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇
⠀⠉⠈⠉⠀⠀⢦⡈⢻⣿⣿⣿⣶⣶⣶⣶⣤⣽⡹⣿⣿⣿⣿⡇
⠀⠀⠀⠀⠀⠀⠀⠉⠲⣽⡻⢿⣿⣿⣿⣿⣿⣿⣷⣜⣿⣿⣿⡇
⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣷⣶⣮⣭⣽⣿⣿⣿⣿⣿⣿⣿⠀
⠀⠀⠀⠀⠀⠀⣀⣀⣈⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠇⠀
⠀⠀⠀⠀⠀⠀⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠃⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠀⠀⠀⠀⠀
⠄⠄⠄⠄⠄⠄⣠⢼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⡄⠄⠄⠄
⠄⠄⣀⣤⣴⣾⣿⣷⣭⣭⣭⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⡀⠄⠄
⠄⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣸⣿⣿⣧⠄⠄
⠄⣿⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⢻⣿⣿⡄⠄
⠄⢸⣿⣮⣿⣿⣿⣿⣿⣿⣿⡟⢹⣿⣿⣿⡟⢛⢻⣷⢻⣿⣧⠄
⠄⠄⣿⡏⣿⡟⡛⢻⣿⣿⣿⣿⠸⣿⣿⣿⣷⣬⣼⣿⢸⣿⣿⠄
⠄⠄⣿⣧⢿⣧⣥⣾⣿⣿⣿⡟⣴⣝⠿⣿⣿⣿⠿⣫⣾⣿⣿⡆
⠄⠄⢸⣿⣮⡻⠿⣿⠿⣟⣫⣾⣿⣿⣿⣷⣶⣾⣿⡏⣿⣿⣿⡇
⠄⠄⢸⣿⣿⣿⡇⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇⣿⣿⣿⡇
⠄⠄⢸⣿⣿⣿⡇⠄⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⣿⣿⣿⠄
⠄⠄⣼⣿⣿⣿⢃⣾⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⣿⣿⣿⡇⠄
⠄⠄⠸⣿⣿⢣⢶⣟⣿⣖⣿⣷⣻⣮⡿⣽⣿⣻⣖⣶⣤⣭⡉⠄⠄⠄⠄⠄
⠄⠄⠄⢹⠣⣛⣣⣭⣭⣭⣁⡛⠻⢽⣿⣿⣿⣿⢻⣿⣿⣿⣽⡧⡄⠄⠄⠄
⠄⠄⠄⠄⣼⣿⣿⣿⣿⣿⣿⣿⣿⣶⣌⡛⢿⣽⢘⣿⣷⣿⡻⠏⣛⣀⠄⠄
⠄⠄⠄⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⠙⡅⣿⠚⣡⣴⣿⣿⣿⡆⠄
⠄⠄⣰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⠄⣱⣾⣿⣿⣿⣿⣿⣿⠄
⠄⢀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⠄
⠄⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠣⣿⣿⣿⣿⣿⣿⣿⣿⣿⠄
⠄⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠛⠑⣿⣮⣝⣛⠿⠿⣿⣿⣿⣿⠄
⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⠄⠄⠄⠄⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠄
⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠇⠄⠄⠄⠄⢹⣿⣿⣿⣿⣿⣿⣿⣿⠁⠄
⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠏⠄⠄⠄⠄⠄⠸⣿⣿⣿⣿⣿⡿⢟⣣⣀'''
        self.braile_dict = {}
        self.braile_pairs = {10431: 10367, 10367: 10431, 10311:10424,10424:10311, 10438:10480, 10480:10438, 10312:ord('⢁'), ord('⢁'):10312 , 10436: ord('⣠'), 32: 32, ord('⣠'): 10436, 10372:ord("⡠"),ord("⡠"):10372 , 10484: ord('⣦'), ord('⣦'):10484, 10404: ord('⡤'), ord('⡤'):10404 , 10427:10335,  10335: 10427, 10455: ord('⣺'),ord('⣺'):10455, 10433:10440, 10440:10433, 
                             10366: ord('⢷'), ord('⢷'): 10366, 10394: ord('⡓'), ord('⡓'):10394, 10469:10476, 10476: 10469, 10494: ord('⣷'), ord('⣷'): 10494, 10493:10479, 10479:10493, 10478:ord('⣵'),ord('⣵'):10478, 10492:10471, 10471:10492, 10444:10465, 10465:10444, 10425:10319, 10319:10425,10334: ord('⢳'),ord('⢳'):10334, 10486:10486, 10361: ord('⢏'), ord('⢏'):10361,10406:ord('⡴'), ord('⡴'):10406, 10460:10467, 10467:10460,
                             10363: ord('⡻'), ord('⡻'):10363, 10477:10477, 10428:10343, 10343:10428, 10488:10439, 10439:10488, 10395:10331, 10331:10395,10310:ord('⢰'), ord('⢰'):10310,10475:10461, 10461:10475,10463:10491, 10491:10463, 10422: ord('⡶'), ord('⡶'):10422, 10403: ord('⡜'), ord('⡜'):10403, 10343: ord('⢼'), ord('⢼'):10343, 10429: ord('⡯'), ord('⡯'):10429,10459:10459,10392: ord('⡃'), ord('⡃'):10392,10309: ord('⢨'), ord('⢨'):10309, 10400: ord('⡄'), ord('⡄'):10400,
                              10399: ord('⡻'), ord('⡻'):10399, 10240:10240, 10304:10368,10368:10304, 10489:ord('⣏'), ord('⣏'):10489,10468:10468, 10432:10432, 10495:10495, 10303:10303, 10296:10247, 10247:10296, 10265: ord('⠋'), ord('⠋'):10265, 10241:10248, 10248:10241, 10242:ord('⠐'), ord('⠐'):10242,
                              10267:10267, 10285:10285, 10292:ord('⠦'), ord('⠦'):10292, 10260: ord('⠢'), ord('⠢'):10260, 10249:10249, 10271:10299, 10299:10271, 10290: ord('⠖'), ord('⠖'):10290, 10243:ord('⠘'), ord('⠘'):10243, 10297: ord('⠏'),  ord('⠏'):10297, 10244: ord('⠠'), ord('⠠'):10244,
                              ord('⡘'):10371, 10371:ord('⡘'), 10313: ord('⢉'), ord('⢉'):10313, 10454:ord('⣲'), ord('⣲'):10454, 10275: ord('⡰'), ord('⡰'):10275, 10255: ord('⠏'), ord('⠏'):ord('⠹'),  10266:ord('⠓'), ord('⠓'):10266, 10481: ord('⣎'), ord('⣎'):10481, 10302:ord('⠷'), ord('⠷'):10302,
                              ord('⢛'): ord('⡛'), ord('⡛'): ord('⢛'), ord('⢼'): ord('⡧'), ord('⡧'):ord('⢼'), ord('⢦'):ord('⡴'), ord('⡴'):ord('⢦'), ord('⠑'):ord('⠊'), ord('⢂'):ord('⡐'), ord('⡐'):ord('⢂')  }
                             
        self.braile_to_ascii = {10204: chr(10204),10304: chr(10304),ord("⠀"): "⠀",ord("⠀"):"⠀", ord('a'): '⠁', ord('b'): '⠃', ord('c'): '⠉', ord('d'): '⠙', ord('e'): '⠑', ord('f'): '⠋', ord('g'): '⠛', ord('h'): '⠓', ord('i'): '⠊', ord('j'): '⠚', ord('k'): '⠅', ord('l'): '⠇', ord('m'): '⠍', ord('n'): '⠝', ord('o'): '⠕', ord('p'): '⠏', ord('q'): '⠟', ord('r'): '⠗', ord('s'): '⠎', ord('t'): '⠞', ord('u'): '⠥', ord('v'): '⠧', ord('w'): '⠺', ord('x'): '⠭', ord('y'): '⠽', ord('z'): '⠵', ord(' '): '⠀'}   
       # self.ascii_to_braile = {chr(10304):10304,"⠀": "⠀","⠀": "⠀", 'a': '⠁', 'b': '⠃', 'c': '⠉', 'd': '⠙', 'e': '⠑', 'f': '⠋', 'g': '⠛', 'h': '⠓', 'i': '⠊', 'j': '⠚', 'k': '⠅', 'l': '⠇', 'm': '⠍', 'n': '⠝', 'o': '⠕', 'p': '⠏', 'q': '⠟', 'r': '⠗', 's': '⠎', 't': '⠞', 'u': '⠥', 'v': '⠧', 'w': '⠺', 'x': '⠭', 'y': '⠽', 'z': '⠵', ' ': '⠀'}

                             
                             
                             
                             
                             
                             
                             
                             

    def deftermine_phase(self,days=0.0):
        amount = days/27
        if amount >= .98 or amount < .01:
            return 'New Moon'
        if amount >=.01 and amount <.24:
            return 'Waxing Crescent'
        if amount >= .24 and amount < .26:
            return 'First Quarter'
        if amount >= .26 and amount < .49:
            return 'Waxing Gibbous'
        if amount >= .49 and amount < .52:
            return 'Full Moon'
        if amount >= .52 and amount < .74:
            return 'Waning Gibbous'
        if amount >= .74 and amount <.76:
            return 'Last Quarter'
        if amount >= .76 and amount < .98:
            return 'Waning Crescent'

    def wait_for_file(filepath, timeout=30):
        loops = 0
        result = True
        while not exists(filepath):
            asyncio.sleep(1)
            loops+= 1
            if loops>timeout:
                result = False
                break
        return result
    
    async def mirror_art(self, ctx, input: str):
        output = ""
        ostr = ""
        string = input.split('\n',100)
        for s in string:
            temp_rev = s[::-1].strip()
            for c in temp_rev:
                output += chr(self.braile_pairs[ord(c)])
               
                    

        final_out = ""
        

        high = 0
        
        for s in string:
            if len(s) > high:
               
                high = len(s)#find the max length of the string
                print('high length = '+s + str(len(s)))
        
                
                
                
            temp_space = ""
            if len(s) < high:
                print(s + str(len(s)))
                for f in range(high-len(s)+1):
                    temp_space += " "
            final_out += temp_space + temp_rev + '\n'

                #if this row is shorter than the max, we need to add blank space
       

        return final_out
                
                    
    @commands.command()
    @checks.is_owner()
    async def testsh(self, ctx):
        await ctx.send(chr(10370))
        string = ""
        for f in self.braile_pairs.keys():
            string += str(chr(f)) + ":"+ str(chr(self.braile_pairs[f])) + "\n"
        
        
        await ctx.send(string)
        await ctx.send(await self.mirror_art(ctx,self.shrek))
       
    
    @commands.command()

    async def shrek(self, ctx):
        shrek =''' ⡴⠑⡄⠀⠀⠀⠀⠀⠀⠀⣀⣀⣤⣤⣤⣀⡀⠀⠀⠀⠀
⠸⡇⠀⠿⡀⠀⠀⠀⣀⡴⢿⣿⣿⣿⣿⣿⣿⣿⣷⣦⡀⠀⠀⠀
⠀⠀⠀⠀⠑⢄⣠⠾⠁⣀⣄⡈⠙⣿⣿⣿⣿⣿⣿⣿⣿⣆⠀⠀
⠀⠀⠀⠀⢀⡀⠁⠀⠀⠈⠙⠛⠂⠈⣿⣿⣿⣿⣿⠿⡿⢿⣆⠀
⠀⠀⠀⢀⡾⣁⣀⠀⠴⠂⠙⣗⡀⠀⢻⣿⣿⠭⢤⣴⣦⣤⣹⠀
⠀⠀⢀⣾⣿⣿⣿⣷⣮⣽⣾⣿⣥⣴⣿⣿⡿⢂⠔⢚⡿⢿⣿⣦
⠀⢀⡞⠁⠙⠻⠿⠟⠉⠀⠛⢹⣿⣿⣿⣿⣿⣌⢤⣼⣿⣾⣿⡟
⠀⣾⣷⣶⠇⠀⠀⣤⣄⣀⡀⠈⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇
⠀⠉⠈⠉⠀⠀⢦⡈⢻⣿⣿⣿⣶⣶⣶⣶⣤⣽⡹⣿⣿⣿⣿⡇
⠀⠀⠀⠀⠀⠀⠀⠉⠲⣽⡻⢿⣿⣿⣿⣿⣿⣿⣷⣜⣿⣿⣿⡇
⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣷⣶⣮⣭⣽⣿⣿⣿⣿⣿⣿⣿⠀
⠀⠀⠀⠀⠀⠀⣀⣀⣈⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠇⠀
⠀⠀⠀⠀⠀⠀⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠃⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠀⠀⠀⠀⠀
⠄⠄⠄⠄⠄⠄⣠⢼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⡄⠄⠄⠄
⠄⠄⣀⣤⣴⣾⣿⣷⣭⣭⣭⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⡀⠄⠄
⠄⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣸⣿⣿⣧⠄⠄
⠄⣿⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⢻⣿⣿⡄⠄
⠄⢸⣿⣮⣿⣿⣿⣿⣿⣿⣿⡟⢹⣿⣿⣿⡟⢛⢻⣷⢻⣿⣧⠄
⠄⠄⣿⡏⣿⡟⡛⢻⣿⣿⣿⣿⠸⣿⣿⣿⣷⣬⣼⣿⢸⣿⣿⠄
⠄⠄⣿⣧⢿⣧⣥⣾⣿⣿⣿⡟⣴⣝⠿⣿⣿⣿⠿⣫⣾⣿⣿⡆
⠄⠄⢸⣿⣮⡻⠿⣿⠿⣟⣫⣾⣿⣿⣿⣷⣶⣾⣿⡏⣿⣿⣿⡇
⠄⠄⢸⣿⣿⣿⡇⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇⣿⣿⣿⡇
⠄⠄⢸⣿⣿⣿⡇⠄⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⣿⣿⣿⠄
⠄⠄⣼⣿⣿⣿⢃⣾⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⣿⣿⣿⡇⠄
⠄⠄⠸⣿⣿⢣⢶⣟⣿⣖⣿⣷⣻⣮⡿⣽⣿⣻⣖⣶⣤⣭⡉⠄⠄⠄⠄⠄
⠄⠄⠄⢹⠣⣛⣣⣭⣭⣭⣁⡛⠻⢽⣿⣿⣿⣿⢻⣿⣿⣿⣽⡧⡄⠄⠄⠄
⠄⠄⠄⠄⣼⣿⣿⣿⣿⣿⣿⣿⣿⣶⣌⡛⢿⣽⢘⣿⣷⣿⡻⠏⣛⣀⠄⠄
⠄⠄⠄⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⠙⡅⣿⠚⣡⣴⣿⣿⣿⡆⠄
⠄⠄⣰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⠄⣱⣾⣿⣿⣿⣿⣿⣿⠄
⠄⢀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⠄
⠄⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠣⣿⣿⣿⣿⣿⣿⣿⣿⣿⠄
⠄⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠛⠑⣿⣮⣝⣛⠿⠿⣿⣿⣿⣿⠄
⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⠄⠄⠄⠄⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠄
⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠇⠄⠄⠄⠄⢹⣿⣿⣿⣿⣿⣿⣿⣿⠁⠄
⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠏⠄⠄⠄⠄⠄⠸⣿⣿⣿⣿⣿⡿⢟⣣⣀'''
        revshrek = await self.mirror_art(ctx,shrek)
        print(revshrek)
        msg = await ctx.send(shrek)
        await asyncio.sleep(1)
        await msg.edit(content=revshrek)
        await asyncio.sleep(1)
        await msg.edit(content=shrek)
        await asyncio.sleep(1)
        await msg.edit(content=revshrek)
        
       

    @commands.command()
    async def moony(self, ctx):
        await ctx.send('Standby...')
        f = '/home/jay/redenv/lib/python3.9/site-packages/redbot/cogs/homies/moony/moony.gif'
        with open(f, 'r+') as pic:
            await ctx.send(file=discord.File(f, f))

    @commands.command()
    async def moon(self, ctx):
        link = None
        await ctx.send('Standby')
        f = requests.get("https://svs.gsfc.nasa.gov/Gallery/moonphase.html")
        print('f - '+ str(f))
        soup = BeautifulSoup(f.text, 'html.parser')
        links = soup.find_all('href')
        for f in links:
            print(f)
            if f.find('moon'):
                if f[:-3] == 'jpg':
                    link = f
                    print('link ' + str(link))
                    break
            await asyncio.sleep(1)
        if link is not None:
            url = link
            print(url)
            dt = datetime.datetime.now()
            response = wget.download(url, out=f'/home/jay/redenv/lib/python3.9/site-packages/redbot/cogs/homies/pics/moon_{dt.day}_{dt.hour}_{dt.minute}_{dt.second}.jpg')
            await ctx.send(file=discord.File(response))
                    
                    
                   
            
               
                
   

            
    @commands.command()
    async def homies(self, ctx):
        await ctx.send('>nova\n>throat\n>moon\n>moonlanding (download a high quality image of the moon with points of interest labeled)\n')

    @commands.command()
    async def nova(self, ctx):
        await ctx.send('I want head pats')
        await ctx.send(file=discord.File(self.mol_filepath+self.mol_num[self.mol_ind] + '.gif', self.mol_filepath+self.mol_num[self.mol_ind] + '.gif'))
        if self.mol_ind + 1 >= len(self.mol_num):
            self.mol_ind = 0
        else:
            self.mol_ind += 1

    @commands.command()
    async def throat(self, ctx, *, text: str = None):
        if ctx.message.attachments:
            url = ctx.message.attachments[0].url
        elif text:
            url = f"http://emojicombos.com/dot-art-generator?text={text}"
        else:
            await ctx.send("Please provide either a text or an image.")
            return

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                content = await response.text()

        soup = BeautifulSoup(content, 'html.parser')
        result = soup.find('pre', class_='text-lg')

        if result:
            await ctx.send(f"```{result.text}```")
        else:
            await ctx.send("Couldn't generate dot art. Please try again.")

        
        
        
        
        
        ext = '.gif'
        await ctx.send('LMAO get a load of this creature')
        if str(self.thrt_ind + 1) in ['8','9','10','11']:
            ext = '.jpg'
        await ctx.send(file=discord.File(self.thrt_filepath+self.thrt_num[self.thrt_ind] + ext, self.mol_filepath+self.thrt_num[self.thrt_ind] + ext))
        if self.thrt_ind + 1 >= len(self.thrt_num):
            self.thrt_ind = 0
        else:
            self.thrt_ind += 1

         
  