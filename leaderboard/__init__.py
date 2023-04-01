
from redbot.core.bot import Red
from .leaderboard import Leaderboard

async def setup(bot: Red):
    bot.add_cog(Leaderboard(bot))

