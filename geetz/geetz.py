import discord
from redbot.core import commands
import asyncio
import io
import requests
from PIL import Image, ImageDraw, ImageFont

class Geetz(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.reacted_messages = []
        
    @commands.command()
    async def geet(self, ctx):
        gif_url = "https://cdn.discordapp.com/attachments/1047739355738943540/1089112795322253413/1.gif"
        msg = await ctx.send(gif_url)
        await msg.add_reaction("<a:finalfire:1089091108165922836>")

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) == "<a:finalfire:1089091108165922836>" and reaction.message.id == msg.id

        try:
            reaction, user = await self.bot.wait_for("reaction_add", timeout=60.0, check=check)
        except asyncio.TimeoutError:
            return
        else:
            gif_url2 = "https://cdn.discordapp.com/attachments/1047739355738943540/1089112835122024489/2.gif"
            await msg.edit(content=gif_url2)
            await ctx.send("<a:finalfire:1089091108165922836>" * 20)
            self.reacted_messages = []
            
    @commands.Cog.listener()
    async def on_message(self, message):
        if len(self.reacted_messages) >= 4:
            return

        if message.author.bot:
            return

        if message.content.startswith("]geet"):
            return

        await message.add_reaction("<a:finalfire:1089091108165922836>")
        await message.add_reaction("<a:letwiggleg:1047789428174757908>")
        await message.add_reaction("<a:letwigglee:1047789423217098814>")
        await message.add_reaction("<a:letwigglee:1089110256430370877>")
        await message.add_reaction("<a:letwigglet:1047789468708524082>")
        await message.add_reaction("<a:finalfire:1089110692952539166>")
        self.reacted_messages.append(message)
####################################################################
    @commands.command()
    async def dot(self, ctx, *, text: str = None):
        if text:
            await self.dot_text(ctx, text)
        elif ctx.message.attachments:
            await self.dot_image(ctx, ctx.message.attachments[0].url)
        else:
            await ctx.send("Please provide text or attach an image with the command.")

    async def dot_text(self, ctx, text: str):
        img = Image.new("1", (len(text) * 6, 8), 1)
        draw = ImageDraw.Draw(img)
        font = ImageFont.load_default()
        draw.text((0, 0), text, font=font, fill=0)
        output = io.BytesIO()
        img.save(output, format="PNG")
        output.seek(0)
        await ctx.send(file=discord.File(fp=output, filename="dot_art_text.png"))

    async def dot_image(self, ctx, url: str):
        response = requests.get(url)
        input_image = Image.open(io.BytesIO(response.content)).convert("1")
        output = io.BytesIO()
        input_image.save(output, format="PNG")
        output.seek(0)
        await ctx.send(file=discord.File(fp=output, filename="dot_art_image.png"))
