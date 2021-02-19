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
"""Configuration routines for the ccasdtv application."""

from pathlib import Path
import sys
import yaml


def writeConfig(config, appname="ccasdtv"):
    try:
        yamlfn = f"{appname}.yaml"
        home = Path.home()
        configfn = home.joinpath(".config", yamlfn)
        with open(str(configfn), "w") as cfn:
            yaml.dump(config, cfn, default_flow_style=False)
    except Exception as e:
        exci = sys.exc_info()[2]
        lineno = exci.tb_lineno
        fname = exci.tb_frame.f_code.co_name
        ename = type(e).__name__
        msg = f"{ename} Exception at line {lineno} in function {fname}: {e}"
        print(msg)
        raise


def readConfig(appname="ccasdtv"):
    try:
        config = {}
        yamlfn = "tvh.yaml"
        home = Path.home()
        configfn = home.joinpath(".config", yamlfn)
        with open(str(configfn), "r") as cfn:
            config = yaml.safe_load(cfn)
        return config
    except Exception as e:
        exci = sys.exc_info()[2]
        lineno = exci.tb_lineno
        fname = exci.tb_frame.f_code.co_name
        ename = type(e).__name__
        msg = f"{ename} Exception at line {lineno} in function {fname}: {e}"
        print(msg)
        raise
