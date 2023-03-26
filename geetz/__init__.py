from redbot.core.bot import Red
from .geetz import Geetz

async def setup(bot: Red) -> None:
    bot.add_cog(Geetz(bot))