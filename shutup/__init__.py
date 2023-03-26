from .shutup import Shutup


def setup(bot):
    bot.add_cog(Shutup(bot))
