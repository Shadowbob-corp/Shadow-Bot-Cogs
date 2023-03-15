import itertools
import importlib
import sys
import keyword
import traceback
import logging
import asyncio
import discord
from redbot.core.bot import Red
from redbot.core import commands, bank, checks, Config
from redbot.core.utils.predicates import MessagePredicate
from redbot.core.utils.chat_formatting import (
    humanize_list,
    inline,
    pagify,
)
from redbot.core import (
    __version__,
    version_info as red_version_info,
    checks,
    commands,
    errors,

)
from redbot.core.utils import AsyncIter

import shutil
import os
from typing import TYPE_CHECKING, Union, Tuple, List, Optional, Iterable, Sequence, Dict, Set

author = "Jay_"
version = "0.0.1"
log = logging.getLogger("red")

class Testing(commands.Cog):
    '''Custom Wolf Pack cog made by Jay_ for Blackout.
        Wolfpack or die
        '''
    

    def __init__(self, bot: Red):
        self.bot = bot
        self.config = Config.get_conf(self, 755552245)
        #cloud self.root_path = "/home/justm/redenv/lib/python3.9/site-packages/redbot/cogs/"
        self.root_path = "/root/redenv/lib/python3.9/site-packages/redbot/cogs/" #local
        self.config.register_member(entries={'name':[("", "")]}, handled_string_creator=False)
    
    @staticmethod
    def _cleanup_and_refresh_modules(module_name: str) -> None:
        """Internally reloads modules so that changes are detected."""
        splitted = module_name.split(".")

        def maybe_reload(new_name):
            try:
                lib = sys.modules[new_name]
            except KeyError:
                pass
            else:
                importlib._bootstrap._exec(lib.__spec__, lib)

        # noinspection PyTypeChecker
        modules = itertools.accumulate(splitted, "{}.{}".format)
        for m in modules:
            maybe_reload(m)

        children = {
            name: lib
            for name, lib in sys.modules.items()
            if name == module_name or name.startswith(f"{module_name}.")
        }
        for child_name, lib in children.items():
            importlib._bootstrap._exec(lib.__spec__, lib)

    async def _load(self, pkg_names: Iterable[str]) -> Dict[str, Union[List[str], Dict[str, str]]]:
        """
        Loads packages by name.

        Parameters
        ----------
        pkg_names : `list` of `str`
            List of names of packages to load.

        Returns
        -------
        dict
            Dictionary with keys:
              ``loaded_packages``: List of names of packages that loaded successfully
              ``failed_packages``: List of names of packages that failed to load without specified reason
              ``invalid_pkg_names``: List of names of packages that don't have a valid package name
              ``notfound_packages``: List of names of packages that weren't found in any cog path
              ``alreadyloaded_packages``: List of names of packages that are already loaded
              ``failed_with_reason_packages``: Dictionary of packages that failed to load with
              a specified reason with mapping of package names -> failure reason
              ``repos_with_shared_libs``: List of repo names that use deprecated shared libraries
        """
        failed_packages = []
        loaded_packages = []
        invalid_pkg_names = []
        notfound_packages = []
        alreadyloaded_packages = []
        failed_with_reason_packages = {}
        repos_with_shared_libs = set()

        bot = self.bot

        pkg_specs = []

        for name in pkg_names:
            if not name.isidentifier() or keyword.iskeyword(name):
                invalid_pkg_names.append(name)
                continue
            try:
                spec = await bot._cog_mgr.find_cog(name)
                if spec:
                    pkg_specs.append((spec, name))
                else:
                    notfound_packages.append(name)
            except Exception as e:
                log.exception("Package import failed", exc_info=e)

                exception_log = "Exception during import of package\n"
                exception_log += "".join(traceback.format_exception(type(e), e, e.__traceback__))
                bot._last_exception = exception_log
                failed_packages.append(name)

        async for spec, name in AsyncIter(pkg_specs, steps=10):
            try:
                self._cleanup_and_refresh_modules(spec.name)
                await bot.load_extension(spec)
            except errors.PackageAlreadyLoaded:
                alreadyloaded_packages.append(name)
            except errors.CogLoadError as e:
                failed_with_reason_packages[name] = str(e)
            except Exception as e:
                if isinstance(e, commands.CommandRegistrationError):
                    if e.alias_conflict:
                        error_message = (
                            "Alias {alias_name} is already an existing command"
                            " or alias in one of the loaded cogs."
                        ).format(alias_name=inline(e.name))
                    else:
                        error_message = (
                            "Command {command_name} is already an existing command"
                            " or alias in one of the loaded cogs."
                        ).format(command_name=inline(e.name))
                    failed_with_reason_packages[name] = error_message
                    continue

                log.exception("Package loading failed", exc_info=e)

                exception_log = "Exception during loading of package\n"
                exception_log += "".join(traceback.format_exception(type(e), e, e.__traceback__))
                bot._last_exception = exception_log
                failed_packages.append(name)
            else:
                await bot.add_loaded_package(name)
                loaded_packages.append(name)
                # remove in Red 3.4
                downloader = bot.get_cog("Downloader")
                if downloader is None:
                    continue
                try:
                    maybe_repo = await downloader._shared_lib_load_check(name)
                except Exception:
                    log.exception(
                        "Shared library check failed,"
                        " if you're not using modified Downloader, report this issue."
                    )
                    maybe_repo = None
                if maybe_repo is not None:
                    repos_with_shared_libs.add(maybe_repo.name)

        return {
            "loaded_packages": loaded_packages,
            "failed_packages": failed_packages,
            "invalid_pkg_names": invalid_pkg_names,
            "notfound_packages": notfound_packages,
            "alreadyloaded_packages": alreadyloaded_packages,
            "failed_with_reason_packages": failed_with_reason_packages,
            "repos_with_shared_libs": list(repos_with_shared_libs),
        }


    async def load(self, ctx: commands.Context, *cogs: str):
        """Loads cog packages from the local paths and installed cogs.

        See packages available to load with `[p]cogs`.

        Additional cogs can be added using Downloader, or from local paths using `[p]addpath`.

        **Examples:**
            - `[p]load general` - Loads the `general` cog.
            - `[p]load admin mod mutes` - Loads multiple cogs.

        **Arguments:**
            - `<cogs...>` - The cog packages to load.
        """
        cogs = tuple(map(lambda cog: cog.rstrip(","), cogs))
        async with ctx.typing():
            outcomes = await self._load(cogs)

        output = []

        if loaded := outcomes["loaded_packages"]:
            loaded_packages = humanize_list([inline(package) for package in loaded])
            formed = ("Loaded {packs}.").format(packs=loaded_packages)
            output.append(formed)

        if already_loaded := outcomes["alreadyloaded_packages"]:
            if len(already_loaded) == 1:
                formed = ("The following package is already loaded: {pack}").format(
                    pack=inline(already_loaded[0])
                )
            else:
                formed = ("The following packages are already loaded: {packs}").format(
                    packs=humanize_list([inline(package) for package in already_loaded])
                )
            output.append(formed)

        if failed := outcomes["failed_packages"]:
            if len(failed) == 1:
                formed = (
                    "Failed to load the following package: {pack}."
                    "\nCheck your console or logs for details."
                ).format(pack=inline(failed[0]))
            else:
                formed = (
                    "Failed to load the following packages: {packs}"
                    "\nCheck your console or logs for details."
                ).format(packs=humanize_list([inline(package) for package in failed]))
            output.append(formed)

        if invalid_pkg_names := outcomes["invalid_pkg_names"]:
            if len(invalid_pkg_names) == 1:
                formed = (
                    "The following name is not a valid package name: {pack}\n"
                    "Package names cannot start with a number"
                    " and can only contain ascii numbers, letters, and underscores."
                ).format(pack=inline(invalid_pkg_names[0]))
            else:
                formed = (
                    "The following names are not valid package names: {packs}\n"
                    "Package names cannot start with a number"
                    " and can only contain ascii numbers, letters, and underscores."
                ).format(packs=humanize_list([inline(package) for package in invalid_pkg_names]))
            output.append(formed)

        if not_found := outcomes["notfound_packages"]:
            if len(not_found) == 1:
                formed = ("The following package was not found in any cog path: {pack}.").format(
                    pack=inline(not_found[0])
                )
            else:
                formed = (
                    "The following packages were not found in any cog path: {packs}"
                ).format(packs=humanize_list([inline(package) for package in not_found]))
            output.append(formed)

        if failed_with_reason := outcomes["failed_with_reason_packages"]:
            reasons = "\n".join([f"`{x}`: {y}" for x, y in failed_with_reason.items()])
            if len(failed_with_reason) == 1:
                formed = (
                    "This package could not be loaded for the following reason:\n\n{reason}"
                ).format(reason=reasons)
            else:
                formed = (
                    "These packages could not be loaded for the following reasons:\n\n{reasons}"
                ).format(reasons=reasons)
            output.append(formed)

        if repos_with_shared_libs := outcomes["repos_with_shared_libs"]:
            if len(repos_with_shared_libs) == 1:
                formed = (
                    "**WARNING**: The following repo is using shared libs"
                    " which are marked for removal in the future: {repo}.\n"
                    "You should inform maintainer of the repo about this message."
                ).format(repo=inline(repos_with_shared_libs.pop()))
            else:
                formed = (
                    "**WARNING**: The following repos are using shared libs"
                    " which are marked for removal in the future: {repos}.\n"
                    "You should inform maintainers of these repos about this message."
                ).format(repos=humanize_list([inline(repo) for repo in repos_with_shared_libs]))
            output.append(formed)

        if output:
            total_message = "\n\n".join(output)
            for page in pagify(
                total_message, delims=["\n", ", "], priority=True, page_length=1500
            ):
                if page.startswith(", "):
                    page = page[2:]
                await ctx.send(page)

    async def _unload(self, pkg_names: Iterable[str]) -> Dict[str, List[str]]:
        """
        Unloads packages with the given names.

        Parameters
        ----------
        pkg_names : `list` of `str`
            List of names of packages to unload.

        Returns
        -------
        dict
            Dictionary with keys:
              ``unloaded_packages``: List of names of packages that unloaded successfully.
              ``notloaded_packages``: List of names of packages that weren't unloaded
              because they weren't loaded.
        """
        notloaded_packages = []
        unloaded_packages = []

        bot = self.bot

        for name in pkg_names:
            if name in bot.extensions:
                bot.unload_extension(name)
                await bot.remove_loaded_package(name)
                unloaded_packages.append(name)
            else:
                notloaded_packages.append(name)

        return {"unloaded_packages": unloaded_packages, "notloaded_packages": notloaded_packages}

    async def unload(self, ctx: commands.Context, *cogs: str):
        """Unloads previously loaded cog packages.

        See packages available to unload with `[p]cogs`.

        **Examples:**
            - `[p]unload general` - Unloads the `general` cog.
            - `[p]unload admin mod mutes` - Unloads multiple cogs.

        **Arguments:**
            - `<cogs...>` - The cog packages to unload.
        """
        cogs = tuple(map(lambda cog: cog.rstrip(","), cogs))
        outcomes = await self._unload(cogs)

        output = []

        if unloaded := outcomes["unloaded_packages"]:
            if len(unloaded) == 1:
                formed = ("The following package was unloaded: {pack}.").format(
                    pack=inline(unloaded[0])
                )
            else:
                formed = ("The following packages were unloaded: {packs}.").format(
                    packs=humanize_list([inline(package) for package in unloaded])
                )
            output.append(formed)

        if failed := outcomes["notloaded_packages"]:
            if len(failed) == 1:
                formed = ("The following package was not loaded: {pack}.").format(
                    pack=inline(failed[0])
                )
            else:
                formed = ("The following packages were not loaded: {packs}.").format(
                    packs=humanize_list([inline(package) for package in failed])
                )
            output.append(formed)

        if output:
            total_message = "\n\n".join(output)
            for page in pagify(total_message):
                await ctx.send(page)

    async def get_cog(self, ctx: commands.Context,  name=""):
        t = await self.config.member(ctx.author).name()
        for c in t:
            print(f'c = {str(c)} \n {str(t)}')
            if c[0] == name:
                return c
        return None
    
    @commands.command()
    @checks.is_owner()
    async def testing(self, ctx: commands.Context, *cog: str):
        
        cgs = await self.config.member(ctx.author).name()
        print(cgs)
        cogs = []
        if cgs is not None:
            cogs.extend(cgs)
        else:
            cgs = cog

            for c in cgs:
                cogs.append(c[0])
            if cgs is None:
                loaded = list(self.bot.extensions.keys())
                print('loaded = ' + str(loaded))
                temp = []
                for l in loaded:
                    temp.append((loaded, "prod"))
                    cogs.append(l)
                await self.config.member(ctx.author).name.set(temp)


                
        for c in cog:
            cgs = cogs
            if c not in cogs:
                print("9999999999\n" + str(cogs))
                await ctx.send(f"{c} not in cogs, create new testing instance? (yes/no)")
                
                pred = MessagePredicate.yes_or_no(ctx)        
                event = "message"
                try:
                    await ctx.bot.wait_for(event, check=pred, timeout=30)
                except asyncio.TimeoutError:
                    with contextlib.suppress(discord.NotFound):
                        await query.delete()
                    return
                if pred.result:
                    if not os.path.exists(str(self.root_path) + c +"/test" + str(ctx.author.id) + "/"):
                        print("doesn\'t exist path")
                        os.mkdir(str(self.root_path) + c +"/test"+ str(ctx.author.id) + "/")
                        if not os.path.exists(str(self.root_path) + c +"/test"+ str(ctx.author.id) + "/" + c + ".py"):
                            print("doesn\'t exist path")
                            shutil.copy2(str(self.root_path) + c +"/" + c + ".py", str(self.root_path) + c +"/test"+ str(ctx.author.id) + "/"+ c + ".py")
                            temp = await self.config.member(ctx.author).name()
                            temp.append((c, "testing"))
                            await self.config.member(ctx.author).name.set(temp)
                            continue
                   
                else:
                    return
            else:
                state = self.get_cog(ctx, c)[1]
                if state[1] == "prod":
                    print("in prod")
                    shutil.copy(str(self.root_path) + c +"/" + c + ".py",str(self.root_path) + c +"/" + c + "2.py")
                    await asyncio.sleep(1)
                    os.remove(str(self.root_path) + c +"/" + c + ".py")
                    await asyncio.sleep(1)
                    shutil.copy(str(self.root_path) + c +"/test" +  str(ctx.author.id) + "/" + c + ".py",str(self.root_path) + c +"/" + c + ".py")
                    os.remove(str(self.root_path) + c +"/test" +  str(ctx.author.id) + "/" + c + ".py")
                    

                    
                    
                    print(str(os.path.dirname(str(self.root_path) + c +"/" + c + ".py")) + " else " + str(self.root_path) + c +"/" + c + ".py")

                    


                elif state[1] == "testing":
                    shutil.copy(str(self.root_path) + c +"/test" +  str(ctx.author.id) + "/" + c + ".py",str(self.root_path) + c +"/test" +  str(ctx.author.id) + "/" + c + "2.py")
                    await asyncio.sleep(1)
                    os.rename(str(self.root_path) + c +"/" + c + "2.py", str(self.root_path) + c +"/test"+ str(ctx.author.id) + "/" + c + "2.py")
                    await asyncio.sleep(1)
                    shutil.copy2(str(self.root_path) + c +"/test"+ str(ctx.author.id) + "/" + c + ".py", str(self.root_path) + c +"/" + c + ".py")
                    os.rename(str(self.root_path) + c +"/test"+ str(ctx.author.id) + "/" + c + "2.py", str(self.root_path) + c +"/test"+ str(ctx.author.id) + "/" + c + ".py")
                    await asyncio.sleep(1)

                    print(str(os.path.dirname(str(self.root_path) + c +"/" + c + ".py")) + " else " + str(self.root_path) + c +"/" + c + ".py")
                await self.unload(ctx,c)
                await self.load(ctx, c)

           
               
        