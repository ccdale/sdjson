"""flask display routing"""
from pathlib import Path
import sys

import ccalogging
from flask import Flask

from sdjson import __version__

appname = "ccasdtv"

home = Path.home()
logfilename = home.joinpath(f".{appname}.log")
ccalogging.setLogFile(logfilename)
# ccalogging.setDebug()
ccalogging.setInfo()
log = ccalogging.log

app = Flask(__name__)


@app.route("/")
def hello():
    try:
        return f"I am {appname} {__version__}"
    except Exception as e:
        exci = sys.exc_info()[2]
        lineno = exci.tb_lineno
        fname = exci.tb_frame.f_code.co_name
        ename = type(e).__name__
        msg = f"{ename} Exception at line {lineno} in function {fname}: {e}"
        log.error(msg)
        raise
