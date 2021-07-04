from sdjson.html import timeLine
from sdjson.html import makeColspan
from sdjson.html import makeTag
from sdjson.timedisplay import roundTime


def test_timeline():
    # 1625308196 is Saturday 3rd  July 11:29
    start = roundTime(ts=1625308196, roundto="h")
    xstr = timeLine(start)
    assert xstr.startswith("<tr class='timerow'>")
    assert xstr.endswith("</tr>\n")
    assert "<td colspan=1 class='timerowdata'>" in xstr
    assert "Sat 03/07/2021" in xstr
    assert "<a href=/grid?offset=-86400>" in xstr


def test_tag_atts_string():
    tag = makeTag("p", "the data", "attribute")
    assert tag == "<p attribute>the data</p>"


def test_tag_atts_list():
    xl = ["colspan=1", "class='time'"]
    tag = makeTag("p", "the data", xl)
    assert tag == """<p colspan=1 class='time'>the data</p>"""


def test_tag_atts_dict():
    xd = {"colspan": 1, "class": '"time"'}
    tag = makeTag("p", "the data", xd)
    assert tag == """<p colspan=1 class="time">the data</p>"""


def test_make_colspan():
    cp = makeColspan(
        tablestart=tablestart, progstart=progstart, progdur=progdur, colwidth=300
    )
