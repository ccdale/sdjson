#!/usr/bin/env python3
"""CLI for ccasdtv."""

from pathlib import Path
import sys

import ccalogging
import click

from sdjson.cache import makeCacheDir
from sdjson.config import readConfig
from sdjson.config import writeConfig
from sdjson.sdapi import SDApi
from sdjson import __version__

appname = "ccasdtv"
home = Path.home()

logfilename = home.joinpath(f"{appname}.log")
ccalogging.setLogFile(logfilename)
ccalogging.setDebug()
log = ccalogging.log

log.info(f"{appname} {__version__} CLI Starting")
