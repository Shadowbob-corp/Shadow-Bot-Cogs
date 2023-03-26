import discord
from discord.ext import commands 
from discord.ext.commands import Cog
from redbot.core import commands, checks, Config
from redbot.core.bot import Red
import asyncio

class HelpMenu(commands.Cog):
    def __init__(self, bot: Red):
        self.bot = bot
    
    @commands.command()
    async def hellp(self, ctx): 

        # this will grab the server icon and member avatar 
        server_icon = ctx.guild.icon_url
        member_avatar = ctx.author.avatar_url

        #This the big birth of the embed baby 
        embed = discord.Embed(
             title = "SHADOW BOTS HELP LINE",
             description = "YOU'VE REACHED THE SHADOW BOT HELP LINE. HOW MAY WE ASSIST YOU?",
            color=discord.Color.blue()
        )
        embed.set_thumbnail(url=server_icon)
        embed.set_author(name=ctx.author.display_name, icon_url=member_avatar)

        # Add cog categories and emojis
        cog_categories = {
            "<a:bbycowboy:1088977522026356796>": "Geets Cogs",
            "<:jay:1088972905225924648>": "Jays Cogs",
            "<a:pepemakeitrain:1089014313471180830>": "Ca$h Cogs"
        }

        for emoji, category in cog_categories.items():
            embed.add_field(name=emoji, value=category, inline=True)

        message = await ctx.send(embed=embed)

        # Add reactions to the message
        for emoji in cog_categories:
            await message.add_reaction(emoji)

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in cog_categories and reaction.message.id == message.id

        try:
            reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check)
        except asyncio.TimeoutError:
            await ctx.send("<a:boneybonkers:1054581193481392128> Too slow bitch. Gotta be quicker than that <a:boneybonkers:1054581193481392128>")
        else:
            # Display corresponding category cogs and commands
            category = cog_categories[str(reaction.emoji)]
            embed.clear_fields()
            embed.description = f"Commands for {category}:"

            # Replace with actual cogs and commands for the selected category
            commands_list = {
                "command1": "Description of command1",
                "command2": "Description of command2"
            }

            for command, description in commands_list.items():
                embed.add_field(name=command, value=description, inline=False)

            await message.edit(embed=embed)

