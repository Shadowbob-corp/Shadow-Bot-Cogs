import discord
from redbot.core.utils.chat_formatting import box, humanize_number

from redbot.core import checks, bank, commands
from redbot.core.i18n import Translator, cog_i18n

from redbot.core.bot import Red  # Only used for type hints

def Shutup(commands.Cog):
    """Tell someone politely that they are talking too much"""

    def __init__(self, bot: Red):
        
        self.bot = bot
        self.role = 1088698012399841311
    
    @commands.command()
    async def shutup(self, ctx: commands.Context, member: discord.Member):
        if 

