"""flask display routing"""
from pathlib import Path
import sys

import ccalogging
from flask import Flask
from flask import request

from sdjson.config import Configuration
from sdjson.db import SDDb
from sdjson.html import channelPage
from sdjson.html import frontPage
from sdjson.html import gridPage
from sdjson.startup import begin
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
        CFGo = Configuration(appname)
        cfg = CFGo.config
        page = frontPage(cfg)
        return page
    except Exception as e:
        exci = sys.exc_info()[2]
        lineno = exci.tb_lineno
        fname = exci.tb_frame.f_code.co_name
        ename = type(e).__name__
        msg = f"{ename} Exception at line {lineno} in function {fname}: {e}"
        log.error(msg)
        raise


@app.route("/channel/<channelid>")
def channel(channelid):
    try:
        CFGo = Configuration(appname)
        cfg = CFGo.config
        sdb = SDDb(appname=appname)
        toffset = request.args.get("offset")
        try:
            offset = 0 if toffset is None else int(toffset)
        except ValueError:
            offset = 0
        return channelPage(sdb, cfg, channelid, offset)
    except Exception as e:
        exci = sys.exc_info()[2]
        lineno = exci.tb_lineno
        fname = exci.tb_frame.f_code.co_name
        ename = type(e).__name__
        msg = f"{ename} Exception at line {lineno} in function {fname}: {e}"
        log.error(msg)
        raise


@app.route("/grid")
def grid():
    try:
        CFGo = Configuration(appname)
        cfg = CFGo.config
        sdb = SDDb(appname=appname)
        offset = request.args.get("offset")
        gp = gridPage(sdb, cfg, offset)
        # print(gp)
        return gp
    except Exception as e:
        exci = sys.exc_info()[2]
        lineno = exci.tb_lineno
        fname = exci.tb_frame.f_code.co_name
        ename = type(e).__name__
        msg = f"{ename} Exception at line {lineno} in function {fname}: {e}"
        log.error(msg)
        raise
