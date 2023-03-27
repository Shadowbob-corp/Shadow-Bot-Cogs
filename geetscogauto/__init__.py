from redbot.core.bot import Red
from .Geetscogauto import Cogit

async def setup(bot: Red) -> None:
    bot.add_cog(Cogit(bot))