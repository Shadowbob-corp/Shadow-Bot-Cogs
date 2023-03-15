import random

import discord
from redbot.core import commands
from redbot.core.config import Config
from redbot.core.utils.chat_formatting import pagify


class Pp(commands.Cog):
    """Shows your or someone else's pp Note - 100% accurate"""

    def __init__(self, bot):
        self.bot = bot
        default = {"random": True}
        self.config = Config.get_conf(self, 694835810347909161, force_registration=True)
        self.config.register_global(**default)

    async def red_delete_data_for_user(self, **kwargs):
        """
        Nothing to delete.
        """
        return

    @commands.command()
    @commands.is_owner()
    async def randompp(self, ctx, toggle: bool):
        """
        Sets whether or not to generate a new pp length ever time the command
        is ran.
        """
        await self.config.random.set(random)
        await ctx.send(f'Random pp length is now {"enabled" if random else "disabled"}.')

    @commands.command()
    async def pp(self, ctx, *users: discord.Member):
        """
        Detects user's pp length.

        Note : This is 100% accurate.

        Enter multiple users for a comparison!

        """
        if ctx.author.id == 151079090097487873: #wolf
            await ctx.send('8" come see me.\n8================================================D')

            return
        if ctx.author.id == 279302747398995989: #pricey
            await ctx.send('''
........▄▄ ▄▄
......▄▌▒▒▀▒▒▐▄
.... ▐▒▒▒▒▒▒▒▒▒▌
... ▐▒▒▒▒▒▒▒▒▒▒▒▌
....▐▒▒▒▒▒▒▒▒▒▒▒▌
....▐▀▄▄▄▄▄▄▄▄▄▀▌
....▐░░░░░░░░░░░▌
....▐░░░░░░░░░░░▌
....▐░░░░░░░░░░░▌
....▐░░░░░░░░░░░▌
....▐░░░░░░░░░░░▌
....▐░░░░░░░░░░░▌
....▐░░░░░░░░░░░▌
....▐░░░░░░░░░░░▌
....▐░░░░░░░░░░░▌
....▐░░░░░░░░░░░▌
....▐░░░░░░░░░░░▌
...▄█▓░░░░░░░░░▓█▄
..▄▀░░░░░░░░░░░░░ ▀▄
.▐░░░░░░░▀▄▒▄▀░░░░░░▌
▐░░░░░░░▒▒▐▒▒░░░░░░░▌
▐▒░░░░░▒▒▒▐▒▒▒░░░░░▒▌
.▀▄▒▒▒▒▒▄▀▒▀▄▒▒▒▒▒▄▀
.. ▀▀▀▀▀ ▀▀▀▀▀''')
            return
        if ctx.author.id in (829943145373892628,793279897120014417): #pb, molly
            await ctx.send(f'No pp found')
            return
        if not users:
            users = {ctx.author}

        lengths = {}

        for user in users:
            random.seed(None) if await self.config.random() else random.seed(str(user.id))

            if user.id == ctx.bot.user.id or user.id in list(ctx.bot.owner_ids):
                length = random.randint(30, 35)
            else:
                length = random.randint(0, 30)

            lengths[user] = f'8{"=" * length}D'

        lengths = sorted(lengths.items(), key=lambda x: x[1])

        msg = "".join(f"**{user.display_name}'s size:**\n{length}\n" for user, length in lengths)

        for page in pagify(msg):
            await ctx.send(page)
