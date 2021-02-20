"""Database class for the ccasdtv application."""

import sqlite3
from pathlib import Path


class SDDb:
    def __init__(self, appname="ccasdtv"):
        try:
            dbfn = f"{appname}.db"
            home = Path.home()
            self.dbpath = home.joinpath(".config", dbfn)
        except Exception as e:
            exci = sys.exc_info()[2]
            lineno = exci.tb_lineno
            fname = exci.tb_frame.f_code.co_name
            ename = type(e).__name__
            msg = f"{ename} Exception at line {lineno} in function {fname}: {e}"
            print(msg)
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
            print(msg)
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
            print(msg)
            raise
