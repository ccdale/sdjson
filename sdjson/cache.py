#
# Copyright (c) 2021, Christopher Allison
#
#     This file is part of ccasdtv.
#
#     ccasdtv is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     ccasdtv is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with ccasdtv.  If not, see <http://www.gnu.org/licenses/>.
"""Cache functions for ccasdtv."""

from pathlib import Path
import sys

import ccalogging

log = ccalogging.log


def getCacheDir(appname="ccasdtv"):
    try:
        home = Path.home()
        cachedir = home.joinpath(f".{appname}")
        return cachedir
    except Exception as e:
        exci = sys.exc_info()[2]
        lineno = exci.tb_lineno
        fname = exci.tb_frame.f_code.co_name
        ename = type(e).__name__
        msg = f"{ename} Exception at line {lineno} in function {fname}: {e}"
        log.error(msg)
        raise


def getDescendingDir(name):
    """Make a path like string of the 1st 4 chars of name."""
    try:
        # name is the md5 sum of the program data
        # use the 1st 4 characters of the name to make descending
        # directories for the cache.
        hold = ""
        tree = []
        for i in range(4):
            hold += name[i]
            tree.append(hold)
        return "/".join(tree)
    except Exception as e:
        exci = sys.exc_info()[2]
        lineno = exci.tb_lineno
        fname = exci.tb_frame.f_code.co_name
        ename = type(e).__name__
        msg = f"{ename} Exception at line {lineno} in function {fname}: {e}"
        log.error(msg)
        raise


def makeCacheDir(name, dtype="program", appname="ccasdtv"):
    """Makes the cache directories for the ccasdtv application."""
    try:
        home = Path.home()
        cachedir = getCacheDir(appname)
        if dtype == "cache":
            home.mkdir(cachedir, parents=True, exist_ok=True)
            return cachedir
        elif dtype == "channel":
            chandir = home.joinpath(cachedir, "channel", name)
            home.mkdir(chandir, parents=True, exist_ok=True)
            return chandir
        elif dtype == "program":
            pdir = home.joinpath(cachedir, "program", getDescendingDir(name))
            home.mkdir(pdir, parents=True, exist_ok=True)
            return pdir
    except Exception as e:
        exci = sys.exc_info()[2]
        lineno = exci.tb_lineno
        fname = exci.tb_frame.f_code.co_name
        ename = type(e).__name__
        msg = f"{ename} Exception at line {lineno} in function {fname}: {e}"
        log.error(msg)
        raise


def setupCache(appname="ccasdtv"):
    """Sets up the cache directories for the ccasdtv application."""
    try:
        cachedict = {}
        cachedict["cachedir"] = makeCacheDir("cache", dtype="cache", appname=appname)
        cachedict["chandir"] = makeCacheDir(
            "channels", dtype="channel", appname=appname
        )
        cachedict["progdir"] = makeCacheDir(
            "programs", dtype="program", appname=appname
        )
        return cachedict
    except Exception as e:
        exci = sys.exc_info()[2]
        lineno = exci.tb_lineno
        fname = exci.tb_frame.f_code.co_name
        ename = type(e).__name__
        msg = f"{ename} Exception at line {lineno} in function {fname}: {e}"
        log.error(msg)
        raise
