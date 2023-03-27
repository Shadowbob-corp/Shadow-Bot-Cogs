from redbot.core import commands
import discord

class SuggestShit(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

intents = discord.Intents.default()
intents.typing = False
intents.presences = False

bot = commands.Bot(command_prefix='!', intents=intents)
suggestions = {}

@bot.command(name='suggest')
async def suggest(ctx, *, suggestion_text: str):
    global suggestions
    suggestion_id = len(suggestions) + 1
    suggestions[suggestion_id] = suggestion_text
    await ctx.send(f'Suggestion {suggestion_id} added: {suggestion_text}')

@bot.command(name='approve')
async def approve(ctx, suggestion_id: int):
    await handle_suggestion(ctx, suggestion_id, 'Approved')

@bot.command(name='deny')
async def deny(ctx, suggestion_id: int):
    await handle_suggestion(ctx, suggestion_id, 'Denied')

@bot.command(name='consider')
async def consider(ctx, suggestion_id: int):
    await handle_suggestion(ctx, suggestion_id, 'Under Consideration')

async def handle_suggestion(ctx, suggestion_id, verdict):
    global suggestions
    if suggestion_id not in suggestions:
        await ctx.send('Invalid suggestion ID.')
        return

    suggestion_text = suggestions[suggestion_id]
    del suggestions[suggestion_id]

    channel_id = 1030564322352562257
    channel = bot.get_channel(channel_id)
    
    if channel is None:
        await ctx.send('Could not find the specified channel.')
        return

    embed = discord.Embed(
        title='Suggestion Verdict',
        description=f'{verdict}: {suggestion_text}',
        color=discord.Color.green() if verdict == 'Approved' else discord.Color.red() if verdict == 'Denied' else discord.Color.orange()
    )
    embed.set_footer(text=f'Suggestion ID: {suggestion_id}')
    
    await channel.send(embed=embed)
