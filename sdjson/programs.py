import datetime
import sys
import time

import ccalogging

log = ccalogging.log


def channelPrograms(sdb, channelid, dayoffset=0):
    try:
        progs = []
        days = dayoffset * 86400
        today = datetime.date.today()
        midnight = int(time.mktime(today.timetuple())) + days
        tomorrow = midnight + 86400
        sql = "select * from schedule where stationid=? and airdate>=? and airdate<=? order by airdate asc"
        rows = sdb.selectSql(sql, [channelid, midnight, tomorrow])
        # make a list of program ids and remove duplicates
        pids = set([row[0] for row in rows])
        iprogs = getProgramsFromList(sdb, pids)
        for row in rows:
            prog = {}
            prog["programid"] = row[0]
            prog["airdate"] = row[3]
            prog["duration"] = row[4]
            # xprow = sdb.selectSql(sql, [prog["programid"]])
            # prow = xprow[0]
            prog["title"] = iprogs[prog["programid"]][2]
            prog["episodetitle"] = iprogs[prog["programid"]][3]
            prog["shortdesc"] = iprogs[prog["programid"]][4]
            prog["longdesc"] = iprogs[prog["programid"]][5]
            progs.append(prog)
        return progs
    except Exception as e:
        exci = sys.exc_info()[2]
        lineno = exci.tb_lineno
        fname = exci.tb_frame.f_code.co_name
        ename = type(e).__name__
        msg = f"{ename} Exception at line {lineno} in function {fname}: {e}"
        log.error(msg)
        raise


def getProgramsFromList(sdb, pids):
    try:
        oprogs = {}
        qpids = ",".join([f'"{x}"' for x in pids])
        sql = f"select * from program where programid in ({qpids})"
        progrows = sdb.selectSql(sql)
        for row in progrows:
            oprogs[row[0]] = row
        return oprogs
    except Exception as e:
        exci = sys.exc_info()[2]
        lineno = exci.tb_lineno
        fname = exci.tb_frame.f_code.co_name
        ename = type(e).__name__
        msg = f"{ename} Exception at line {lineno} in function {fname}: {e}"
        log.error(msg)
        raise