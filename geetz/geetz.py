
import discord
from redbot.core import Config, checks, commands
from redbot.core.bot import Red 
import asyncio

class Geetz(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=123456789)
        self.reaction_task = []
        

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if user.bot:
            return

        if reaction.message.id in self.reaction_task:
            if str(reaction.emoji) == '<a:finalfire:1089110692952539166>':
                await reaction.message.clear_reaction('<a:finalfire:1089110692952539166>')
                await reaction.message.add_reaction('<a:finalfire:1089110692952539166>')
                await reaction.message.add_reaction('<a:letwiggleg:1047789428174757908>')
                await reaction.message.add_reaction('<a:letwigglee:1089110256430370877>')
                await reaction.message.add_reaction('<a:letwigglee:1089110256430370877>')
                await reaction.message.add_reaction('<a:letwigglet:1047789468708524082>')
                await reaction.message.add_reaction('<a:finalfire:1089110692952539166>')

                embed = discord.Embed()
                embed.set_image(url="https://cdn.discordapp.com/attachments/1047739355738943540/1089112835122024489/2.gif")
                await reaction.message.edit(embed=embed)
                await reaction.message.channel.send('<a:finalfire:1089091108165922836>' * 10)

                self.reaction_task.remove(reaction.message.id)

    @commands.command()
    async def geet(self, ctx):
        embed = discord.Embed()
        embed.set_image(url="https://cdn.discordapp.com/attachments/1047739355738943540/1089112795322253413/1.gif")
        message = await ctx.send(embed=embed)
        await message.add_reaction('<a:finalfire:1089110692952539166>')

        self.reaction_task.append(message.id)

