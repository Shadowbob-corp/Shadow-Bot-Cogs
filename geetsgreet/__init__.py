from redbot.core.bot import Red
from .geetsgreet import GeetsGreet

async def setup(bot: Red) -> None:
    bot.add_cog(GeetsGreet(bot))