"""Personal TV Guide application."""
from pathlib import Path
import sys

import ccalogging

from sdjson.db import SDDb
from sdjson.schedule import doUpdate
from sdjson.startup import begin
from sdjson.startup import die

appname = "ccasdtv"
home = Path.home()
logfilename = home.joinpath(f".{appname}.log")
ccalogging.setLogFile(logfilename)
# ccalogging.setDebug()
ccalogging.setInfo()
log = ccalogging.log


def tvg():
    try:
        sd, CFGo = begin(appname)
        sdb = SDDb(appname=appname)
        doUpdate(CFGo.config, sd, sdb)
        CFGo.writeConfig()
    except Exception as e:
        exci = sys.exc_info()[2]
        lineno = exci.tb_lineno
        fname = exci.tb_frame.f_code.co_name
        ename = type(e).__name__
        msg = f"{ename} Exception at line {lineno} in function {fname}: {e}"
        log.error(msg)
        die(msg)


if __name__ == "__main__":
    tvg()
