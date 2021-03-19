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
"""ccasdtv personal tv guide application."""

import hashlib
from pathlib import Path
import sys

import ccalogging
import PySimpleGUI as sg

from sdjson.cache import SDCache
import sdjson.config as CFG
from sdjson.lineup import parseLineupData
from sdjson.sdapi import SDApi
from sdjson import __version__

appname = "ccasdtv"
home = Path.home()

logfilename = home.joinpath(f".{appname}.log")
ccalogging.setLogFile(logfilename)
ccalogging.setDebug()
log = ccalogging.log


def usernamePassword(username=""):
    try:
        layout = [
            [sg.T("SD Username"), sg.I(username, key="UIN")],
            [sg.T("SD Password"), sg.I(key="PIN")],
            # [sg.CB("Save password in config file", default=True, key="SPW")],
            [sg.Submit(key="submit"), sg.Cancel(key="cancel")],
        ]
        window = sg.Window("Schedules Direct Credentials.", layout)
        event, values = window.read()
        window.close()
        # un = pw = chkbx = None
        un = pw = None
        if event == "submit":
            un = values["UIN"]
            pw = values["PIN"]
            # chkbx = values["SPW"]
        log.debug(f"event: {event}, values: {values}")
        # return un, pw, chkbx
        return un, pw
    except Exception as e:
        exci = sys.exc_info()[2]
        lineno = exci.tb_lineno
        fname = exci.tb_frame.f_code.co_name
        ename = type(e).__name__
        msg = f"{ename} Exception at line {lineno} in function {fname}: {e}"
        log.error(msg)
        raise


def testCredsConfig(cfg):
    try:
        needconfig = False
        if "password" not in cfg:
            needconfig = True
        if "username" not in cfg:
            needconfig = True
            username = ""
        else:
            username = cfg["username"]
        if needconfig:
            log.debug("Configuration required")
            # username, password, storepw = usernamePassword(username)
            username, password = usernamePassword(username)
            if username:
                cfg["username"] = username
                cfg["amdirty"] = True
            # if password and storepw:
            if password:
                cfg["password"] = hashlib.sha1(password.encode()).hexdigest()
                cfg["amdirty"] = True
        if "password" not in cfg or "username" not in cfg:
            raise Exception(
                "Username and/or Password for Schedulesdirect not supplied."
            )
        return cfg
    except Exception as e:
        exci = sys.exc_info()[2]
        lineno = exci.tb_lineno
        fname = exci.tb_frame.f_code.co_name
        ename = type(e).__name__
        msg = f"{ename} Exception at line {lineno} in function {fname}: {e}"
        log.error(msg)
        raise


def fillDict(keys, xdict, odict=None):
    try:
        if not odict:
            odict = {}
        for key in keys:
            if key in xdict:
                odict[key] = xdict[key]
        return odict
    except Exception as e:
        exci = sys.exc_info()[2]
        lineno = exci.tb_lineno
        fname = exci.tb_frame.f_code.co_name
        ename = type(e).__name__
        msg = f"{ename} Exception at line {lineno} in function {fname}: {e}"
        log.error(msg)
        raise


def errorWindow(emsg):
    try:
        layout = [[sg.T(emsg)], [sg.Cancel()]]
        win = sg.Window("Error", layout)
        event, values = win.read()
        win.close()
    except Exception as e:
        exci = sys.exc_info()[2]
        lineno = exci.tb_lineno
        fname = exci.tb_frame.f_code.co_name
        ename = type(e).__name__
        msg = f"{ename} Exception at line {lineno} in function {fname}: {e}"
        log.error(msg)
        raise


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


def channelSelector(cfg, chandata):
    try:
        cns = chandata["channelsbyname"]
        selchans = [] if "channels" not in cfg else cfg["channels"]
        unselchans = [f"""{cns[x]["stationID"]:7} {x}""" for x in sorted(cns)]
        # unselchans = [x for x in sorted(chandata["channelsbyname"])]
        layout = [
            [sg.T("Available Channels"), sg.T("Selected Channels")],
            [
                sg.Listbox(
                    values=unselchans,
                    size=(50, 40),
                    key="ULB",
                    select_mode="multiple",
                ),
                sg.Listbox(
                    values=selchans, size=(50, 40), key="SLB", select_mode="multiple"
                ),
            ],
            [sg.Button("Move"), sg.Cancel("Save"), sg.Cancel()],
        ]
        log.debug("Creating Window")
        win = sg.Window("Select a Channel", layout)
        while True:
            log.debug("reading Window")
            event, values = win.read()
            log.debug(f"event: {event}, values: {values}")
            if event == "Move":
                if "ULB" in values:
                    for val in values["ULB"]:
                        unselchans.remove(val)
                    win["ULB"].update(unselchans)
                    selchans.extend(values["ULB"])
                    win["SLB"].update(selchans)
            else:
                break
        win.close()
        cfg["channels"] = selchans
        cfg["amdirty"] = True
        return cfg
    except Exception as e:
        exci = sys.exc_info()[2]
        lineno = exci.tb_lineno
        fname = exci.tb_frame.f_code.co_name
        ename = type(e).__name__
        msg = f"{ename} Exception at line {lineno} in function {fname}: {e}"
        log.error(msg)
        raise


def gRun():
    try:
        log.info(f"{appname} {__version__} starting.")
        needconfig = False
        ckwargs = {"appname": appname}
        cfg = CFG.readConfig(**ckwargs)
        cfg = testCredsConfig(cfg)
        sdc = SDCache(**ckwargs)
        sdc.setupCache()
        ckwargs = fillDict(
            ["username", "password", "token", "tokenexpires"], cfg, ckwargs
        )
        sd = SDApi(**ckwargs)
        sd.apiOnline()
        if not sd.online:
            errorWindow(sd.statusmsg)
            sys.exit(1)
        if "lineups" in cfg and sd.lineups is not None:
            xlineups = []
            for lineup in cfg["lineups"]:
                xlineups.append(checkLineup(sd, sdc, lineup))
                cfg["amdirty"] = True
            cfg["lineups"] = xlineups
        for lineup in cfg["lineups"]:
            ldata = sdc.readLineupData(lineup["lineupid"])
            log.debug(f"""writing lineup data to disk for {lineup["lineupid"]}""")
            for chan in ldata["channelsbyid"]:
                sdc.writeChannelToCache(ldata["channelsbyid"][chan])
            log.debug("lineup data write completed.")
        cfg = channelSelector(cfg, ldata)
        ckwargs = {"appname": appname}
        CFG.writeConfig(cfg, **ckwargs)
    except Exception as e:
        exci = sys.exc_info()[2]
        lineno = exci.tb_lineno
        fname = exci.tb_frame.f_code.co_name
        ename = type(e).__name__
        msg = f"{ename} Exception at line {lineno} in function {fname}: {e}"
        log.error(msg)
        layout = [[sg.T(msg)], [sg.Cancel()]]
        window = sg.Window("An Error Occurred.", layout)
        event, values = window.read()
        window.close()
        sys.exit(1)
