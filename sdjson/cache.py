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

import json
from pathlib import Path
import sys

import ccalogging

log = ccalogging.log

cachedict = None


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


def makeCacheDir(name=None, dtype="program", appname="ccasdtv"):
    """Makes the cache directories for the ccasdtv application."""
    try:
        home = Path.home()
        cachedir = getCacheDir(appname)
        if dtype == "cache":
            cachedir.mkdir(parents=True, exist_ok=True)
            return cachedir
        elif dtype == "channel":
            chandir = cachedir.joinpath("channel")
            chandir.mkdir(parents=True, exist_ok=True)
            return chandir
        elif dtype == "program":
            if name is not None:
                pdir = cachedir.joinpath("program", getDescendingDir(name))
            else:
                pdir = cachedir.joinpath("program")
            pdir.mkdir(parents=True, exist_ok=True)
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
        cachedict["cachedir"] = makeCacheDir(dtype="cache", appname=appname)
        cachedict["chandir"] = makeCacheDir(dtype="channel", appname=appname)
        cachedict["progdir"] = makeCacheDir(dtype="program", appname=appname)
    except Exception as e:
        exci = sys.exc_info()[2]
        lineno = exci.tb_lineno
        fname = exci.tb_frame.f_code.co_name
        ename = type(e).__name__
        msg = f"{ename} Exception at line {lineno} in function {fname}: {e}"
        log.error(msg)
        raise


def setupChannelDir(stationid):
    try:
        if cachedict is None:
            raise Exception("Cache dictionary has not been setup")
        xdir = cachedict["chandir"].joinpath(stationid)
        xdir.mkdir(exist_ok=True)
        return xdir
    except Exception as e:
        exci = sys.exc_info()[2]
        lineno = exci.tb_lineno
        fname = exci.tb_frame.f_code.co_name
        ename = type(e).__name__
        msg = f"{ename} Exception at line {lineno} in function {fname}: {e}"
        log.error(msg)
        raise


def writeChannelToCache(chandata):
    try:
        print(chandata)
        xdir = setupChannelDir(chandata["stationID"])
        channelfilename = xdir.joinpath(f"""{chandata["stationID"]}.json""")
        with open(channelfilename, "w") as cfn:
            json.dump(chandata, cfn, seperators=(",", ":"))
    except Exception as e:
        exci = sys.exc_info()[2]
        lineno = exci.tb_lineno
        fname = exci.tb_frame.f_code.co_name
        ename = type(e).__name__
        msg = f"{ename} Exception at line {lineno} in function {fname}: {e}"
        log.error(msg)
        raise


def writeChannelScheduleToCache(stationid, chansched):
    try:
        xdir = setupChannelDir(stationid)
        schedfilename = xdir.joinpath("schedule.json")
        with open(schedfilename, "w") as cfn:
            json.dump(chansched, cfn, seperators=(",", ":"))
    except Exception as e:
        exci = sys.exc_info()[2]
        lineno = exci.tb_lineno
        fname = exci.tb_frame.f_code.co_name
        ename = type(e).__name__
        msg = f"{ename} Exception at line {lineno} in function {fname}: {e}"
        log.error(msg)
        raise
