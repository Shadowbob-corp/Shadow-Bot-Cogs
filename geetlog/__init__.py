# Copyright (c) 2021 - Jojo#7791
# Licensed under MIT



from redbot.core.bot import Red

from .geetlog import Geetlog


async def setup(bot: Red):
    bot.add_cog(Geetlog(bot))
