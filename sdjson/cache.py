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

# TODO test this class
class SDCache:
    """Cache class for the ccasdtv application."""

    def __init__(self, appname="ccasdtv"):
        try:
            self.cachedict = None
            self.appname = appname
        except Exception as e:
            exci = sys.exc_info()[2]
            lineno = exci.tb_lineno
            fname = exci.tb_frame.f_code.co_name
            ename = type(e).__name__
            msg = f"{ename} Exception at line {lineno} in function {fname}: {e}"
            log.error(msg)
            raise

    def getCacheDir(self):
        try:
            home = Path.home()
            cachedir = home.joinpath(f".{self.appname}")
            log.debug(f"setting cache directory to be: {cachedir}")
            return cachedir
        except Exception as e:
            exci = sys.exc_info()[2]
            lineno = exci.tb_lineno
            fname = exci.tb_frame.f_code.co_name
            ename = type(e).__name__
            msg = f"{ename} Exception at line {lineno} in function {fname}: {e}"
            log.error(msg)
            raise

    def getDescendingDir(self, name):
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
            xs = "/".join(tree)
            log.debug(f"built path {xs}")
            return xs
        except Exception as e:
            exci = sys.exc_info()[2]
            lineno = exci.tb_lineno
            fname = exci.tb_frame.f_code.co_name
            ename = type(e).__name__
            msg = f"{ename} Exception at line {lineno} in function {fname}: {e}"
            log.error(msg)
            raise

    def makeCacheDir(self, name=None, dtype="program"):
        """Makes the cache directories for the ccasdtv application."""
        try:
            home = Path.home()
            cachedir = self.getCacheDir()
            if dtype == "cache":
                log.debug(f"making directory {cachedir}")
                cachedir.mkdir(parents=True, exist_ok=True)
                return cachedir
            elif dtype == "channel":
                chandir = cachedir.joinpath("channel")
                log.debug(f"making directory {chandir}")
                chandir.mkdir(parents=True, exist_ok=True)
                return chandir
            elif dtype == "program":
                if name is not None:
                    pdir = cachedir.joinpath("program", getDescendingDir(name))
                else:
                    pdir = cachedir.joinpath("program")
                log.debug(f"making directory {pdir}")
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

    def setupCache(self):
        """Sets up the cache directories for the ccasdtv application."""
        try:
            # global cachedict
            log.debug("Setting up cache locations")
            self.cachedict = {}
            self.cachedict["cachedir"] = self.makeCacheDir(dtype="cache")
            self.cachedict["chandir"] = self.makeCacheDir(dtype="channel")
            self.cachedict["progdir"] = self.makeCacheDir(dtype="program")
        except Exception as e:
            exci = sys.exc_info()[2]
            lineno = exci.tb_lineno
            fname = exci.tb_frame.f_code.co_name
            ename = type(e).__name__
            msg = f"{ename} Exception at line {lineno} in function {fname}: {e}"
            log.error(msg)
            raise

    def setupChannelDir(self, stationid):
        try:
            if self.cachedict is None:
                raise Exception("Cache dictionary has not been setup")
            xdir = self.cachedict["chandir"].joinpath(stationid)
            log.debug(f"creating directory {xdir}")
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

    def writeChannelToCache(self, chandata):
        try:
            xdir = self.setupChannelDir(chandata["stationID"])
            channelfilename = xdir.joinpath(f"""{chandata["stationID"]}.json""")
            log.debug(f"saving channel data to {channelfilename}")
            with open(channelfilename, "w") as cfn:
                json.dump(chandata, cfn, separators=(",", ":"))
        except Exception as e:
            exci = sys.exc_info()[2]
            lineno = exci.tb_lineno
            fname = exci.tb_frame.f_code.co_name
            ename = type(e).__name__
            msg = f"{ename} Exception at line {lineno} in function {fname}: {e}"
            log.error(msg)
            raise

    def writeChannelScheduleToCache(self, stationid, chansched):
        try:
            xdir = self.setupChannelDir(stationid)
            schedfilename = xdir.joinpath("schedule.json")
            log.debug(f"writing schedule data to {schedfilename}")
            with open(schedfilename, "w") as cfn:
                json.dump(chansched, cfn, separators=(",", ":"))
        except Exception as e:
            exci = sys.exc_info()[2]
            lineno = exci.tb_lineno
            fname = exci.tb_frame.f_code.co_name
            ename = type(e).__name__
            msg = f"{ename} Exception at line {lineno} in function {fname}: {e}"
            log.error(msg)
            raise

    def writeLineupData(self, linupid, ldata):
        try:
            cachedir = self.getCacheDir()
            lineupfn = cachedir.joinpath(f"{lineupid}.json")
            with open(lineupfn, "w") as lfn:
                json.dump(ldata, xfn, seperators=(",", ":"))
        except Exception as e:
            exci = sys.exc_info()[2]
            lineno = exci.tb_lineno
            fname = exci.tb_frame.f_code.co_name
            ename = type(e).__name__
            msg = f"{ename} Exception at line {lineno} in function {fname}: {e}"
            print(msg)
            raise
