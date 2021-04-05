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
                if sdb.insertSql(sql, [cdata["md5"], chanid, date, dts, lmts]):
                    log.debug("new data inserted for channel md5")
                else:
                    log.debug("data already exists")
    except Exception as e:
        exci = sys.exc_info()[2]
        lineno = exci.tb_lineno
        fname = exci.tb_frame.f_code.co_name
        ename = type(e).__name__
        msg = f"{ename} Exception at line {lineno} in function {fname}: {e}"
        log.error(msg)
        raise


def chanMd5DB(cfg, sd, sdb):
    try:
        chanlist = [chan["stationid"] for chan in cfg["channels"]]
        schedmd5 = sd.getScheduleMd5(chanlist)
        for chan in schedmd5:
            for date in schedmd5[chan]:
                ddata = schedmd5[chan][date]
                insertChanMd5DB(sdb, chan, date, ddata)
    except Exception as e:
        exci = sys.exc_info()[2]
        lineno = exci.tb_lineno
        fname = exci.tb_frame.f_code.co_name
        ename = type(e).__name__
        msg = f"{ename} Exception at line {lineno} in function {fname}: {e}"
        log.error(msg)
        raise
