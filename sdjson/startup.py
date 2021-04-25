import hashlib
import sys

import ccalogging

from sdjson.config import Configuration
from sdjson.credential import Credential
from sdjson.sdapi import SDApi
from sdjson.windows import credsWindow
from sdjson.windows import errorWindow

log = ccalogging.log


def die(msg=""):
    try:
        if len(msg) == 0:
            msg = "an unexpected error has occurred."
        errorWindow(msg)
        log.error(msg)
        sys.exit(1)
    except Exception as e:
        exci = sys.exc_info()[2]
        lineno = exci.tb_lineno
        fname = exci.tb_frame.f_code.co_name
        ename = type(e).__name__
        msg = f"{ename} Exception at line {lineno} in function {fname}: {e}"
        print(msg)
        sys.exit(1)


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


def begin(appname="ccasdtv"):
    try:
        CFGo = Configuration(appname)
        cfg = CFGo.config
        cfgun = cfg.get("username", "")
        un, hpw = getCreds(cfgun)
        if un is not None and un != cfgun:
            CFGo.update("username", un)
        if hpw is None:
            die("Unconfigured")
        ckwargs = {"username": un, "password": hpw}
        if "token" in cfg and "tokenexpires" in cfg:
            ckwargs["token"] = cfg["token"]
            ckwargs["tokenexpires"] = cfg["tokenexpires"]
        sd = SDApi(**ckwargs)
        sd.apiOnline()
        if not sd.online:
            del cfg["token"]
            del cfg["tokenexpires"]
            die(sd.statusmsg)
        return (sd, CFGo)
    except Exception as e:
        exci = sys.exc_info()[2]
        lineno = exci.tb_lineno
        fname = exci.tb_frame.f_code.co_name
        ename = type(e).__name__
        msg = f"{ename} Exception at line {lineno} in function {fname}: {e}"
        log.error(msg)
        raise