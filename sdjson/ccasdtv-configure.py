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

import hashlib
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


def configure():
    f"""Sets up the configuration for the {appname} application."""
    try:
        log.info(f"{appname} {__version__} configuration routine starting.")
        ckwargs = {"appname": appname}
        cfg = CFG.readConfig(**ckwargs)
        cfg = confUser(cfg)
        sd = testCreds(cfg["username"], cfg["password"])
        cfg["amdirty"] = True
        cfg["token"] = sd.token
        cfg["tokenexpires"] = sd.tokenexpires
        sdc = SDCache(**ckwargs)
        sdc.setupCache()
        cfg["lineups"] = []
        if sd.lineups is not None:
            for lu in sd.lineups:
                ldata = parseLineupData(sd.getLineup(lu["lineupID"]))
                lineup = {"lineupid": lu["lineupID"], "modified": ldata["modified"]}
                cfg["lineups"].append(lineup)
                sdc.writeLineupData(lu["lineupID"], ldata)
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
