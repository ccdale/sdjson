#!/usr/bin/env python3

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
"""Configuration for the ccasdtv application."""

from pathlib import Path
import sys

import ccalogging

from sdjson.cache import SDCache
import sdjson.config as CFG
from sdjson.lineup import parseLineupData
from sdjson.sdapi import SDApi
from sdjson.sduser import confUser
from sdjson.sduser import testCreds
from sdjson import __version__

appname = "ccasdtv"
home = Path.home()

logfilename = home.joinpath(f".{appname}.log")
ccalogging.setLogFile(logfilename)
ccalogging.setDebug()
log = ccalogging.log


def checkLineup(sd, sdc, cfglineup):
    """Checks that the lineup is not out of date."""
    try:
        for slu in sd.lineups:
            if cfglineup["lineupid"] == slu["lineupID"]:
                lum = sd.getTimeStamp(slu["modified"])
                if int(cfglineup["modified"]) < lum:
                    log.info(
                        f"""Lineup {slu["lineupID"]} is out of date, retrieving fresh data."""
                    )
                    ldata = parseLineupData(sd.getLineup(slu["lineupID"]))
                    sdc.writeLineupData(slu["lineupID"], ldata)
                    cfglineup["modified"] = lum
        return cfglineup
    except Exception as e:
        exci = sys.exc_info()[2]
        lineno = exci.tb_lineno
        fname = exci.tb_frame.f_code.co_name
        ename = type(e).__name__
        msg = f"{ename} Exception at line {lineno} in function {fname}: {e}"
        print(msg)
        raise


def configure():
    f"""Sets up the configuration for the {appname} application."""
    try:
        log.info(f"{appname} {__version__} configuration routine starting.")
        ckwargs = {"appname": appname}
        cfg = CFG.readConfig(**ckwargs)
        cfg = confUser(cfg)
        if "token" not in cfg:
            cfg["token"] = "X"
            cfg["tokenexpires"] = 0
        sd = testCreds(
            cfg["username"], cfg["password"], cfg["token"], cfg["tokenexpires"]
        )
        sys.exit(0)
        cfg["amdirty"] = True
        cfg["token"] = sd.token
        cfg["tokenexpires"] = sd.tokenexpires
        sdc = SDCache(**ckwargs)
        sdc.setupCache()
        # check that the lineup is not out of date
        if "lineups" in cfg and sd.lineups is not None:
            xlineups = []
            for lineup in cfg["lineups"]:
                xlineups.append(checkLineup(sd, sdc, lineup))
                cfg["amdirty"] = True
            cfg["lineups"] = xlineups
        CFG.writeConfig(cfg, **ckwargs)
    except Exception as e:
        exci = sys.exc_info()[2]
        lineno = exci.tb_lineno
        fname = exci.tb_frame.f_code.co_name
        ename = type(e).__name__
        msg = f"{ename} Exception at line {lineno} in function {fname}: {e}"
        log.error(msg)
        print(f"{e}")
        sys.exit(1)
