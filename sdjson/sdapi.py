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
"""ScheduleDirect API class for the ccasdtv application."""

import datetime
import json
import sys

import requests

from sdjson import __version__


# when the 20191022 api is out of beta the default url should be:
# https://json.schedulesdirect.org/20191022
class SDApi:
    """Schedules Direct API class."""

    def __init__(
        self,
        username,
        sha1password,
        appname="ccasdtv",
        url="https://w8xmzqba6c.execute-api.us-east-1.amazonaws.com/20191022",
        debug=False,
    ):
        """Initialise the SDApi Class.

        Args:
            username: str: Schedule Direct username
            sha1password: str: sha1 encoded password for SD
            appname: str: Name that is used as the User-Agent header
            url: str: SD API URL - default is the beta 20191022 url
            debug: bool: print api calls and responses
        """
        try:
            self.username = username
            self.password = sha1password
            self.url = url
            self.debug = debug
            self.headers = {"User-Agent": f"{appname} / {__version__}"}
            self.token = None
            self.status = True
            self.statusmsg = "initialising"
        except Exception as e:
            exci = sys.exc_info()[2]
            lineno = exci.tb_lineno
            fname = exci.tb_frame.f_code.co_name
            ename = type(e).__name__
            msg = f"{ename} Exception at line {lineno} in function {fname}: {e}"
            print(msg)
            raise

    def showResponse(self, jresp):
        try:
            if self.debug:
                print(
                    json.dumps(jresp, indent=4, sort_keys=True), end="\n\n", flush=True
                )
        except Exception as e:
            exci = sys.exc_info()[2]
            lineno = exci.tb_lineno
            fname = exci.tb_frame.f_code.co_name
            ename = type(e).__name__
            msg = f"{ename} Exception at line {lineno} in function {fname}: {e}"
            print(msg)
            raise

    # Decorator function to call the API
    def apiNoToken(self, func):
        """Call the API, handle any errors, return the JSON payload."""

        def callFunc(*args, **kwargs):
            res = None
            try:
                res = func(*args, **kwargs)
            except Exception as e:
                print(f"{type(e).__name__} Exception in {func.__name__}:\n{e}")
                raise
            jresp = None
            try:
                res.raise_for_status()
                jresp = res.json()
            except Exception as e:
                print(
                    f"Reading json response: {type(e).__name__} Exception in {func.__name__}:\n{e}"
                )
                raise
            self.showResponse(jresp)
            return jresp

        return callFunc

    # Decorator function to call the SD API with token
    def apiTokenRequired(self, func):
        """Set the "token" header, call the api then remove the header."""

        def callFunc(*args, **kwargs):
            if not self.token:
                self.apiToken()
            self.headers["token"] = self.token

            @self.apiNoToken
            def callAPI():
                return func(*args, **kwargs)

            jresp = callAPI()
            del self.headers["token"]

        return callFunc

    def apiPost(self, route, postdict):
        try:
            url = f"{self.url}/{route}"
            return requests.post(url, headers=self.headers, data=json.dumps(postdict))
        except Exception as e:
            exci = sys.exc_info()[2]
            lineno = exci.tb_lineno
            fname = exci.tb_frame.f_code.co_name
            ename = type(e).__name__
            msg = f"{ename} Exception at line {lineno} in function {fname}: {e}"
            print(msg)
            raise

    def apiGet(self, route, querydict={}):
        try:
            url = f"{self.url}/{route}"
            return requests.get(url, headers=self.headers, params=querydict)
        except Exception as e:
            exci = sys.exc_info()[2]
            lineno = exci.tb_lineno
            fname = exci.tb_frame.f_code.co_name
            ename = type(e).__name__
            msg = f"{ename} Exception at line {lineno} in function {fname}: {e}"
            print(msg)
            raise

    def apiToken(self):
        try:
            if self.debug:
                print("Asking for a token")
            reqdata = {"username": self.username, "password": self.password}
            res = self.apiPost("token", reqdata)
            res.raise_for_status()
            jres = res.json()
            code = int(jres["code"])
            if code == 0:
                self.token = jres["token"]
                if self.debug:
                    print("Token obtained")
            else:
                msg = f"code: {code}: "
                msg += f"""jres["response"]"""
                raise Exception(msg)
        except Exception as e:
            exci = sys.exc_info()[2]
            lineno = exci.tb_lineno
            fname = exci.tb_frame.f_code.co_name
            ename = type(e).__name__
            msg = f"{ename} Exception at line {lineno} in function {fname}: {e}"
            print(msg)
            raise

    def apiStatus(self):
        """Set the status of the SD API"""
        try:

            @self.apiTokenRequired
            def sdapiStatus():
                return self.apiGet("status")

            xstatus = sdapiStatus()
            self.parseLatestStatus(xstatus)
        except Exception as e:
            exci = sys.exc_info()[2]
            lineno = exci.tb_lineno
            fname = exci.tb_frame.f_code.co_name
            ename = type(e).__name__
            msg = f"{ename} Exception at line {lineno} in function {fname}: {e}"
            print(msg)
            raise

    def parseLatestStatus(self, xstatus):
        try:
            if "systemStatus" in xstatus:
                latest = 0
                for xst in xstatus["systemStatus"]:
                    pdt = datetime.strptime(
                        xst["date"], "%Y-%m-%dT%H:%M:%SZ"
                    ).timestamp()
                    if pdt > latest:
                        latest = pdt
                        if xst["status"] == "Online":
                            self.status = True
                        else:
                            self.status = False
                        self.statusmsg = xst["message"]
        except Exception as e:
            exci = sys.exc_info()[2]
            lineno = exci.tb_lineno
            fname = exci.tb_frame.f_code.co_name
            ename = type(e).__name__
            msg = f"{ename} Exception at line {lineno} in function {fname}: {e}"
            print(msg)
            raise
