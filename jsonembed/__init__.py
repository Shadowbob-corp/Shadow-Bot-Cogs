from .jsonembed import Jsonembed


def setup(bot):
    bot.add_cog(Jsonembed(bot))
