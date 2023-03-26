import discord
from discord.ext import commands, tasks

import datetime
from redbot.core import commands, checks, Config
from redbot.core.bot import Red

author = "Geeter Skeeter#8008"
version = "1.0.0"



class Calendar(commands.Cog):
    def __init__(self, bot: Red):
        self.bot = bot
        self.calendar = []
        
    @commands.command(name='calen')
    async def show_calendar(self,ctx):
        embed = discord.Embed(title='Blackout Staff Calendar', color=0x00ff00)
        for event in self.calendar:
            embed.add_field(name=event['name'], value=f"Date:{event['date'].strftime('%Y-%m-%d %H:%M')}", inline=False)
        await ctx.send(embed=embed)
    #this is the command that shows the calendar

    @commands.command(name='addcalen')
    async def add_calendar(self,ctx, event_name: str, event_date: str, event_time: str):
        event_d= datetime.datetime.strptime(event_date, '%m-%d-%Y')
        event_t = datetime.datetime.strptime(event_time, '%H:%M')
        event = datetime.datetime(year=event_d.year, month= event_d.month, day=event_d.day, hour=event_t.hour, minute=event_t.minute)
        self.calendar.append({'name': event_name, 'date': event})
        await ctx.send(f"Event'{event_name}' added to staff calendar for {event_d.strftime('%Y-%m-%d %H:%M')}")

    @tasks.loop(minutes=1)
    async def event_reminder(self):
        now = datetime.datetime.now()
        for event in self.calendar:
            if event['date'] - datetime.timedelta(minutes=1) <= now <= event['date']:
                channel = self.bot.get_channel(1030564322352562249)
                await channel.send(f"@everyone {event['name']}' IS ABOUT TO FUCKING START NOW!")
        
