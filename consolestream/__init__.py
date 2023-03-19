from .consolestream import ConsoleStream


def setup(bot):
    cog = ConsoleStream(bot)
    bot.add_cog(cog)
