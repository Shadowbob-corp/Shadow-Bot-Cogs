from redbot.core.bot import Red
from redbot.core import commands
import asyncio
import discord

author = "geeter"
version = "0.0.1"


class Racemenu(commands.Cog):
    """My custom cog"""

    def __init__(self, bot:Red):
        self.bot = bot
        self.user_id = 0
        self.message = None
        self.racer_index = 0
        self.racer_list = ["https://i.imgur.com/hlEhXND.gif"]
        
    @commands.Cog.listener()
    async def on_reaction_add(self, reaction: discord.Reaction, member: discord.Member):
        if self.user_id == 0:
            return
        if member.id == self.user_id.id:
            print(reaction)
            if reaction.emoji.id == 1081118540385484930:
                print('left' + str(reaction.emoji))
                if self.racer_index == 0:
                    self.racer_index = 1
                embed=discord.Embed(title="Racer " + str((self.racer_index % len(self.racer_list) - 1)), color=0x00ff00)
                self.racer_index -= 1
                embed.set_image(url=self.racer_list[self.racer_index % len(self.racer_list) ])
                await self.message.edit(embed=embed)
                await self.message.remove_reaction(reaction, member)
                #makes it go left
            elif reaction.emoji.id == 1081118440670122035: #right
                print(self.message)
                embed = discord.Embed(title="Racer " + str((self.racer_index % len(self.racer_list) + 1)), color=0x00ff00)
                self.racer_index += 1
                embed.set_image(url=self.racer_list[self.racer_index % len(self.racer_list) ])
                await self.message.edit(embed=embed)
                await self.message.remove_reaction(reaction, member)
        
    @commands.command()
    async def racem(self, ctx):
        self.user_id = ctx.author
        embed = discord.Embed(title="‎‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎   ‎    ‎ ‎ ‎ ‎   ‎ ‎ ‎ ‎    <a:letrflx_p:1044940398520438784><a:letrflx_i:1044940381831315528><a:letrflx_c:1044940368887681104><a:letrflx_k:1044940386495373322> ‎ ‎ ‎ ‎ ‎‎   ‎", description="<a:letrflx_y:1044940417881342062>     <a:letrflx_o:1044940396440068146>   <a:letrflx_u:1044940409475969065> ‎ ‎ <a:letrflx_r:1044940403335512106>   ‎   ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎   ‎    ‎     ‎      ‎ ‎ㅤㅤㅤㅤㅤ<a:letfirer:1033718024030650368><a:letfirea:1033717912596385822><a:letfirec:1033717922629165066><a:letfiree:1033717935384047666><a:letfirer:1033718024030650368>\n<a:racearrowyellow:1081289958066753657><a:racearrowyellow:1081289958066753657><a:racearrowyellow:1081289958066753657><a:racearrowyellow:1081289958066753657><a:racearrowyellow:1081289958066753657> ‎ ‎ ‎‎‎  ‎  ‎ ‎ ‎‎ ‎ ‎  ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ <a:leftracearrowyellowcopy:1081291888339984435> <a:leftracearrowyellowcopy:1081291888339984435> <a:leftracearrowyellowcopy:1081291888339984435> <a:leftracearrowyellowcopy:1081291888339984435> <a:leftracearrowyellowcopy:1081291888339984435>", color=2105893)
        embed.set_image(url="https://i.imgur.com/hlEhXND.gif")
        embed.add_field(name="‎‎ ‎ ‎‎‎ ‎   ⊡⊡⊡‎‎ ‎ ‎  ‎ ⊡⊡⊡‎‎ ‎  ‎‎  ⊡⊡⊡‎ ‎ ‎‎  ‎ ⊡⊡⊡ ‎ ‎‎‎ ‎    ⊡⊡⊡‎‎ ‎ ‎‎⊡⊡⊡‎‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎  ⊡⊡‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎‎       ⊡⊡", value="‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎‎‎‎ ‎ ‎ ‎ ‎‎ ███ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎‎ \n‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎  ‎ ‎  ‎ ‎ ‎‎ ‎ ‎ ‎ ‎‎◼︎◼︎◼︎ \n‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎  ‎ ‎  ‎  ‎  ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎   ‎  ‎ ‎  ‎     ‎  ‎   ‎  ‎  ‎   ‎  ‎ ‎  ‎   ‎  ‎ ‎ ‎  ‎   ‎  ‎ <a:leftracearrowcopy:1081386180274294916>  <a:rightracearrow:1081118440670122035> \n‎   ‎  ‎ ‎   ‎    ‎  ‎         ‎ ‎ ‎     ‎     ‎  ‎  Use the arrows below to pick a racer", inline=False)
        await ctx.send(embed=embed)
        embed.add_field(name="", value="", inline=False)
        await ctx.send(embed=embed)
        embed.set_image(url="https://i.imgur.com/hlEhXND.gif")
        msg = await ctx.send(embed=embed)
        self.message = msg

   
        # this posts an embed displaying the racer character image
       
        # this reacts to the message above embed with the custom navigation emojis

        
      
                # if the user reacts with an emoji this is the new embed that will be displayed with a new racer image

