
import os
import wget
from redbot.core import commands, checks
import asyncio
import builtins
import discord
from io import BytesIO
from PIL import Image

def print(*args, **kwargs):
        with open('/home/jay/redenv/terminal.log','a') as logfile:
            temp = ""
            for a in args:
                temp += str(a)
            logfile.write(temp)
            logfile.close()
        builtins.print(*args, **kwargs)

class Impersonate(commands.Cog):
    '''This cog streams the output of the console to a specified channel (set self.channel to the id)
    Be sure to run the accompanying bash script to correctly launch Redbot so that it is streaming the console output to the file.
    Set the filepath of your output in self.file_path.'''

    __author__ = "Jay_"
    __version__ = "0.0.1"

    def __init__(self, bot):
        self.bot = bot
        self.member_info = {}
        

    def pfp(self, mem: discord.Member):
        user = mem
        if user.is_avatar_animated():
            url = user.avatar_url_as(format="gif")
        if not user.is_avatar_animated():
            url = user.avatar_url_as(static_format="png")
        #print(url)
        return url

    @commands.command()
    @checks.is_owner()
    async def impersonate(self, ctx:commands.Context, member: discord.Member):        
        url = self.pfp(member)
        print(member.avatar_url_as(format="png"))
        path = f'/home/jay/redenv/lib/python3.9/site-packages/redbot/cogs/impersonate/' + str(member.name) + '.jpg'
        response = wget.download(str(url))
        print(response)
        with open(path,'rb') as _avatar:
            av = _avatar
            self.member_info = {member.id: {'avatar': av, 'name': member.name}}
            mem = member.edit(avatar=_avatar)
            
        