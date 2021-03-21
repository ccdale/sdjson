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

    def writeChannelSchedule(self, chanid, scheddata):
        try:
            # chanid = scheddata["stattionID"]
            xdir = self.setupChannelDir(chanid)
            cfn = xdir.joinpath(f"""{chanid}-schedule.json""")
            log.debug(f"saving schedule data to {cfn}")
            with open(cfn, "w") as ofn:
                json.dump(scheddata, ofn, separators=(",", ":"))
        except Exception as e:
            exci = sys.exc_info()[2]
            lineno = exci.tb_lineno
            fname = exci.tb_frame.f_code.co_name
            ename = type(e).__name__
            msg = f"{ename} Exception at line {lineno} in function {fname}: {e}"
            log.error(msg)
            raise

    def readChannelSchedule(self, chanid):
        try:
            jdata = None
            xdir = self.setupChannelDir(chanid)
            cfn = xdir.joinpath(f"""{chanid}-schedule.json""")
            if cfn.exists():
                with open(cfn, "r") as ifn:
                    jdata = json.load(ifn)
            return jdata
        except Exception as e:
            exci = sys.exc_info()[2]
            lineno = exci.tb_lineno
            fname = exci.tb_frame.f_code.co_name
            ename = type(e).__name__
            msg = f"{ename} Exception at line {lineno} in function {fname}: {e}"
            log.error(msg)
            raise

    def writeChannelMd5(self, chanid, md5data):
        try:
            # chanid = md5data["stattionID"]
            xdir = self.setupChannelDir(chanid)
            cfn = xdir.joinpath(f"""{chanid}-schedule-md5.json""")
            log.debug(f"saving md5 data to {cfn}")
            with open(cfn, "w") as ofn:
                json.dump(md5data, ofn, separators=(",", ":"))
        except Exception as e:
            exci = sys.exc_info()[2]
            lineno = exci.tb_lineno
            fname = exci.tb_frame.f_code.co_name
            ename = type(e).__name__
            msg = f"{ename} Exception at line {lineno} in function {fname}: {e}"
            log.error(msg)
            raise

    def readChannelMd5(self, chanid):
        try:
            jdata = None
            xdir = self.setupChannelDir(chanid)
            cfn = xdir.joinpath(f"""{chanid}-schedule-md5.json""")
            if cfn.exists():
                with open(cfn, "r") as ifn:
                    jdata = json.load(ifn)
            return jdata
        except Exception as e:
            exci = sys.exc_info()[2]
            lineno = exci.tb_lineno
            fname = exci.tb_frame.f_code.co_name
            ename = type(e).__name__
            msg = f"{ename} Exception at line {lineno} in function {fname}: {e}"
            log.error(msg)
            raise

    def writeChannelToCache(self, chandata, overwrite=False):
        try:
            xdir = self.setupChannelDir(chandata["stationID"])
            channelfilename = xdir.joinpath(f"""{chandata["stationID"]}.json""")
            if overwrite or not Path.exists(channelfilename):
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

    def readChannelDataById(self, chanid):
        try:
            cdata = None
            xdir = self.setupChannelDir(chanid)
            channelfilename = xdir.joinpath(f"{chanid}.json")
            if channelfilename.exists():
                with open(channelfilename, "r") as cfn:
                    cdata = json.load(cfn)
            return cdata
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

    def writeLineupData(self, lineupid, ldata):
        try:
            cachedir = self.getCacheDir()
            lineupfn = cachedir.joinpath(f"{lineupid}.json")
            with open(lineupfn, "w") as lfn:
                json.dump(ldata, lfn, separators=(",", ":"))
        except Exception as e:
            exci = sys.exc_info()[2]
            lineno = exci.tb_lineno
            fname = exci.tb_frame.f_code.co_name
            ename = type(e).__name__
            msg = f"{ename} Exception at line {lineno} in function {fname}: {e}"
            print(msg)
            raise

    def readLineupData(self, lineupid):
        try:
            ldata = None
            cachedir = self.getCacheDir()
            lineupfn = cachedir.joinpath(f"{lineupid}.json")
            if Path.exists(lineupfn):
                log.debug(f"Reading lineup file {lineupfn}")
                with open(lineupfn, "r") as lfn:
                    ldata = json.load(lfn)
            else:
                raise Exception(f"lineup path {lineupfn} does not exist")
            return ldata
        except Exception as e:
            exci = sys.exc_info()[2]
            lineno = exci.tb_lineno
            fname = exci.tb_frame.f_code.co_name
            ename = type(e).__name__
            msg = f"{ename} Exception at line {lineno} in function {fname}: {e}"
            print(msg)
            raise
