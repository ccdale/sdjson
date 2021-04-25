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

appname = "ccasdtv"
home = Path.home()
logfilename = home.joinpath(f".{appname}.log")
ccalogging.setLogFile(logfilename)
# ccalogging.setDebug()
ccalogging.setInfo()
log = ccalogging.log


def credsWindow(username):
    try:
        log.debug("opening credentials window.")
        layout = [
            [sg.T("Password will stored in the system keyring.")],
            [sg.T("SD Username"), sg.I(username, key="UIN")],
            [sg.T("SD Password"), sg.I(key="PIN")],
            [sg.Submit(key="submit"), sg.Cancel(key="cancel")],
        ]
        window = sg.Window("Schedules Direct Credentials.", layout)
        event, values = window.read()
        window.close()
        log.debug("credentials window closed.")
        # un = pw = chkbx = None
        un = pw = None
        if event == "submit":
            un = values["UIN"]
            pw = values["PIN"]
        if "PIN" in values:
            values["PIN"] = "xxxxxxxxxx"
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
        un, hpw = getCreds(cfg.get("username", ""))
        log.info(f"un: {un}, pw: {hpw}")
        if un is not None and un != cfg.get("username", ""):
            cfg["username"] = un
            cfg["amdirty"] = True
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
