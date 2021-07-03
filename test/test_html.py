from sdjson.html import timeLine
from sdjson.html import makeTag
from sdjson.timedisplay import roundTime


def test_timeline():
    expected = """<tr class="timerow"><td colspan="1" class="timerowdata">Sat 03/07</td>
<td colspan="1" class="timerowdata">11:00</td>
<td colspan="1" class="timerowdata">11:30</td>
<td colspan="1" class="timerowdata">12:00</td>
<td colspan="1" class="timerowdata">12:30</td>
</tr>
"""
    # 1625308196 is Saturday 3rd  July 11:29
    start = roundTime(ts=1625308196, roundto="h")
    xstr = timeLine(start)
    assert xstr == expected


def test_tag_atts_string():
    tag = makeTag("p", "the data", "attribute")
    assert tag == "<p attribute>the data</p>"


def test_tag_atts_list():
    xl = ["colspan=1", "class='time'"]
    tag = makeTag("p", "the data", xl)
    assert tag == """<p colspan=1 class='time'>the data</p>"""


def test_tag_atts_dict():
    xd = {"colspan": 1, "class": "time"}
    tag = makeTag("p", "the data", xd)
    assert tag == """<p colspan="1" class="time">the data</p>"""
