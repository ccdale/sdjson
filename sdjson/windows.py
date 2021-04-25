import sys

import PySimpleGUI as sg


def credsWindow(username):
    try:
        log.debug("opening credentials window.")
        layout = [
            [sg.T("Password will stored in the system keyring.")],
            [sg.T("SD Username"), sg.I(username, key="UIN")],
            [sg.T("SD Password"), sg.I(key="PIN")],
            [sg.Submit(key="submit"), sg.Cancel(key="cancel")],
        ]
        window = sg.Window("Schedules Direct Credentials.", layout)
        event, values = window.read()
        window.close()
        log.debug("credentials window closed.")
        un = pw = None
        if event == "submit":
            un = values["UIN"]
            pw = values["PIN"]
        if "PIN" in values:
            values["PIN"] = "xxxxxxxxxx"
        log.debug(f"event: {event}, values: {values}")
        return un, pw
    except Exception as e:
        exci = sys.exc_info()[2]
        lineno = exci.tb_lineno
        fname = exci.tb_frame.f_code.co_name
        ename = type(e).__name__
        msg = f"{ename} Exception at line {lineno} in function {fname}: {e}"
        log.error(msg)
        raise
