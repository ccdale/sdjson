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

"""Database class for the ccasdtv application."""

from pathlib import Path
import sqlite3
import sys

from sdjson.ccabase import log
from sdjson.cache import SDCache
from sdjson.ccabase import Base


class SDDb(Base):
    def __init__(self, appname="ccasdtv"):
        try:
            sc = SDCache(appname)
            cd = sc.getCacheDir()
            dbfn = f"{appname}.db"
            self.dbpath = cd.joinpath(dbfn)
        except Exception as e:
            exci = sys.exc_info()[2]
            lineno = exci.tb_lineno
            fname = exci.tb_frame.f_code.co_name
            ename = type(e).__name__
            msg = f"{ename} Exception at line {lineno} in function {fname}: {e}"
            log.error(msg)
            raise

    def getConnection(self):
        try:
            self.connection = sqlite3.connect(self.dbpath)
        except Exception as e:
            exci = sys.exc_info()[2]
            lineno = exci.tb_lineno
            fname = exci.tb_frame.f_code.co_name
            ename = type(e).__name__
            msg = f"{ename} Exception at line {lineno} in function {fname}: {e}"
            log.error(msg)
            raise

    def doSql(self, sql, dictionary=True, one=False):
        try:
            self.get_connection()
            with self.connection:
                if dictionary:
                    self.connection.row_factory = sqlite3.Row
                cursor = self.connection.cursor()
                cursor.execute(sql)
                if one:
                    rows = cursor.fetchone()
                else:
                    rows = cursor.fetchall()
            self.connection.close()
            return rows
        except Exception as e:
            exci = sys.exc_info()[2]
            lineno = exci.tb_lineno
            fname = exci.tb_frame.f_code.co_name
            ename = type(e).__name__
            msg = f"{ename} Exception at line {lineno} in function {fname}: {e}"
            log.error(msg)
            raise

    def sql(self, sql, values=None):
        try:
            rows = None
            self.getConnection()
            with self.connection:
                log.debug(f"sql: {sql} values: {values}")
                c = self.connection.cursor()
                c.execute(sql) if values is None else c.execute(sql, values)
                rows = c.fetchall()
                log.debug(f"sql result: {rows}")
            self.connection.close()
            return rows
        except Exception as e:
            exci = sys.exc_info()[2]
            lineno = exci.tb_lineno
            fname = exci.tb_frame.f_code.co_name
            ename = type(e).__name__
            msg = f"{ename} Exception at line {lineno} in function {fname}: {e}"
            log.error(msg)
            raise

    def insertSql(self, sql, values):
        try:
            self.getConnection()
            with self.connection:
                log.debug(f"sql: {sql} values: {values}")
                c = self.connection.cursor()
                c.execute(sql, values)
                # log.debug(f"sql result: {rows}")
            self.connection.close()
            return True
        except sqlite3.IntegrityError:
            log.debug("Row already exists")
            return False
        except Exception as e:
            exci = sys.exc_info()[2]
            lineno = exci.tb_lineno
            fname = exci.tb_frame.f_code.co_name
            ename = type(e).__name__
            msg = f"{ename} Exception at line {lineno} in function {fname}: {e}"
            log.error(msg)
            raise

    def selectSql(self, sql, values):
        try:
            rows = None
            self.getConnection()
            with self.connection:
                log.debug(f"sql: {sql} values: {values}")
                c = self.connection.cursor()
                c.execute(sql, values)
                rows = c.fetchall()
                log.debug(f"sql result: {rows}")
            self.connection.close()
            return rows
        except Exception as e:
            exci = sys.exc_info()[2]
            lineno = exci.tb_lineno
            fname = exci.tb_frame.f_code.co_name
            ename = type(e).__name__
            msg = f"{ename} Exception at line {lineno} in function {fname}: {e}"
            log.error(msg)
            raise
