from redbot.core.bot import Red
from .calendar import Calendar



async def setup(bot: Red) -> None:
    bot.add_cog(Calendar(bot))