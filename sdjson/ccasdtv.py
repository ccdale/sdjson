#!/usr/bin/env python3
"""CLI for ccasdtv."""

import hashlib
from pathlib import Path
import sys

import ccalogging
import click

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

# blank line to mark the beginning of a run in the log file
log.info("")
log.info(f"{appname} {__version__} CLI Starting")

# TODO use the new cache class


@click.group()
def cli():
    pass


def askCredentials():
    try:
        uname = input("Schedules Direct username: ")
        password = input("SD Password: ")
        pword = hashlib.sha1(password.encode()).hexdigest()
        return (uname, pword)
    except Exception as e:
        exci = sys.exc_info()[2]
        lineno = exci.tb_lineno
        fname = exci.tb_frame.f_code.co_name
        ename = type(e).__name__
        msg = f"{ename} Exception at line {lineno} in function {fname}: {e}"
        # print(msg)
        log.error(msg)
        raise


def testCreds(uname, pword):
    try:
        sd = SDApi(uname, pword)
        sd.apiOnline()
        if not sd.online:
            print(sd.statusmsg)
            raise Exception("Schedules Direct is not online")
        log.debug("Supplied credentials appear to be correct")
        return sd
    except Exception as e:
        exci = sys.exc_info()[2]
        lineno = exci.tb_lineno
        fname = exci.tb_frame.f_code.co_name
        ename = type(e).__name__
        msg = f"{ename} Exception at line {lineno} in function {fname}: {e}"
        # print(msg)
        log.error(msg)
        raise


# @click.command()
def doConfigure():
    try:
        kwargs = {"appname": appname}
        cfg = CFG.readConfig(**kwargs)
        cfg["amdirty"] = False
        sd = testCreds(cfg["username"], cfg["password"])
        CFG.writeConfig(cfg, **kwargs)
    except Exception as e:
        exci = sys.exc_info()[2]
        lineno = exci.tb_lineno
        fname = exci.tb_frame.f_code.co_name
        ename = type(e).__name__
        msg = f"{ename} Exception at line {lineno} in function {fname}: {e}"
        log.error(msg)
        print("An Error occurred, see log file for details")
        sys.exit(1)


def setupSD(cfg):
    try:
        kwargs = {"appname": appname}
        # keymap = {"password": "sha1password"}
        keys = ["username", "password", "url", "token", "tokenexpires"]
        for key in keys:
            # xkey = keymap[key] if key in keymap else key
            if key in cfg:
                kwargs[xkey] = cfg[key]
        sd = SDApi(**kwargs)
        sd.apiOnline()
        if cfg["token"] != sd.token:
            cfg["token"] = sd.token
            cfg["tokenexpires"] = sd.tokenexpires
            cfg["amdirty"] = True
        return sd
    except Exception as e:
        exci = sys.exc_info()[2]
        lineno = exci.tb_lineno
        fname = exci.tb_frame.f_code.co_name
        ename = type(e).__name__
        msg = f"{ename} Exception at line {lineno} in function {fname}: {e}"
        log.error(msg)
        raise


def getSchedules():
    try:
        ckwargs = {"appname": appname}
        cfg = CFG.readConfig(**ckwargs)
        cfg["amdirty"] = False
        sd = setupSD(cfg)
        if cachedict is None:
            setupCache(appname=appname)
        if sd.lineups is not None:
            for lineup in sd.lineups:
                print(lineup)
                break
                ljson = sd.getLineup(lineup["lineupID"])
                channeldict = parseLineupData(ljson)
                byid = channeldict["channelsbyid"]
                for chan in byid:
                    writeChannelToCache(byid[chan])

        CFG.writeConfig(cfg, **ckwargs)
    except Exception as e:
        exci = sys.exc_info()[2]
        lineno = exci.tb_lineno
        fname = exci.tb_frame.f_code.co_name
        ename = type(e).__name__
        msg = f"{ename} Exception at line {lineno} in function {fname}: {e}"
        log.error(msg)
        print("An Error occurred, see log file for details")
        sys.exit(1)


@click.command()
def run():
    """Retrieves listings from Schedules Direct"""
    try:
        ckwargs = {"appname": appname}
        cfg = CFG.readConfig(**ckwargs)
        if "username" not in cfg:
            msg = f"You will need to configure {appname} before using it."
            print(msg)
            sys.exit(1)
    except Exception as e:
        exci = sys.exc_info()[2]
        lineno = exci.tb_lineno
        fname = exci.tb_frame.f_code.co_name
        ename = type(e).__name__
        msg = f"{ename} Exception at line {lineno} in function {fname}: {e}"
        log.error(msg)
        print("An Error occurred, see log file for details")
        sys.exit(1)


@cli.command()
def configure():
    f"""Sets up the configuration for the {appname} application."""
    try:
        cfg = {"amdirty": True}
        ckwargs = {"appname": appname}
        cfg["username"], cfg["password"] = askCredentials()
        sd = testCreds(cfg["username"], cfg["password"])
        CFG.writeConfig(cfg, **ckwargs)
    except Exception as e:
        exci = sys.exc_info()[2]
        lineno = exci.tb_lineno
        fname = exci.tb_frame.f_code.co_name
        ename = type(e).__name__
        msg = f"{ename} Exception at line {lineno} in function {fname}: {e}"
        print(msg)
        raise
