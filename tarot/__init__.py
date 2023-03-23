from .tarot import Tarot


def setup(bot):
    bot.add_cog(Tarot(bot))