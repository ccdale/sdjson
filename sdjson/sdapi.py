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
"""ScheduleDirect API class for the ccasdtv application.

Mainly coding ideas from https://github.com/essandess/sd-py
re-written in my coding style, with added token caching/renewing
Thankyou Steven T. Smith.
"""

import datetime
import json
import sys
import time

import ccalogging
import requests

from sdjson import __version__

log = ccalogging.log

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
        token=None,
        tokenexpires=0,
    ):
        """Initialise the SDApi Class.

        Args:
            username: str: Schedule Direct username
            sha1password: str: sha1 encoded password for SD
            appname: str: Name that is used as the User-Agent header
            url: str: SD API URL - default is the beta 20191022 url
            debug: bool: print api calls and responses
            token: str: cached token from previous runs, default: None
            tokenexpires: float: timestamp for when the cached token expires, default: 0
        """
        try:
            self.username = username
            self.password = sha1password
            self.url = url
            self.debug = debug
            self.headers = {"User-Agent": f"{appname} / {__version__}"}
            self.token = token
            self.tokenexpires = tokenexpires
            self.online = False
            self.statusmsg = "initialising"
            self.lineups = None
            log.debug("SDApi initialising")
        except Exception as e:
            exci = sys.exc_info()[2]
            lineno = exci.tb_lineno
            fname = exci.tb_frame.f_code.co_name
            ename = type(e).__name__
            msg = f"{ename} Exception at line {lineno} in function {fname}: {e}"
            # print(msg)
            log.error(msg)
            raise

    def showResponse(self, jresp, force=False):
        """Pretty print json responses."""
        try:
            if self.debug or force:
                print(
                    json.dumps(jresp, indent=4, sort_keys=True), end="\n\n", flush=True
                )
        except Exception as e:
            exci = sys.exc_info()[2]
            lineno = exci.tb_lineno
            fname = exci.tb_frame.f_code.co_name
            ename = type(e).__name__
            msg = f"{ename} Exception at line {lineno} in function {fname}: {e}"
            # print(msg)
            log.error(msg)
            raise

    # Decorator function to call the API
    def apiNoToken(self, func):
        """Call the API, handle any errors, return the JSON payload."""

        def callFunc(*args, **kwargs):
            res = None
            try:
                res = func(*args, **kwargs)
            except Exception as e:
                log.error(f"{type(e).__name__} Exception in {func.__name__}:\n{e}")
                raise
            jresp = None
            try:
                res.raise_for_status()
                jresp = res.json()
            except Exception as e:
                log.error(
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
            if not self.token or self.tokenexpires < time.time():
                self.apiToken()
            self.headers["token"] = self.token

            @self.apiNoToken
            def callAPI():
                return func(*args, **kwargs)

            jresp = callAPI()
            del self.headers["token"]
            return jresp

        return callFunc

    def apiPost(self, route, postdict):
        """Post data to the SD API."""
        try:
            url = f"{self.url}/{route}"
            log.debug(
                f"POST request to {url}, headers: {self.headers}, params: {postdict}"
            )
            return requests.post(url, headers=self.headers, data=json.dumps(postdict))
        except Exception as e:
            exci = sys.exc_info()[2]
            lineno = exci.tb_lineno
            fname = exci.tb_frame.f_code.co_name
            ename = type(e).__name__
            msg = f"{ename} Exception at line {lineno} in function {fname}: {e}"
            # print(msg)
            log.error(msg)
            raise

    def apiGet(self, route, querydict={}):
        """Get data from the SD API."""
        try:
            url = f"{self.url}/{route}"
            log.debug(
                f"GET request to {url}, headers: {self.headers}, params: {querydict}"
            )
            return requests.get(url, headers=self.headers, params=querydict)
        except Exception as e:
            exci = sys.exc_info()[2]
            lineno = exci.tb_lineno
            fname = exci.tb_frame.f_code.co_name
            ename = type(e).__name__
            msg = f"{ename} Exception at line {lineno} in function {fname}: {e}"
            # print(msg)
            log.error(msg)
            raise

    def apiPut(self, route, querydict={}):
        """Put data to the SD API."""
        try:
            url = f"{self.url}/{route}"
            log.debug(
                f"PUT request to {url}, headers: {self.headers}, params: {querydict}"
            )
            return requests.put(url, headers=self.headers, params=querydict)
        except Exception as e:
            exci = sys.exc_info()[2]
            lineno = exci.tb_lineno
            fname = exci.tb_frame.f_code.co_name
            ename = type(e).__name__
            msg = f"{ename} Exception at line {lineno} in function {fname}: {e}"
            # print(msg)
            log.error(msg)
            raise

    def apiToken(self):
        """Obtain an API Token."""
        try:
            log.debug("Asking for a token")
            reqdata = {"username": self.username, "password": self.password}
            res = self.apiPost("token", reqdata)
            res.raise_for_status()
            jres = res.json()
            code = int(jres["code"])
            if code == 0:
                self.token = jres["token"]
                self.tokenexpires = datetime.datetime.strptime(
                    jres["datetime"], "%Y-%m-%dT%H:%M:%SZ"
                ).timestamp() + (3600 * 23)
                log.debug("Token obtained")
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
            # print(msg)
            log.error(msg)
            raise

    def apiOnline(self):
        """Obtain the status of the SD API"""
        try:

            @self.apiTokenRequired
            def sdapiOnline():
                return self.apiGet("status")

            xstatus = sdapiOnline()
            self.parseLatestStatus(xstatus)
            state = "ONLINE" if self.online else "OFFLINE"
            log.debug(f"{state}: {self.statusmsg}")
            if not self.online:
                raise Exception(f"SD API is Offline: {sd.statusmsg}")
            if "lineups" in xstatus:
                self.lineups = xstatus["lineups"]
        except Exception as e:
            exci = sys.exc_info()[2]
            lineno = exci.tb_lineno
            fname = exci.tb_frame.f_code.co_name
            ename = type(e).__name__
            msg = f"{ename} Exception at line {lineno} in function {fname}: {e}"
            # print(msg)
            log.error(msg)
            raise

    def parseLatestStatus(self, xstatus):
        """Find and parse the latest status message from the SD API."""
        try:
            if "systemStatus" in xstatus:
                latest = 0
                for xst in xstatus["systemStatus"]:
                    pdt = datetime.datetime.strptime(
                        xst["date"], "%Y-%m-%dT%H:%M:%SZ"
                    ).timestamp()
                    if pdt > latest:
                        latest = pdt
                        if xst["status"] == "Online":
                            self.online = True
                        else:
                            self.online = False
                        self.statusmsg = xst["message"]
        except Exception as e:
            exci = sys.exc_info()[2]
            lineno = exci.tb_lineno
            fname = exci.tb_frame.f_code.co_name
            ename = type(e).__name__
            msg = f"{ename} Exception at line {lineno} in function {fname}: {e}"
            # print(msg)
            log.error(msg)
            raise

    def available(self):
        """Retrieve the list of Services available from SD."""
        try:

            @self.apiNoToken
            def sdavailable():
                return self.apiGet("available")

            return sdavailable()
        except Exception as e:
            exci = sys.exc_info()[2]
            lineno = exci.tb_lineno
            fname = exci.tb_frame.f_code.co_name
            ename = type(e).__name__
            msg = f"{ename} Exception at line {lineno} in function {fname}: {e}"
            # print(msg)
            log.error(msg)
            raise

    def getLineups(self, countrycode, postcode):
        """Retrieve the lineups available for the country/postcode combo."""
        try:
            qs = {"country": countrycode, "postalcode": postcode}

            @self.apiTokenRequired
            def sdlineups():
                return self.apiGet("lineups", querydict=qs)

            return sdlineups()
        except Exception as e:
            exci = sys.exc_info()[2]
            lineno = exci.tb_lineno
            fname = exci.tb_frame.f_code.co_name
            ename = type(e).__name__
            msg = f"{ename} Exception at line {lineno} in function {fname}: {e}"
            # print(msg)
            log.error(msg)
            raise

    def preview(self, lineupcode):
        """Preview a lineup to determine the channel/station mapping."""
        try:

            @self.apiTokenRequired
            def sdpreview():
                return self.apiGet(f"lineups/preview/{lineupcode}")

            return sdpreview()
        except Exception as e:
            exci = sys.exc_info()[2]
            lineno = exci.tb_lineno
            fname = exci.tb_frame.f_code.co_name
            ename = type(e).__name__
            msg = f"{ename} Exception at line {lineno} in function {fname}: {e}"
            # print(msg)
            log.error(msg)
            raise

    def getLineup(self, lineupcode):
        """Retrieve the map of channel to stationid for the lineup."""
        try:

            @self.apiTokenRequired
            def sdgetlineup():
                return self.apiGet(f"lineups/{lineupcode}")

            return sdgetlineup()
        except Exception as e:
            exci = sys.exc_info()[2]
            lineno = exci.tb_lineno
            fname = exci.tb_frame.f_code.co_name
            ename = type(e).__name__
            msg = f"{ename} Exception at line {lineno} in function {fname}: {e}"
            # print(msg)
            log.error(msg)
            raise

    def putLineup(self, lineupcode):
        """Put the users lineup into their SD account."""
        try:

            @self.apiTokenRequired
            def sdputlineup():
                return self.apiPut(f"lineups/{lineupcode}")

            return sdputlineup()
        except Exception as e:
            exci = sys.exc_info()[2]
            lineno = exci.tb_lineno
            fname = exci.tb_frame.f_code.co_name
            ename = type(e).__name__
            msg = f"{ename} Exception at line {lineno} in function {fname}: {e}"
            # print(msg)
            log.error(msg)
            raise
