from redbot.core.bot import Red
from .helpmenu import HelpMenu

async def setup(bot: Red) -> None:
    bot.add_cog(HelpMenu(bot))