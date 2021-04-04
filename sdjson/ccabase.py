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

"""Base Class for ccasdtv application."""

import datetime
import sys

import ccalogging

log = ccalogging.log


class Base:
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

    def getTimeStamp(self, dt, dtformat="%Y-%m-%dT%H:%M:%SZ"):
        """Returns the integer epoch timestamp for the date time described by dt."""
        try:
            return int(datetime.datetime.strptime(dt, dtformat).timestamp())
        except Exception as e:
            exci = sys.exc_info()[2]
            lineno = exci.tb_lineno
            fname = exci.tb_frame.f_code.co_name
            ename = type(e).__name__
            msg = f"{ename} Exception at line {lineno} in function {fname}: {e}"
            log.error(msg)
            raise
