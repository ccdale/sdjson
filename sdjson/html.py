import datetime
import sys
import time

import ccalogging

from sdjson.programs import dayProgs
from sdjson.timedisplay import hms

log = ccalogging.log

style = """
table {
  border-collapse: collapse;
  width: 100%;
}

th, td {
  text-align: left;
  padding: 8px;
}

tr:nth-child(even) {background-color: #f2f2f2;}
"""


def makeTag(tag, data, attrs=None, close=True):
    try:
        op = f"<{tag}"
        cl = f"</{tag}>" if close else ""
        if attrs is not None:
            for attr in attrs:
                op += f" {attr}"
        return f"{op}>{data}{cl}"
    except Exception as e:
        exci = sys.exc_info()[2]
        lineno = exci.tb_lineno
        fname = exci.tb_frame.f_code.co_name
        ename = type(e).__name__
        msg = f"{ename} Exception at line {lineno} in function {fname}: {e}"
        log.error(msg)
        raise


def makeLink(route, linktxt):
    try:
        attrs = [f"href={route}"]
        return makeTag("a", linktxt, attrs)
    except Exception as e:
        exci = sys.exc_info()[2]
        lineno = exci.tb_lineno
        fname = exci.tb_frame.f_code.co_name
        ename = type(e).__name__
        msg = f"{ename} Exception at line {lineno} in function {fname}: {e}"
        log.error(msg)
        raise


def makeDiv(data):
    try:
        return makeTag("div", data)
    except Exception as e:
        exci = sys.exc_info()[2]
        lineno = exci.tb_lineno
        fname = exci.tb_frame.f_code.co_name
        ename = type(e).__name__
        msg = f"{ename} Exception at line {lineno} in function {fname}: {e}"
        log.error(msg)
        raise


def makeP(data):
    try:
        return makeTag("p", data)
    except Exception as e:
        exci = sys.exc_info()[2]
        lineno = exci.tb_lineno
        fname = exci.tb_frame.f_code.co_name
        ename = type(e).__name__
        msg = f"{ename} Exception at line {lineno} in function {fname}: {e}"
        log.error(msg)
        raise


def makePage(body, head=None):
    try:
        global style
        css = makeTag("style", style)
        hd = makeTag("head", head) if head is not None else makeTag("head", css)
        bd = makeTag("body", body)
        return makeTag("html", hd + bd)
    except Exception as e:
        exci = sys.exc_info()[2]
        lineno = exci.tb_lineno
        fname = exci.tb_frame.f_code.co_name
        ename = type(e).__name__
        msg = f"{ename} Exception at line {lineno} in function {fname}: {e}"
        log.error(msg)
        raise


def dayLine(channelid, offset=0):
    try:
        op = ""
        today = datetime.date.today()
        for i in range(1, 7):
            pass
        dayname = today.strftime("%a")
    except Exception as e:
        exci = sys.exc_info()[2]
        lineno = exci.tb_lineno
        fname = exci.tb_frame.f_code.co_name
        ename = type(e).__name__
        msg = f"{ename} Exception at line {lineno} in function {fname}: {e}"
        log.error(msg)
        raise


def channelName(cfg, stationid):
    try:
        for chan in cfg["channels"]:
            if chan["stationid"] == stationid:
                return chan["name"]
        return ""
    except Exception as e:
        exci = sys.exc_info()[2]
        lineno = exci.tb_lineno
        fname = exci.tb_frame.f_code.co_name
        ename = type(e).__name__
        msg = f"{ename} Exception at line {lineno} in function {fname}: {e}"
        log.error(msg)
        raise


def progLine(prog):
    try:
        tt = datetime.datetime.fromtimestamp(prog["airdate"])
        hr = tt.hour
        xmin = tt.minute
        stt = makeTag("td", f"{hr:02}:{xmin:02}")
        mdur = makeTag(
            "td",
            f'{hms(int(prog["duration"]), small=False, colons=True, noseconds=True)}',
        )
        tit = makeTag("td", prog["title"])
        row = makeTag("tr", stt + mdur + tit)
        return row
    except Exception as e:
        exci = sys.exc_info()[2]
        lineno = exci.tb_lineno
        fname = exci.tb_frame.f_code.co_name
        ename = type(e).__name__
        msg = f"{ename} Exception at line {lineno} in function {fname}: {e}"
        log.error(msg)
        raise


def channelPage(sdb, cfg, channelid, offset=0):
    try:
        # sql = "select name from channel where stationid=?"
        # rows = sdb.selectSql(sql, [channelid])
        # name = rows[0][0]
        name = channelName(cfg, channelid)
        heading = makeDiv(makeTag("h3", name))
        progs = dayProgs(sdb, channelid, offset)
        trows = []
        ccalogging.setDebug()
        for prog in progs:
            trows.append(progLine(prog))
        ccalogging.setInfo()
        rows = "\n".join(trows)
        table = makeTag("table", rows)
        dtable = makeDiv(table)
        body = heading + dtable
        return makePage(body)
    except Exception as e:
        exci = sys.exc_info()[2]
        lineno = exci.tb_lineno
        fname = exci.tb_frame.f_code.co_name
        ename = type(e).__name__
        msg = f"{ename} Exception at line {lineno} in function {fname}: {e}"
        log.error(msg)
        raise


def frontPage(cfg):
    try:
        heading = makeDiv(makeTag("h3", "Personal TV Guide"))
        op = ""
        for chan in cfg["channels"]:
            route = f"""/channel/{chan["stationid"]}"""
            lnktxt = chan["name"]
            op += makeP(makeLink(route, lnktxt))
        body = heading + makeDiv(op)
        return makePage(body)
    except Exception as e:
        exci = sys.exc_info()[2]
        lineno = exci.tb_lineno
        fname = exci.tb_frame.f_code.co_name
        ename = type(e).__name__
        msg = f"{ename} Exception at line {lineno} in function {fname}: {e}"
        log.error(msg)
        raise
