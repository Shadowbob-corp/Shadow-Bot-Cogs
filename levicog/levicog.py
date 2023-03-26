import discord
from discord.ext import commands 
from discord.ext.commands import Cog
from redbot.core import commands, checks, Config
from redbot.core.bot import Red
import asyncio

class LeviCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.reacted_messages = []

    @commands.command()
    async def levi(self, ctx):
        img_url = "https://cdn.discordapp.com/attachments/1047739355738943540/1089321544670515230/Aye_buhdey.png"
        msg = await ctx.send(img_url)
        await msg.add_reaction("<:gaba2:1089304006544855211>")

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) == "<:gaba2:1089304006544855211>" and reaction.message.id == msg.id

        try:
            reaction, user = await self.bot.wait_for("reaction_add", timeout=60.0, check=check)
        except asyncio.TimeoutError:
            return
        else:
            img_url2 = "https://cdn.discordapp.com/attachments/1047739355738943540/1089319479902740520/WHO_TOOK.png"
            await msg.edit(content=img_url2)
            await ctx.send("<:gaba2:1089304006544855211><:gaba:1089303637722943609><:gaba2:1089304006544855211><:gaba:1089303637722943609><:gaba2:1089304006544855211><:gaba:1089303637722943609><:gaba2:1089304006544855211>")

    @commands.Cog.listener()
    async def on_message(self, message):
        if len(self.reacted_messages) >= 4:
            return  

        if message.author.bot:
            return

        if message.content.startswith("]levi"):
            return

        await message.add_reaction("<:gaba2:1089304006544855211>")
        await message.add_reaction("<:chatterljnug:1044011767304572958>")
        await message.add_reaction("<a:neonultrafastParrot:1032407830432596109>")
        await message.add_reaction("<a:s_G:1081386781443903579>")
        await message.add_reaction("<a:s_A:1081386763261587466>")
        await message.add_reaction("<a:s_B:1081386766369562687>")
        await message.add_reaction("<a:s_A:1089311993263050862>")
        await message.add_reaction("<:chatterljnug:1089312361480994907>")
        await message.add_reaction("<a:neonultrafastParrot:1089312663231803513>")
        self.reacted_messages.append(message)