from .console import Console


def setup(bot):
    cog = Console(bot)
    bot.add_cog(cog)
