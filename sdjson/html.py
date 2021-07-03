import datetime
import sys
import time

import ccalogging

from sdjson.programs import dayProgs
from sdjson.programs import gridProgs
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


def makeTag(tag, data, attrs=None, close=True, datanl=False, endnl=False, indent=""):
    try:
        op = f"<{tag}"
        cl = f"</{tag}>" if close else ""
        dnl = "\n" if datanl else ""
        ednl = "\n" if datanl and data[-1] != "\n" else ""
        enl = "\n" if endnl else ""
        if attrs is not None:
            if type(attrs) is dict:
                for key in attrs:
                    op += f' {key}="{attrs[key]}"'
            elif type(attrs) is list:
                for attr in attrs:
                    op += f" {attr}"
            else:
                op += f" {attrs}"
        return f"{indent}{op}>{dnl}{data}{ednl}{cl}{enl}"
    except Exception as e:
        exci = sys.exc_info()[2]
        lineno = exci.tb_lineno
        fname = exci.tb_frame.f_code.co_name
        ename = type(e).__name__
        msg = f"{ename} Exception at line {lineno} in function {fname}: {e}"
        log.error(msg)
        raise


def makeLink(route, linktxt, endnl=False, datanl=False, indent=""):
    try:
        attrs = [f"href={route}"]
        return makeTag("a", linktxt, attrs, endnl=endnl, datanl=datanl, indent=indent)
    except Exception as e:
        exci = sys.exc_info()[2]
        lineno = exci.tb_lineno
        fname = exci.tb_frame.f_code.co_name
        ename = type(e).__name__
        msg = f"{ename} Exception at line {lineno} in function {fname}: {e}"
        log.error(msg)
        raise


def makeDiv(data, endnl=False, datanl=False, indent=""):
    try:
        return makeTag("div", data, endnl=endnl, datanl=datanl, indent=indent)
    except Exception as e:
        exci = sys.exc_info()[2]
        lineno = exci.tb_lineno
        fname = exci.tb_frame.f_code.co_name
        ename = type(e).__name__
        msg = f"{ename} Exception at line {lineno} in function {fname}: {e}"
        log.error(msg)
        raise


def makeP(data, indent="", endnl=False, datanl=False):
    try:
        return makeTag("p", data, indent=indent, endnl=endnl, datanl=datanl)
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
        indent = "  "
        css = makeTag("style", style, endnl=True, indent=indent + indent)
        hd = (
            makeTag("head", head, datanl=True, endnl=True, indent=indent)
            if head is not None
            else makeTag("head", css, datanl=True, endnl=True, indent=indent)
        )
        bd = makeTag("body", body, endnl=True, datanl=True, indent=indent)
        page = makeTag("html", hd + bd, datanl=True)
        return "<!DOCTYPE html>\n" + page
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


def progLine(prog, indent=""):
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
        row = makeTag("tr", stt + mdur + tit, datanl=True, endnl=True, indent=indent)
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
        indent = "  "
        name = channelName(cfg, channelid)
        nlink = makeLink("/", name)
        heading = makeDiv(makeTag("h3", nlink, endnl=True, indent=indent))
        progs = dayProgs(sdb, channelid, offset)
        trows = []
        ccalogging.setDebug()
        for prog in progs:
            trows.append(progLine(prog))
        ccalogging.setInfo()
        rows = "".join(trows)
        table = makeTag("table", rows, indent=indent + indent)
        dtable = makeDiv(table, indent=indent)
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


def timeLine(start, numcolumns=1, width=4):
    """returns a table row of the date and half hour increments.

    start: the timestamp of the start time
    numcolumns: the number of table cols per half hour
    width: the number of half hours to show
    """
    try:
        dt = datetime.datetime.fromtimestamp(start)
        sdate = f"{dt.strftime('%a')} {dt.day:02}/{dt.month:02}"
        dt.weekday
        attrs = {"colspan": numcolumns, "class": "timerowdata"}
        row = makeTag("td", sdate, attrs=attrs, endnl=True)
        for i in range(width):
            dt = datetime.datetime.fromtimestamp(start)
            stime = f"{dt.hour:02}:{dt.minute:02}"
            row += makeTag("td", stime, attrs=attrs, endnl=True)
            start = start + 1800
        attrs = {"class": "timerow"}
        trow = makeTag("tr", row, attrs=attrs, endnl=True, datanl=True)
        return trow
    except Exception as e:
        exci = sys.exc_info()[2]
        lineno = exci.tb_lineno
        fname = exci.tb_frame.f_code.co_name
        ename = type(e).__name__
        msg = f"{ename} Exception at line {lineno} in function {fname}: {e}"
        log.error(msg)
        raise


def gridPage(sdb, cfg, offset=0):
    try:
        pdict, shortest, start = gridProgs(sdb, cfg["channels"], startoffset=offset)
        tl = timeLine(start, numcolumns=1, width=4)
        trows = [tl]
        for channame in pdict:
            row = makeTag("td", channame, endnl=True)
            for prog in pdict[channame]:
                row += makeTag("td", prog["title"], endnl=True)
            trows.append(makeTag("tr", row, endnl=True, datanl=True))
        rows = "".join(trows)
        tab = makeTag("table", rows, datanl=True, endnl=True)
        dtable = makeDiv(tab, datanl=True, endnl=True)
        return makePage(dtable)
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
