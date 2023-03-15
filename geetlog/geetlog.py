# Copyright (c) 2021 - Jojo#7791
# Licensed under MIT


from redbot.core import  commands, checks, Config
from redbot.core.bot import Red
import discord
import asyncio
import datetime

class Geetlog(commands.Cog):
    def __init__(self, bot: Red):
        self.bot = bot
        self.types = {0: "Mute", 1:"Kick", 2: "Ban", 3: "Move", 4: "Deafen", 5: "Timeout", 6: "Move"}
        self.guild = self.bot.guilds[0]
        self.audit_log = []
        self._init_task = self.bot.loop.create_task(self._initialize())
        self.mirror = [] 
        self.config = Config.get_conf(self, 4444556221)
        self.config.register_global(entries=[], handled_string_creator=False)
        self.mirroring = False       
        self.channel =  1084278179331575808     


    async def _initialize(self):
        """ Should only ever be a task """
        self.audit_log = await self.config.entries()
        async for entry in self.guild.audit_logs(limit=20):
            self.audit_log.append(entry)
        

    @commands.command()
    @checks.is_owner()
    async def mirrors(self, ctx,  channel_id: int=0):
        chan = ctx.guild.get_channel(channel_id)
        if chan is not None:
            self.mirroring = True
            if self.channel not in self.mirror:
                self.mirror.append(self.channel)
            else:
                await ctx.send('Invalid channel id')
                return
            await ctx.send(f'Now mirroring geetlog to {str(chan.name)}.')          
        elif toggle.lower() == 'false':
            self.mirroring = False
            self.mirror = []
        else:
            await ctx.send(f'Use "{ctx.clean_prefix}mirrors true" or "{ctx.clean_prefix}mirrors false" to toggle')

    

    def pfp(self, mem: discord.Member):
        user = mem
        if user.is_avatar_animated():
            url = user.avatar_url_as(format="gif")
        if not user.is_avatar_animated():
            url = user.avatar_url_as(static_format="png")
        print(url)
        return url

    @commands.command()
    @checks.mod_or_permissions(move_members=True)
    async def pull(self, ctx: commands.Context, member: discord.Member):
        blacklist = ctx.guild.get_role(1037631864841711666) #blacklist
        vcver = ctx.guild.get_role(1071733269382574150)
        #print(blacklist) 
        #print(vcver) #vc verified
        if vcver in member.roles: #this assigns the BLACKLIST role to members                       
            await member.remove_roles(vcver) #this removes the VC verified role (channel overrides)
            await member.add_roles(blacklist, reason=f"Blacklist")
            await member.move_to(ctx.guild.get_channel(1041194556701560862))# - shadowboob || 1049924751805648936 whats happening
        
        #this is the pull command 
        #add release command

    @commands.command()
    @checks.mod_or_permissions(move_members=True)
    async def release(self, ctx, member: discord.Member):
        blacklist = ctx.guild.get_role(1037631864841711666)#blacklist
        vcver = ctx.guild.get_role(1071733269382574150)  #vc verified
        if blacklist in member.roles:
            await member.remove_roles(blacklist)
            await member.add_roles(vcver, reason=f"VC Verified") 
            await member.add_roles(ctx.guild.get_role(1071733269382574150))#vc verified
        




    def past_tense(self, stri=""):
        if stri.lower() == "ban":
            return "Banned"
        if stri.lower() == "unban":
            return "Unbanned"
        if stri.lower() == "mute":
            return "Muted"
        if stri.lower() == "unmute":
            return "Unmuted"
        if stri.lower() == "kick":
            return "Kicked"
        if stri.lower() == "deafen":
            return "Deafened"
        if stri.lower() == "undeafen":
            return "Undeafened"
        if stri.lower() == "timeout":
            return "Timedout"
        if stri.lower() == "disconnect":
            return "Disconnected"
        if stri.lower() == "move":
            return "Moved"
        
 

    


    def hasvalue(value=""):
        return value != ""

    def timeout_len(self, inpt: datetime.timedelta):
        #print('input = ' + str(inpt))
        input = inpt
        if input >= datetime.timedelta(days=6):
         #   print('7 days')
            return "1 week"
        if input >= datetime.timedelta(hours=23):
          #  print('1 day')
            return "1 day"
        if input >= datetime.timedelta(minutes=59):
           # print('1hour')
            return "1 hour"
        if input >= datetime.timedelta(minutes=9):
            #print('10 mins')
            return "10 minutes"
        if input >= datetime.timedelta(minutes=4):
            #print('5 mins')
            return "5 minutes"
        if input >= datetime.timedelta(seconds=30):
            #print('1 min')
            return "1 minute"

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        time_un = None
        try:
            async for entry in before.guild.audit_logs(limit=1):
                if entry not in self.audit_log:
                    if str(entry.changes).find('http') > -1:
                        return
                    if entry.action is discord.AuditLogAction.ban:
                        self.audit_log.append(entry)
                        mes = "Ban"
                        await self.post_to_logchannel(entry.user, entry.target, entry.reason, mes)
                        return
                    elif entry.action is discord.AuditLogAction.kick:
                        self.audit_log.append(entry)
                        mes = "Kick"
                        await self.post_to_logchannel(entry,entry.user, entry.target, entry.reason, mes)
                        return
                    msg = str(entry.changes)
                    if msg.find('roles') > -1:
                        return
                    action = ""        
                
                    
                #  print(msg)                
                    before = msg.find('before')
                    after = msg.find('after')
                    if before ==-1 or after == -1:
                        if msg.find("communication_disab") == -1:
                            return
                    self.audit_log.append(entry)
                    before_res = msg.find('\'',before)
                    after_res = msg.find('\'', after)
                    before_close = msg.find('.', before_res)
                    after_close = msg.find('.', after_res)
                        
                # print('before - ' + str(msg[before_res:before_close]))
                    #print('after - ' + str(msg[after_res:after_close]))
                    before_date = str(msg[before_res:before_close]).split('T')
                    after_date = str(msg[after_res:after_close]).split('T')
                    #print(before_date)
                    if len(before_date) == 1:
                        return
                    before_time = before_date[1]
                    before_date = before_date[0]
                    
                    
                    if len(after_date) ==1:
                        await self.post_to_logchannel(entry.user, entry.target, entry.reason, "Removed Timeout")
                        return
                    #print("len - " +str(len(after_date)))
                    after_time = after_date[1]
                    after_date = after_date[0]
                    a = {'year': after_date[1:5], "month": after_date[6:8], "day": after_date[9:11], 'hour':  after_time[:2], 'minute': after_time[3:5], 'second':after_time[6:8]}
                    aftr = datetime.datetime(year=int(after_date[1:5]), month=int(after_date[6:8]), day=int(after_date[9:11]), hour=int(after_time[:2]), minute=int(after_time[3:5]), second=int(after_time[6:8]))
                    #bfre = datetime.datetime(year=int(before_date[1:5]), month=int(before_date[6:8]), day=int(before_date[9:11]), hour=int(before_time[:2]), minute=int(before_time[3:5]), second=int(before_time[6:8]))
                    #print(aftr)
                    time = aftr - datetime.timedelta(hours=6) - datetime.datetime.now()
                    #print(self.timeout_len(time))
                    await self.post_to_logchannel(entry.user, entry.target, entry.reason, "Timeout", self.timeout_len(time))
        except:
            print('exception')


    
    @commands.Cog.listener()    
    async def on_voice_state_update(self, member:discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        mes = ""
        if member is None:
            return
        async for entry in member.guild.audit_logs(limit=1):
            if self.audit_log[-1] != entry:
                #print(f'{entry.user} did {entry.action} to {entry.target}')
                if entry.action is discord.AuditLogAction.member_move and before.channel != after.channel and entry is not None:
                   # print(entry)
                    self.audit_log.append(entry)
                    mes = "Move"
                    await self.post_to_logchannel(entry,entry.user,  member, entry.reason, mes, b_channel=before.channel, a_channel=after.channel)
                    return                                    
                if before.mute != after.mute:
                    if member.voice.mute: 
                        mes = "Mute"
                    else:
                        mes = "Unmute"
                    await self.post_to_logchannel(entry,entry.user,  member, entry.reason, mes)
                    return
                elif after.deaf != before.deaf:                   
                    if member.voice.deaf:
                        mes = "Deafen"
                    else:
                        mes = "Undeafen"                                
                    await self.post_to_logchannel(entry, entry.user,  member, entry.reason, mes)
                    return
    
    async def post_to_logchannel( self,entry,staff:discord.Member, member: discord.Member, reason = "Geetlog", type="", time=None, b_channel=None, a_channel=None):
        await self.config.entries.set(self.audit_log)
        if type == "Timeout":
            embed = discord.Embed(title="Member " + str(self.past_tense(type)), description=f"{member.mention} was timed out by {staff.mention} for {str(time)}", color=0xFF6666)
        elif type == "Removed Timeout":
            embed = discord.Embed(title="Member Kick Removed", description=f"{member.mention}'s timeout was removed by {staff.mention}.", color=0xFF0000)  
        elif type == 'Move':
            embed = discord.Embed(title="Member " + str(self.past_tense(type)),description=f"{member.mention} was moved from {b_channel.mention} to {a_channel.mention} by {staff.mention}.", color=0xFF0000)
        else:
            embed = discord.Embed(title="Member " + str(self.past_tense(type)), description=f"{member.mention} was {self.past_tense(type)} by {staff.mention}", color=0xFF0000)
        #print(embed)
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_author(name=staff.nick, icon_url=staff.avatar_url)        
        embed.add_field(name='Reason', value=reason)
        if self.mirroring:
            for c in self.mirror:
                await staff.guild.get_channel(c).send(embed=embed)
        else:
            await staff.guild.get_channel(self.channel).send(embed=embed)
            
       
