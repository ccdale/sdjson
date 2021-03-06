"""Routines to interact with Schedules Direct"""

import hashlib
import json
import sys

import requests

from sdjson.config import readConfig
from sdjson.config import writeConfig
from sdjson.db import SDDb
from sdjson.sdapi import SDApi
from sdjson import __version__

appname = "ccasdtv"
cfgdirty = False

cfg = readConfig(appname=appname)
if "username" not in cfg:
    cfg["username"] = input("Username: ")
    cfgdirty = True
if "password" not in cfg:
    password = input("Password: ")
    cfg["password"] = hashlib.sha1(password.encode()).hexdigest()
    cfgdirty = True


token = cfg["token"] if "token" in cfg else None
tokenexpires = cfg["tokenexpires"] if "tokenexpires" in cfg else 0
sd = SDApi(
    cfg["username"],
    cfg["password"],
    appname=appname,
    token=token,
    tokenexpires=tokenexpires,
    debug=False,
)

sd.apiOnline()
if not sd.online:
    print(sd.statusmsg)
    sys.exit(1)


avail = sd.available()

res = sd.putLineup("GBR-1000073-DEFAULT")
sd.showResponse(res, True)
# Sandy Heath Transmitter
# prv = sd.preview("GBR-1000073-DEFAULT")
# lineupmap = sd.getLineup("GBR-1000073-DEFAULT")
# sd.showResponse(lineupmap, True)


if cfg["token"] != sd.token:
    cfg["token"] = sd.token
    cfg["tokenexpires"] = sd.tokenexpires
    cfgdirty = True

if cfgdirty:
    writeConfig(cfg, appname=appname)
