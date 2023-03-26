from redbot.core.bot import Red
from .levicog import LeviCog


async def setup(bot):
    bot.add_cog(LeviCog(bot))
