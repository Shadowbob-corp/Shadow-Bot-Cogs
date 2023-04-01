import discord
from discord.ext import commands 
from discord.ext.commands import Cog
from redbot.core import commands, checks, Config
from redbot.core.bot import Red
import asyncio

class LeviCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
        self.config = Config.get_conf(self, identifier=178778732478)
        self.default = {"num": 0, "active": False,"react": False}
        self.config.register_guild(**self.default)
        self.counter = 0
        self.active = False
        self.reaction_add = False
        self.img_url = "https://cdn.discordapp.com/attachments/1047739355738943540/1089321544670515230/Aye_buhdey.png"
        self.img_url2 ="https://cdn.discordapp.com/attachments/1047739355738943540/1089319479902740520/WHO_TOOK.png"
        self.msg = None
        self.no_react = False

    @commands.command()
    @commands.cooldown(1, 30, commands.BucketType.member)
    async def levi(self, ctx):
        if self.active:
            await ctx.send("Someone is already running this command, try again later.")
            return
        
        msg = await ctx.send(self.img_url)
        self.msg = msg
        await msg.add_reaction("<:gaba2:1089304006544855211>")        
        self.reaction_add = True
        await asyncio.sleep(10)
        await self.config.react.set(True)
        
        
    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if user.bot:
            return
        if self.reaction_add and not self.active:
            if str(reaction.emoji) == '<:gaba2:1089304006544855211>':
                await reaction.message.edit(content=self.img_url2)
                await self.msg.add_reaction("<:gaba2:1089304006544855211>")
                await self.msg.add_reaction("<:chatterljnug:1044011767304572958>")
                await self.msg.add_reaction("<a:neonultrafastParrot:1032407830432596109>")
                await self.msg.add_reaction("<a:s_G:1081386781443903579>")
                await self.msg.add_reaction("<a:s_A:1081386763261587466>")
                await self.msg.add_reaction("<a:s_B:1081386766369562687>")
                await self.msg.add_reaction("<a:s_A:1089311993263050862>")
                await self.msg.add_reaction("<:chatterljnug:1089312361480994907>")
                await self.msg.add_reaction("<a:neonultrafastParrot:1089312663231803513>")
                
                self.active = True
                await self.config.react.set(True)c


    @commands.Cog.listener()
    async def on_message(self, message):
        self.no_react = await self.config.react()
        if await self.config.num() is None:
            await self.config.num.set(0)
        while(self.active and self.no_react):
            counter = await self.config.num()
            if counter >= 4:
                counter = 0
                await self.config.num.set(0)
                await self.config.alive.set(False)
                self.active = False
                self.no_react = False
                break
            await message.add_reaction("<:gaba2:1089304006544855211>")
            await message.add_reaction("<:chatterljnug:1044011767304572958>")
            await message.add_reaction("<a:neonultrafastParrot:1032407830432596109>")
            await message.add_reaction("<a:s_G:1081386781443903579>")
            await message.add_reaction("<a:s_A:1081386763261587466>")
            await message.add_reaction("<a:s_B:1081386766369562687>")
            await message.add_reaction("<a:s_A:1089311993263050862>")
            await message.add_reaction("<:chatterljnug:1089312361480994907>")
            await message.add_reaction("<a:neonultrafastParrot:1089312663231803513>")

            counter += 1
            await self.config.num.set(counter)