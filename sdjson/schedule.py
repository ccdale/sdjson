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
        sql = "select * from schedule where airdate < ?"
        rows = sdb.selectSql(sql, [seven])
        cn = len(rows)
        msg = f"Cleaning DB, {cn} schedule rows to delete"
        log.info(msg)
        sql = "delete from schedule where airdate < ?"
        if sdb.deleteSql(sql, [seven]):
            log.info(f"{cn} rows deleted ok.")
        else:
            log.warning(f"failed to delete {cn} rows.")
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
        # chanlist = channels.keys()
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
        requiredprograms = []
        channels = {}
        for chan in cfg["channels"]:
            channels[chan["stationid"]] = chan["name"]
        schedreq = chanMd5DB(cfg, sd, sdb)
        if len(schedreq) > 0:
            scheddata = sd.getSchedules(schedreq)
            for sched in scheddata:
                chan = sched["stationID"]
                ddate = sched["metadata"]["startDate"]
                log.info(f"{channels[chan]} {ddate}")
                cn = rcn = 0
                for prog in sched["programs"]:
                    cn += 1
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
                    sql = "select * from program where programid=? and md5=?"
                    rows = sdb.selectSql(sql, [prog["programID"], prog["md5"]])
                    if len(rows) == 0:
                        rcn += 1
                        requiredprograms.append(prog["programID"])
                log.info(
                    f"{cn} programs inserted into the schedule, need to retrieve data for {rcn}"
                )
        else:
            log.info("All up to date.")
        log.info(f"{len(requiredprograms)} programs marked for retrieval.")
        sreq = set(requiredprograms)
        requiredprograms = list(sreq)
        log.info(
            f"after removing duplicates need to retrieve data for {len(requiredprograms)} programs."
        )
        return requiredprograms
    except Exception as e:
        exci = sys.exc_info()[2]
        lineno = exci.tb_lineno
        fname = exci.tb_frame.f_code.co_name
        ename = type(e).__name__
        msg = f"{ename} Exception at line {lineno} in function {fname}: {e}"
        log.error(msg)
        raise


def getPrograms(sd, sdb, proglist):
    try:
        cn = 0
        xlen = 2000
        plen = len(proglist)
        log.info(f"Need to retrieve {plen} program details.")
        done = False
        while not done:
            if (cn + xlen) > plen:
                end = cn + plen
                done = True
            else:
                end = cn + xlen
            log.debug(f"cn: {cn}, end: {end}, plen: {plen}")
            sublist = proglist[cn:end]
            cn += end
            getProgSublist(sd, sdb, sublist)
    except Exception as e:
        exci = sys.exc_info()[2]
        lineno = exci.tb_lineno
        fname = exci.tb_frame.f_code.co_name
        ename = type(e).__name__
        msg = f"{ename} Exception at line {lineno} in function {fname}: {e}"
        log.error(msg)
        raise


def getProgSublist(sd, sdb, sublist):
    try:
        log.info(f"Retrieving {len(sublist)} individual programs.")
        progs = sd.getPrograms(sublist)
        for prog in progs:
            storeProgram(sdb, prog)
    except Exception as e:
        exci = sys.exc_info()[2]
        lineno = exci.tb_lineno
        fname = exci.tb_frame.f_code.co_name
        ename = type(e).__name__
        msg = f"{ename} Exception at line {lineno} in function {fname}: {e}"
        log.error(msg)
        raise


def progKeyVal(prog):
    try:
        title = extractData(prog, "titles", "title120", True)
        event = extractData(prog, "eventDetails", "subType")
        desc = ""
        if "descriptions" in prog:
            desc = extractData(
                prog["descriptions"], "descriptions1000", "description", True
            )
        originalairdate = prog.get("originalAirDate", "")
        episodetitle = prog.get("episodeTitle150", "")
        seriesn = episoden = 0
        lmdata = prog.get("metadata", None)
        if lmdata is not None and len(lmdata) > 0:
            gn = lmdata[0].get("Gracenote", None)
            if gn is not None:
                seriesn = int(gn.get("season", 0))
                episoden = int(gn.get("episode", 0))
        pfields = {
            "md5": prog["md5"],
            "title": title,
            "episodetitle": episodetitle,
            "shortdesc": desc,
            "originalairdate": originalairdate,
            "series": seriesn,
            "episode": episoden,
        }
        return pfields
    except Exception as e:
        exci = sys.exc_info()[2]
        lineno = exci.tb_lineno
        fname = exci.tb_frame.f_code.co_name
        ename = type(e).__name__
        msg = f"{ename} Exception at line {lineno} in function {fname}: {e}"
        log.error(msg)
        raise


def updateProgram(sdb, progid, prog):
    try:
        pfields = progKeyVal(prog)
        klist = []
        vals = []
        for key in pfields:
            klist.append(f"{key}=?")
            vals.append(pfields[key])
        sql = "update program set "
        sql += ",".join(klist)
        sql += " where programid=?"
        vals.append(progid)
        sdb.insertSql(sql, vals)
    except Exception as e:
        exci = sys.exc_info()[2]
        lineno = exci.tb_lineno
        fname = exci.tb_frame.f_code.co_name
        ename = type(e).__name__
        msg = f"{ename} Exception at line {lineno} in function {fname}: {e}"
        log.error(msg)
        raise


def insertProgram(sdb, progid, prog):
    try:
        pfields = progKeyVal(prog)
        klist = ["programid"]
        vals = [progid]
        qvals = ["?"]
        for key in pfields:
            klist.append(f"{key}")
            vals.append(pfields[key])
            qvals.append("?")
        kstr = ",".join(klist)
        qvstr = ",".join(qvals)
        sql = f"insert into program ({kstr}) values ({qvstr})"
        sdb.insertSql(sql, vals)
    except Exception as e:
        exci = sys.exc_info()[2]
        lineno = exci.tb_lineno
        fname = exci.tb_frame.f_code.co_name
        ename = type(e).__name__
        msg = f"{ename} Exception at line {lineno} in function {fname}: {e}"
        log.error(msg)
        raise


def storeProgram(sdb, prog):
    """Store the program in the program table.

    drop table if exists program;
    create table program (
        programid text,
        md5 text,
        title text,
        episodetitle text,
        shortdesc text,
        longdesc text,
        originalairdate text,
        series int,
        episode int,
        primary key(programid, md5)
    );
    """
    try:
        sql = "select * from program where programid=?"
        row = sdb.selectSql(sql, [prog["programID"]])
        if len(row) > 0:
            updateProgram(sdb, prog["programID"], prog)
        else:
            insertProgram(sdb, prog["programID"], prog)
    except Exception as e:
        exci = sys.exc_info()[2]
        lineno = exci.tb_lineno
        fname = exci.tb_frame.f_code.co_name
        ename = type(e).__name__
        msg = f"{ename} Exception at line {lineno} in function {fname}: {e}"
        log.error(msg)
        raise


def extractData(data, key, subkey, subkeyinlist=False):
    try:
        ret = ""
        default = [] if subkeyinlist else {}
        xl = data.get(key, default)
        if subkeyinlist:
            for x in xl:
                ret += x.get(subkey, "")
        else:
            ret += xl.get(subkey, "")
        return ret
    except Exception as e:
        exci = sys.exc_info()[2]
        lineno = exci.tb_lineno
        fname = exci.tb_frame.f_code.co_name
        ename = type(e).__name__
        msg = f"{ename} Exception at line {lineno} in function {fname}: {e}"
        log.error(msg)
        raise


def getProgramTitle(prog):
    try:
        xl = prog.get("titles", [])
        for x in xl:
            title = x.get("title120", "")
        return title
    except Exception as e:
        exci = sys.exc_info()[2]
        lineno = exci.tb_lineno
        fname = exci.tb_frame.f_code.co_name
        ename = type(e).__name__
        msg = f"{ename} Exception at line {lineno} in function {fname}: {e}"
        log.error(msg)
        raise
