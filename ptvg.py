"""Personal TV Guide application."""
import hashlib
from pathlib import Path
import sys

import ccalogging
import PySimpleGUI as sg

import sdjson.config as CFG
from sdjson.config import Configuration
from sdjson.credential import Credential
from sdjson.sdapi import SDApi
from sdjson.windows import credsWindow

appname = "ccasdtv"
home = Path.home()
logfilename = home.joinpath(f".{appname}.log")
ccalogging.setLogFile(logfilename)
# ccalogging.setDebug()
ccalogging.setInfo()
log = ccalogging.log


def getCreds(username):
    try:
        CREDS = Credential(username, "schedulesdirect.org")
        hpw = CREDS.getPassword()
        un = username
        if hpw is None:
            un, pw = credsWindow(username)
            if pw is not None:
                hpw = hashlib.sha1(pw.encode()).hexdigest()
                CREDS.setPassword(hpw)
        return un, hpw
    except Exception as e:
        exci = sys.exc_info()[2]
        lineno = exci.tb_lineno
        fname = exci.tb_frame.f_code.co_name
        ename = type(e).__name__
        msg = f"{ename} Exception at line {lineno} in function {fname}: {e}"
        log.error(msg)
        raise


def tvg():
    try:
        CFGo = Configuration(appname)
        cfg = CFGo.config
        cfgun = cfg.get("username", "")
        un, hpw = getCreds(cfgun)
        if un is not None and un != cfgun:
            CFGo.update("username", un)
    except Exception as e:
        exci = sys.exc_info()[2]
        lineno = exci.tb_lineno
        fname = exci.tb_frame.f_code.co_name
        ename = type(e).__name__
        msg = f"{ename} Exception at line {lineno} in function {fname}: {e}"
        log.error(msg)
        sys.exit(1)


if __name__ == "__main__":
    tvg()
