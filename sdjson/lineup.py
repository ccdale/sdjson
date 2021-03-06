#
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
"""Schedules Direct Lineup functions for ccasdtv."""

import sys

import ccalogging


log = ccalogging.log


def parseStations(sdata, channums):
    try:
        channelsbyname = {}
        channelsbyid = {}
        for station in sdata:
            station["channelnumber"] = channums[station["stationID"]]
            channelsbyname[station["name"]] = station
            channelsbyid[station["stationID"]] = station
        return {"channelsbyname": channelsbyname, "channelsbyid": channelsbyid}
    except Exception as e:
        exci = sys.exc_info()[2]
        lineno = exci.tb_lineno
        fname = exci.tb_frame.f_code.co_name
        ename = type(e).__name__
        msg = f"{ename} Exception at line {lineno} in function {fname}: {e}"
        log.error(msg)
        raise


def parseChannelMap(mapdata):
    try:
        stations = {}
        for chan in mapdata:
            stations[chan["stationID"]] = chan["channel"]
        return stations
    except Exception as e:
        exci = sys.exc_info()[2]
        lineno = exci.tb_lineno
        fname = exci.tb_frame.f_code.co_name
        ename = type(e).__name__
        msg = f"{ename} Exception at line {lineno} in function {fname}: {e}"
        log.error(msg)
        raise


def parseLineupData(jdata):
    try:
        channums = channeldict = None
        if "map" in jdata:
            channums = parseChannelMap(jdata["map"])
        if channums is not None and "stations" in jdata:
            channeldict = parseStations(jdata["stations"], channums)
        return channeldict
    except Exception as e:
        exci = sys.exc_info()[2]
        lineno = exci.tb_lineno
        fname = exci.tb_frame.f_code.co_name
        ename = type(e).__name__
        msg = f"{ename} Exception at line {lineno} in function {fname}: {e}"
        log.error(msg)
        raise
