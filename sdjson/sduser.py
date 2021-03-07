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

"""User configuration for the ccasdtv application."""
import hashlib
import sys

import ccalogging

from sdjson.sdapi import SDApi

log = ccalogging.log


def askMe(q, default, required=False):
    """Input routine for the console.

    Args:
        q: str input question
        default: str default answer

    Raises:
        TypeError: if input `q` is not a string

    Returns:
        str: user input or default
    """
    try:
        if type(q) is not str:
            raise TypeError("Input error, question is not a string.")
        ret = default
        val = input(f"{q} ({default}) > ")
        if len(val) > 0:
            ret = val
        if len(ret) == 0 and required:
            raise Exception(f"Input value: {q} is required")
        return ret
    except Exception as e:
        exci = sys.exc_info()[2]
        lineno = exci.tb_lineno
        fname = exci.tb_frame.f_code.co_name
        ename = type(e).__name__
        msg = f"{ename} Exception at line {lineno} in function {fname}: {e}"
        log.error(msg)
        raise


def askCredentials():
    try:
        uname = askMe("Schedules Direct username: ", "", required=True)
        password = askMe("SD Password: ", "", required=True)
        pword = hashlib.sha1(password.encode()).hexdigest()
        return (uname, pword)
    except Exception as e:
        exci = sys.exc_info()[2]
        lineno = exci.tb_lineno
        fname = exci.tb_frame.f_code.co_name
        ename = type(e).__name__
        msg = f"{ename} Exception at line {lineno} in function {fname}: {e}"
        log.error(msg)
        raise


def testCreds(uname, pword):
    try:
        sd = SDApi(uname, pword)
        sd.apiOnline()
        if not sd.online:
            print(sd.statusmsg)
            raise Exception("Schedules Direct is not online")
        log.debug("Supplied credentials appear to be correct")
        return sd
    except Exception as e:
        exci = sys.exc_info()[2]
        lineno = exci.tb_lineno
        fname = exci.tb_frame.f_code.co_name
        ename = type(e).__name__
        msg = f"{ename} Exception at line {lineno} in function {fname}: {e}"
        log.error(msg)
        raise


def confUser(cfg):
    try:
        if "username" in cfg:
            resp = askMe(f"""keep user creds: {cfg["username"]}""", "Y")
            if resp == "Y":
                return cfg
        cfg["username"], cfg["password"] = askCredentials()
        return cfg
    except Exception as e:
        exci = sys.exc_info()[2]
        lineno = exci.tb_lineno
        fname = exci.tb_frame.f_code.co_name
        ename = type(e).__name__
        msg = f"{ename} Exception at line {lineno} in function {fname}: {e}"
        log.error(msg)
        raise
