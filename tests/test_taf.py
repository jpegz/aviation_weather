"""Tests for aviation_weather/taf.py.

These verify that the tafs() and tafs_xml() convenience wrappers pass
the correct data_source ("taf") and forward all parameters to tools.py.
"""

import responses as rsps

from aviation_weather.taf import tafs, tafs_xml

from .conftest import TAF_KJFK, TAF_XML

BASE = "https://aviationweather.gov/api/data"


@rsps.activate
def test_tafs_uses_taf_endpoint():
    rsps.add(rsps.GET, f"{BASE}/taf", json=[TAF_KJFK])
    tafs("KJFK")
    assert "/taf" in rsps.calls[0].request.url
    assert "/tafs" not in rsps.calls[0].request.url


@rsps.activate
def test_tafs_returns_raw_string_list():
    rsps.add(rsps.GET, f"{BASE}/taf", json=[TAF_KJFK])
    result = tafs("KJFK")
    assert result == [TAF_KJFK["rawTAF"]]


@rsps.activate
def test_tafs_passes_hours_before_now():
    rsps.add(rsps.GET, f"{BASE}/taf", json=[TAF_KJFK])
    tafs("KJFK", hours_before_now=12)
    assert "hours=12" in rsps.calls[0].request.url


@rsps.activate
def test_tafs_xml_uses_xml_format():
    rsps.add(rsps.GET, f"{BASE}/taf", body=TAF_XML)
    result = tafs_xml("KJFK")
    assert "format=xml" in rsps.calls[0].request.url
    assert isinstance(result, bytes)
