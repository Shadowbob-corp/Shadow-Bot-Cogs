from .impersonate import Impersonate


def setup(bot):
    cog = Impersonate(bot)
    bot.add_cog(cog)
