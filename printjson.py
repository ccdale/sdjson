#!/usr/bin/env python3

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

"""Utility to pretty print json data."""

import json
from pathlib import Path
import sys


def jprint():
    try:
        if len(sys.argv) == 1:
            raise Exception("Please supply file name")
        fn = Path(sys.argv[1])
        if fn.exists():
            with open(fn, "r") as ifn:
                jdata = json.load(ifn)
            print(json.dumps(jdata, indent=4, sort_keys=True), end="\n\n", flush=True)
        else:
            raise Exception(f"{fn} file does not exist")
    except Exception as e:
        exci = sys.exc_info()[2]
        lineno = exci.tb_lineno
        fname = exci.tb_frame.f_code.co_name
        ename = type(e).__name__
        msg = f"{ename} Exception at line {lineno} in function {fname}: {e}"
        print(msg)
        sys.exit(1)
