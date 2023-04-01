import discord
from discord.ext import commands
from discord.ext.commands import Cog
from redbot.core import commands, checks, Config
from redbot.core.bot import Red
import asyncio
import datetime

class GeetsGreet(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.last_join = None
    def ordinal(self, n):
        if 10 <= n % 100 <= 20:
            suffix = 'th'
        else:
            suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')
        return str(n) + suffix

    @commands.command()
    @checks.is_owner()
    async def testgeet(self, ctx):
        member = ctx.author
        server_icon = member.guild.icon_url
        member_avatar = member.avatar_url

        # create the welcome embed
        embed = discord.Embed(
            title="█▓▒­░⡷=- 🅆🄴🄻🄲🄾🄼🄴 🅃🄾 🄱🄻🄰🄲🄺🄾🅄🅃 -=⢾░▒▓█",
            description=f"☆ {member.mention} is the {self.ordinal(len(member.guild.members))} blacked out homie to find their way here :p ☆",
            color=0x00ff00
        )
        embed.add_field(name="▼ 𝚆𝚑𝚎𝚛𝚎 𝚝𝚑𝚎 𝚏𝚞𝚌𝚔 𝚊𝚖 𝙸? ▼", value="⇩ ◇ 𝐘𝐨𝐮'𝐫𝐞 𝐇𝐞𝐫𝐞 ◇ ⇩", inline=True)
        embed.add_field(name="▼ 𝚆𝚑𝚎𝚛𝚎 𝚝𝚑𝚎 𝚏𝚞𝚌𝚔 𝚒𝚜 𝚅𝙲? ▼", value="➩ <#1074601429756555286> ➤ VC Entrance", inline=True)
        embed.add_field(name="➩ <#1030564322352562257> ➤ Main Chat", value=" ", inline=False)
        embed.set_author(name=member.guild.name, icon_url=server_icon)
        embed.set_footer(text=":)", icon_url=member_avatar)

        # send the welcome message to the welcome channel
        welcome_channel = discord.utils.get(member.guild.text_channels, name="m𝚊𝚒𝚗-𝚜𝚑𝚘𝚠")
        if welcome_channel is not None:
            await welcome_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        dt = datetime.datetime.now()
        time_since = dt - self.last_join[1]
        if self.last_join[0] == member.id and time_since < datetime.timedelta(seconds=3):
            return

        # get the server icon and member avatar
        server_icon = member.guild.icon_url
        member_avatar = member.avatar_url

        # create the welcome embed
        embed = discord.Embed(
            title="█▓▒­░⡷=- 🅆🄴🄻🄲🄾🄼🄴 🅃🄾 🄱🄻🄰🄲🄺🄾🅄🅃 -=⢾░▒▓█",
            description=f"☆ {member.mention} is the {self.ordinal(len(member.guild.members))} blacked out homie to find their way here :p ☆",
            color=0x00ff00
        )
        embed.add_field(name="▼ 𝚆𝚑𝚎𝚛𝚎 𝚝𝚑𝚎 𝚏𝚞𝚌𝚔 𝚊𝚖 𝙸? ▼", value="⇩ ◇ 𝐘𝐨𝐮'𝐫𝐞 𝐇𝐞𝐫𝐞 ◇ ⇩", inline=True)
        embed.add_field(name="▼ 𝚆𝚑𝚎𝚛𝚎 𝚝𝚑𝚎 𝚏𝚞𝚌𝚔 𝚒𝚜 𝚅𝙲? ▼", value="➩ <#1074601429756555286> ➤ VC Entrance", inline=True)
        embed.add_field(name="➩ <#1030564322352562257> ➤ Main Chat", value=" ", inline=False)
        embed.set_author(name=member.guild.name, icon_url=server_icon)
        embed.set_footer(text="☆", icon_url=member_avatar)

        # send the welcome message to the welcome channel
        welcome_channel = discord.utils.get(member.guild.text_channels, name="m𝚊𝚒𝚗-𝚜𝚑𝚘𝚠")
        if welcome_channel is not None:
            await welcome_channel.send(embed=embed)
            self.last_join = (member.id, datetime.datetime.now())
