import pytest
from sdjson.schedule import extractData


def test_extractData():
    d = {"titles": [{"title120": "some title"}]}
    tit = extractData(d, "titles", "title120", True)
    assert tit == "some title"


def test_simpleExtractData():
    d = {"event": {"details": "series"}}
    tit = extractData(d, "event", "details")
    assert tit == "series"
