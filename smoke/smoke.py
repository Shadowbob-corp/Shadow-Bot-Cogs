# Developed by Redjumpman for Redbot.
# Inspired by the snail race mini game.

# Standard Library

import asyncio
# Red
from redbot.core import  commands
import wget

# Discord

from redbot.core.utils.chat_formatting import pagify

__author__ = "jay_"
__version__ = "0.0.1"



class Smoke(commands.Cog):


    def __init__(self, bot):
        self.bot = bot
        self.emojism = ":wind_blowing_face:"
        self.cloudsm = ":cloud:"
        self.love_dict = {
            "0":":heart:",
            "1":"<:7633_gay_LGBTQ_rainbow_heart:1043734366871891968>",
            "2":"<:7635_lesbian_pride_heart:1043734369786941450>",
            "3":"<:4647_Trans_Sparkling_heart:1043734364162379796>",
            "4":"<:2208_bisexual_heart:1043734372211249212>",
            "5":"<:panflag:1044105042069827716>",
            "6":"<:6023straightallysparkleheart:1043734374669111426>", 
            "7":"<:Plasticheart:1034688443025993808>",
            "8":"<a:neonhearts_OL:1032408836394451067>",
            "9":"<a:heartsrainbow2_DIOR:1032408813216739358>",
            "0":":heart:"
        }
        

    @commands.command()
    async def heart(self, ctx, message = '1234567898'):
        
        if len(message) > 20:
            await ctx.send('Please dont send more than 20 hearts, save some for the rest of us.')
            strng = message[0:20]
        else:
            strng = message
        order = []
        await ctx.send(f'{ctx.author.mention} loves you')
        for p in message:
            order.append(self.love_dict[p])
        cur_string = order[0]
        msg = await ctx.send(cur_string)
        ind  = 1
        last_three = False
        for h in order[1:]:            
            if ind <= 20:
                ind += 1
                cur_string = h + " " + cur_string 
                await msg.edit(content=str(cur_string))
                await asyncio.sleep(.7)
        
            
    @commands.command()
    async def hearthelp(self, ctx):
        await ctx.send(f'type >heart #######  (those being numbers from 1-9)')
        await ctx.send(f'0 = {self.love_dict["0"]} 1 = {self.love_dict["1"]} , 2 = {self.love_dict["2"]} , 3 = {self.love_dict["3"]} , 4 = {self.love_dict["4"]} , 5 = {self.love_dict["5"]} , 6 = {self.love_dict["6"]} , 7 = {self.love_dict["7"]} , 8 = {self.love_dict["8"]} , 9 = {self.love_dict["9"]}')
            
                

            
            
            
        
        
        
    @commands.command()
    async def smoke(self, ctx):
        strng = f'{self.emojism}{self.cloudsm}'
        message = await ctx.send(strng)
        spaces =  ""        
        for i in range(20):
            spaces = spaces + "   "
            await message.edit(content=str(self.emojism + spaces + self.cloudsm))
            await asyncio.sleep(1)
        await message.delete()