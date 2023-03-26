import discord
from redbot.core import commands
from redbot.core import Config
from typing import Optional

class SuggestShit(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=1234567890, force_registration=True)
        self.config.register_guild(suggestions_counter=0)

    @commands.command()
    async def suggest(self, ctx, *, suggestion: str):
        if ctx.channel.id != 1032433292655480833:
            return
        counter = await self.config.guild(ctx.guild).suggestions_counter()
        await self.config.guild(ctx.guild).suggestions_counter.set(counter + 1)

        suggestion_embed = discord.Embed(title=f"Suggestion #{counter}", description=suggestion, color=0x3498DB)
        suggestion_embed.set_footer(text=f"suggested by {ctx.author}", icon_url=ctx.author.avatar_url)

        await ctx.message.delete()
        suggestions_channel = self.bot.get_channel(1037405141499912192)
        await suggestions_channel.send(embed=suggestion_embed)

    @commands.command()
    async def decision(self, ctx, decision: str, suggestion_number: int, *, reason: Optional[str] = None):
        if decision.lower() not in ['approve', 'deny', 'consider']:
            await ctx.send("Invalid decision. Please use 'approve', 'deny', or 'consider'.")
            return

        decision_channel = self.bot.get_channel(1030564322352562257)
        suggestions_channel = self.bot.get_channel(1037405141499912192)

        suggestion_message = None
        async for message in suggestions_channel.history(limit=100):
            if message.embeds and message.embeds[0].title == f'Suggestion #{suggestion_number}':
                suggestion_message = message
                break

        if not suggestion_message:
            await ctx.send("Suggestion not found.")
            return

        suggestion_embed = suggestion_message.embeds[0]
        suggestion_embed.color = 0x2ECC71 if decision.lower() == 'approve' else 0xE74C3C if decision.lower() == 'deny' else 0xF1C40F
        suggestion_embed.add_field(name=f"Decision: {decision.capitalize()}", value=reason if reason else "No reason provided", inline=False)

        await decision_channel.send(embed=suggestion_embed)
        await suggestion_message.delete()

