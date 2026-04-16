"""Tests for aviation_weather/metar.py.

These verify that the metars() and metars_xml() convenience wrappers pass
the correct data_source ("metar") and forward all parameters to tools.py.
"""

import responses as rsps

from aviation_weather.metar import metars, metars_xml

from .conftest import METAR_KJFK, METAR_XML

BASE = "https://aviationweather.gov/api/data"


@rsps.activate
def test_metars_uses_metar_endpoint():
    rsps.add(rsps.GET, f"{BASE}/metar", json=[METAR_KJFK])
    metars("KJFK")
    assert "/metar" in rsps.calls[0].request.url
    assert "/metars" not in rsps.calls[0].request.url


@rsps.activate
def test_metars_returns_raw_string_list():
    rsps.add(rsps.GET, f"{BASE}/metar", json=[METAR_KJFK])
    result = metars("KJFK")
    assert result == [METAR_KJFK["rawOb"]]


@rsps.activate
def test_metars_passes_hours_before_now():
    rsps.add(rsps.GET, f"{BASE}/metar", json=[METAR_KJFK])
    metars("KJFK", hours_before_now=6)
    assert "hours=6" in rsps.calls[0].request.url


@rsps.activate
def test_metars_xml_uses_xml_format():
    rsps.add(rsps.GET, f"{BASE}/metar", body=METAR_XML)
    result = metars_xml("KJFK")
    assert "format=xml" in rsps.calls[0].request.url
    assert isinstance(result, bytes)
