#!/usr/bin/env python3
"""CLI for ccasdtv."""

import hashlib
from pathlib import Path
import sys

import ccalogging
import click

from sdjson.cache import makeCacheDir
import sdjson.config as CFG
from sdjson.sdapi import SDApi
from sdjson import __version__

appname = "ccasdtv"
home = Path.home()

logfilename = home.joinpath(f"{appname}.log")
ccalogging.setLogFile(logfilename)
ccalogging.setDebug()
log = ccalogging.log

log.info(f"{appname} {__version__} CLI Starting")


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
        log.info("Supplied credentials appear to be correct")
    except Exception as e:
        exci = sys.exc_info()[2]
        lineno = exci.tb_lineno
        fname = exci.tb_frame.f_code.co_name
        ename = type(e).__name__
        msg = f"{ename} Exception at line {lineno} in function {fname}: {e}"
        # print(msg)
        log.error(msg)
        raise


@click.command()
def doConfigure():
    try:
        kwargs = {"appname": appname}
        cfg = CFG.readConfig(**kwargs)
        cfg["amdirty"] = False
        print(cfg)
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


if __name__ == "__main__":
    doConfigure()
