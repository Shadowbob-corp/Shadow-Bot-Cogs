from redbot.core.bot import Red
from .suggestshit import SuggestShit

async def setup(bot: Red) -> None:
    bot.add_cog(SuggestShit(bot))