
from redbot.core.bot import Red
from .dev import Dev

async def setup(bot: Red):
    bot.add_cog(Dev(bot))

