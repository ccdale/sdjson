import datetime
import sys
import time

import ccalogging

log = ccalogging.log


def addToString(xstr, xadd):
    """Appends the string `xadd` to the string `xstr`.

    if xadd is a list then each list member that is a string
    is appended to xstr

    Args:
        xstr: str input string
        xadd: list or str

    Raises:
        TypeError: Exception

    Returns:
        str:
    """
    try:
        if type(xstr) is str:
            op = xstr
        else:
            op = ""
        if type(xadd) is list:
            for xi in xadd:
                if type(xi) is str:
                    op += xi
        elif type(xadd) is str:
            op += xadd
        else:
            raise TypeError("Input format error. xadd is neither list nor string")
        return op
    except Exception as e:
        exci = sys.exc_info()[2]
        lineno = exci.tb_lineno
        fname = exci.tb_frame.f_code.co_name
        ename = type(e).__name__
        msg = f"{ename} Exception at line {lineno} in function {fname}: {e}"
        log.error(msg)
        raise


def padStr(xstr, xlen=2, pad=" ", padleft=True):
    """Pads the input string to be the required length.

    Args:
        xstr: str the input string
        xlen: int the required length
        pad: str the character or characters to pad with
        padleft: Bool

    Returns:
        str: the input string padded to the required length with pad
    """
    try:
        zstr = xstr
        while len(zstr) < xlen:
            if padleft:
                zstr = pad + zstr
            else:
                zstr += pad
        return zstr
    except Exception as e:
        exci = sys.exc_info()[2]
        lineno = exci.tb_lineno
        fname = exci.tb_frame.f_code.co_name
        ename = type(e).__name__
        msg = f"{ename} Exception at line {lineno} in function {fname}: {e}"
        log.error(msg)
        raise


def decomplexifyhms(tim, index, labels, labindex, oplen, colons=False):
    """Secondary function to remove some of the complexity of the hms function.

    Do not call this function directly

    Args:
        tim: list
        index: int
        labels: list
        labindex: int
        oplen: int
        colons: Bool

    Returns:
        list:
    """
    try:
        op = []
        if colons:
            delim = ":"
        else:
            delim = " " if labindex == 2 else ", "
            if index == 3:
                delim = " " if labindex == 2 else " and "
        if oplen > 0:
            op.append(delim)
        if colons:
            sval = padStr(str(tim[index]), pad="0")
        else:
            if labindex == 2:
                sval = str(tim[index]) + labels[labindex][index]
            else:
                sval = displayValue(tim[index], labels[labindex][index], zero=False)
        op.append(sval)
        return op
    except Exception as e:
        exci = sys.exc_info()[2]
        lineno = exci.tb_lineno
        fname = exci.tb_frame.f_code.co_name
        ename = type(e).__name__
        msg = f"{ename} Exception at line {lineno} in function {fname}: {e}"
        log.error(msg)
        raise


def reduceTime(unit, secs):
    """Performs the modulo function on secs.

    Args:
        unit: int the divisor
        secs: int a number

    Raises:
        ValueError: Exception

    Returns:
        tuple: (units: int, remainder: int)
    """
    try:
        rem = units = 0
        if unit > 0:
            units = int(secs / unit)
            rem = int(secs % unit)
        else:
            raise ValueError(
                f"divide by zero requested in reduceTime: unit: {unit}, secs: {secs}"
            )
        return (units, rem)
    except Exception as e:
        exci = sys.exc_info()[2]
        lineno = exci.tb_lineno
        fname = exci.tb_frame.f_code.co_name
        ename = type(e).__name__
        msg = f"{ename} Exception at line {lineno} in function {fname}: {e}"
        log.error(msg)
        raise


def displayValue(val, label, zero=True):
    """Pluralises the label.
    if zero is True val == 0 then the empty string is returned.
    Args:
        val: number
        label: str
        zero: Bool
    Raises:
        TypeError: Exception if val is not numeric
    Returns:
        str:
    """
    try:
        if zero and val == 0:
            return ""
        dlabel = label if val == 1 else label + "s"
        sval = str(val)
        if not sval.isnumeric():
            raise TypeError("input is not numeric")
        return addToString(sval, [" ", dlabel])
    except Exception as e:
        exci = sys.exc_info()[2]
        lineno = exci.tb_lineno
        fname = exci.tb_frame.f_code.co_name
        ename = type(e).__name__
        msg = f"{ename} Exception at line {lineno} in function {fname}: {e}"
        log.error(msg)
        raise


def hms(
    secs,
    small=True,
    short=True,
    single=False,
    colons=False,
    nodays=True,
    noseconds=False,
):
    """Convert `secs` to days, hours, minutes and seconds.

    if `small` is True then only return the higher values
    if they are > zero

    if `short` is True then the labels are their short form

    if `single` is True then the labels are single letters

    if `colons` is True then the output is of the form:
         01:03:23

    Args:
        secs: int the number of seconds
        small: Bool do not return day, hours or mins if they are zero
        short: Bool use short labels
        single: Bool use single letter labels
        colons: Bool return a string of the form 01:32:24

    Returns:
        str:
    """
    try:
        labs = [
            ["day", "hour", "minute", "second"],
            ["day", "hour", "min", "sec"],
            ["d", "h", "m", "s"],
        ]

        tim = [0, 0, 0, 0]
        units = [60 * 60 * 24, 60 * 60, 60]
        rem = secs
        for index in range(3):
            tim[index], rem = reduceTime(units[index], rem)
        tim[3] = rem
        op = []
        started = not small
        if single:
            cnlabs = 2
        else:
            cnlabs = 1 if short else 0
        start = 0 if not nodays else 1
        end = 4 if not noseconds else 3
        for cn in range(start, end):
            if not started and tim[cn] > 0:
                started = True
            if started:
                op += decomplexifyhms(tim, cn, labs, cnlabs, len(op), colons)
        msg = addToString("", op)
        return msg
    except Exception as e:
        exci = sys.exc_info()[2]
        lineno = exci.tb_lineno
        fname = exci.tb_frame.f_code.co_name
        ename = type(e).__name__
        msg = f"{ename} Exception at line {lineno} in function {fname}: {e}"
        log.error(msg)
        raise


def roundTime(roundto="h"):
    """
    Round the current time to the last time unit

    time units:
        "h" - hour
        "d" - day - returns midnight (today)

    returns a timestamp
    """
    try:
        if roundto == "d":
            today = datetime.date.today()
            midnight = int(time.mktime(today.timetuple()))
            return midnight
        elif roundto == "h":
            today = datetime.datetime.today()
            then = datetime.datetime(today.year, today.month, today.day, today.hour)
            tsthen = int(time.mktime(then.timetuple()))
            return tsthen
    except Exception as e:
        exci = sys.exc_info()[2]
        lineno = exci.tb_lineno
        fname = exci.tb_frame.f_code.co_name
        ename = type(e).__name__
        msg = f"{ename} Exception at line {lineno} in function {fname}: {e}"
        log.error(msg)
        raise
