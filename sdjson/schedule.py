# Copyright (c) 2021, Christopher Allison
#
#     This file is part of ccasdtv.
#
#     ccasdtv is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     ccasdtv is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with ccasdtv.  If not, see <http://www.gnu.org/licenses/>.

"""ccasdtv personal tv guide schedules module."""

import sys
import time

import ccalogging

log = ccalogging.log


def testDictKeys(idict, keyslist, optkeyslist=None):
    try:
        kerror = True
        for ikey in keyslist:
            if ikey not in idict:
                kerror = False
                log.error(f"required key {ikey} not in dict {idict}")
                break
        if kerror and optkeyslist is not None:
            for ikey in optkeyslist:
                if ikey not in idict:
                    kerror = False
                    log.error(f"optional key {ikey} not in dict {idict}")
                    break
        return kerror
    except Exception as e:
        exci = sys.exc_info()[2]
        lineno = exci.tb_lineno
        fname = exci.tb_frame.f_code.co_name
        ename = type(e).__name__
        msg = f"{ename} Exception at line {lineno} in function {fname}: {e}"
        log.error(msg)
        raise


def cleanChanMd5DB(sdb):
    try:
        seven = int(time.time()) - ((3600 * 24) * 7)
        sql = "select * from schedulemd5 where datets < ?"
        rows = sdb.selectSql(sql, [seven])
        cn = len(rows)
        msg = f"Cleaning DB, {cn} md5 rows to delete"
        log.info(msg)
        sql = "delete from schedulemd5 where datets < ?"
        if sdb.deleteSql(sql, [seven]):
            log.info("{cn} rows deleted ok.")
        else:
            log.warning("failed to delete {cn} rows.")
    except Exception as e:
        exci = sys.exc_info()[2]
        lineno = exci.tb_lineno
        fname = exci.tb_frame.f_code.co_name
        ename = type(e).__name__
        msg = f"{ename} Exception at line {lineno} in function {fname}: {e}"
        log.error(msg)
        raise


def insertChanMd5DB(sdb, chanid, date, cdata):
    try:
        reqkeys = ["code", "lastModified", "md5", "message"]
        if testDictKeys(cdata, reqkeys):
            if int(cdata["code"]) == 0:
                sql = "insert into schedulemd5 "
                sql += "(md5, stationid, datestr, datets, modified) "
                sql += "values (?, ?, ?, ?, ?)"
                lmts = sdb.getTimeStamp(cdata["lastModified"])
                dts = sdb.getTimeStamp(date, dtformat="%Y-%m-%d")
                return sdb.insertSql(sql, [cdata["md5"], chanid, date, dts, lmts])
        return False
    except Exception as e:
        exci = sys.exc_info()[2]
        lineno = exci.tb_lineno
        fname = exci.tb_frame.f_code.co_name
        ename = type(e).__name__
        msg = f"{ename} Exception at line {lineno} in function {fname}: {e}"
        log.error(msg)
        raise


def chanMd5DB(cfg, sd, sdb):
    """get the schedule md5 for each channel.

    Attempt to insert into the DB, if it fails we already have this schedule
    if it inserts ok, we don't have this schedule data - so record that in
    the form that schedulesdirect want:

            list of dictionaries
            [
                {
                    "stationID": "20454",
                    "date": ["2020-01-21", "2020-01-22"]
                }
            ]
    """
    try:
        cleanChanMd5DB(sdb)
        req = []
        chanlist = [chan["stationid"] for chan in cfg["channels"]]
        schedmd5 = sd.getScheduleMd5(chanlist)
        for chan in schedmd5:
            clist = []
            for date in schedmd5[chan]:
                ddata = schedmd5[chan][date]
                if insertChanMd5DB(sdb, chan, date, ddata):
                    clist.append(date)
            if len(clist) > 0:
                req.append({"stationID": chan, "date": clist})
        return req
    except Exception as e:
        exci = sys.exc_info()[2]
        lineno = exci.tb_lineno
        fname = exci.tb_frame.f_code.co_name
        ename = type(e).__name__
        msg = f"{ename} Exception at line {lineno} in function {fname}: {e}"
        log.error(msg)
        raise


def updateSchedule(cfg, sd, sdb):
    """Retrieve schedule data we don't currently have and insert into db.
    https://json.schedulesdirect.org/20141201/schedules
    """
    try:
        schedreq = chanMd5DB(cfg, sd, sdb)
        if len(schedreq) > 0:
            scheddata = sd.getSchedules(schedreq)
            for sched in scheddata:
                chan = sched["stationID"]
                for prog in sched["programs"]:
                    sql = "insert into schedule (programid, md5, stationid, airdate, duration) values (?, ?, ?, ?, ?)"
                    sdb.insertSql(
                        sql,
                        [
                            prog["programID"],
                            prog["md5"],
                            chan,
                            sdb.getTimeStamp(prog["airDateTime"]),
                            int(prog["duration"]),
                        ],
                    )
        else:
            log.info("All up to date.")
    except Exception as e:
        exci = sys.exc_info()[2]
        lineno = exci.tb_lineno
        fname = exci.tb_frame.f_code.co_name
        ename = type(e).__name__
        msg = f"{ename} Exception at line {lineno} in function {fname}: {e}"
        log.error(msg)
        raise
