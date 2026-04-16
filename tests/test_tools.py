"""Tests for aviation_weather/tools.py.

Each test verifies a specific behavior against realistic API response shapes.
HTTP calls are mocked with the `responses` library so tests run offline and
do not depend on aviationweather.gov availability.
"""

import pytest
import requests
import responses as rsps

from aviation_weather.tools import (
    _HPA_TO_INHG,
    _fetch_json,
    _parse_clouds,
    _to_readable,
    _validate_source,
    aviation_weather,
    aviation_xml,
)

from .conftest import METAR_XML, TAF_XML

BASE = "https://aviationweather.gov/api/data"


# ---------------------------------------------------------------------------
# _validate_source
# ---------------------------------------------------------------------------


def test_validate_source_metar_ok():
    _validate_source("metar")  # must not raise


def test_validate_source_taf_ok():
    _validate_source("taf")  # must not raise


def test_validate_source_invalid():
    with pytest.raises(ValueError, match="Unknown data source"):
        _validate_source("metars")  # old plural name — should now fail


# ---------------------------------------------------------------------------
# _fetch_json
# ---------------------------------------------------------------------------


@rsps.activate
def test_fetch_json_metar_url(metar_kjfk):
    rsps.add(rsps.GET, f"{BASE}/metar", json=[metar_kjfk])
    _fetch_json("metar", "KJFK", hours_before_now=24)
    assert len(rsps.calls) == 1
    url = rsps.calls[0].request.url
    assert "ids=KJFK" in url
    assert "hours=24" in url
    assert "format=json" in url


@rsps.activate
def test_fetch_json_taf_url(taf_kjfk):
    rsps.add(rsps.GET, f"{BASE}/taf", json=[taf_kjfk])
    _fetch_json("taf", "KJFK")
    assert "/taf" in rsps.calls[0].request.url


@rsps.activate
def test_fetch_json_returns_list(metar_kjfk):
    rsps.add(rsps.GET, f"{BASE}/metar", json=[metar_kjfk])
    result = _fetch_json("metar", "KJFK")
    assert isinstance(result, list)
    assert result[0]["icaoId"] == "KJFK"


@rsps.activate
def test_fetch_json_raises_on_http_error():
    rsps.add(rsps.GET, f"{BASE}/metar", status=500)
    with pytest.raises(requests.HTTPError):
        _fetch_json("metar", "KJFK")


def test_fetch_json_invalid_source():
    with pytest.raises(ValueError):
        _fetch_json("metars", "KJFK")


# ---------------------------------------------------------------------------
# aviation_xml
# ---------------------------------------------------------------------------


@rsps.activate
def test_aviation_xml_metar_url():
    rsps.add(rsps.GET, f"{BASE}/metar", body=METAR_XML)
    aviation_xml("metar", "KJFK", hours_before_now=6)
    url = rsps.calls[0].request.url
    assert "format=xml" in url
    assert "ids=KJFK" in url
    assert "hours=6" in url


@rsps.activate
def test_aviation_xml_returns_bytes():
    rsps.add(rsps.GET, f"{BASE}/metar", body=METAR_XML)
    result = aviation_xml("metar", "KJFK")
    assert isinstance(result, bytes)
    assert b"<METAR>" in result


@rsps.activate
def test_aviation_xml_taf_returns_bytes():
    rsps.add(rsps.GET, f"{BASE}/taf", body=TAF_XML)
    result = aviation_xml("taf", "KJFK")
    assert isinstance(result, bytes)
    assert b"<TAF>" in result


def test_aviation_xml_invalid_source():
    with pytest.raises(ValueError):
        aviation_xml("tafs", "KJFK")


# ---------------------------------------------------------------------------
# aviation_weather — raw text mode
# ---------------------------------------------------------------------------


@rsps.activate
def test_aviation_weather_raw_most_recent(metar_kjfk):
    rsps.add(rsps.GET, f"{BASE}/metar", json=[metar_kjfk])
    result = aviation_weather("metar", "KJFK", most_recent=True)
    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0] == metar_kjfk["rawOb"]


@rsps.activate
def test_aviation_weather_most_recent_by_report_time_not_position(metars_out_of_order):
    """most_recent must select the record with the latest reportTime,
    not whichever record happens to be at index 0."""
    rsps.add(rsps.GET, f"{BASE}/metar", json=metars_out_of_order)
    result = aviation_weather("metar", "KJFK", most_recent=True)
    assert len(result) == 1
    # The newer record is at index 1 in the fixture — we must still get it.
    from .conftest import METAR_KJFK_NEWER
    assert result[0] == METAR_KJFK_NEWER["rawOb"]


@rsps.activate
def test_aviation_weather_raw_all_results(two_metars):
    rsps.add(rsps.GET, f"{BASE}/metar", json=two_metars)
    result = aviation_weather("metar", "KJFK,KLAX", most_recent=False)
    assert len(result) == 2
    assert result[0] == two_metars[0]["rawOb"]
    assert result[1] == two_metars[1]["rawOb"]


@rsps.activate
def test_aviation_weather_raw_taf(taf_kjfk):
    rsps.add(rsps.GET, f"{BASE}/taf", json=[taf_kjfk])
    result = aviation_weather("taf", "KJFK", most_recent=True)
    assert result == [taf_kjfk["rawTAF"]]


@rsps.activate
def test_aviation_weather_empty_response():
    rsps.add(rsps.GET, f"{BASE}/metar", json=[])
    result = aviation_weather("metar", "KJFK")
    assert result == []


@rsps.activate
def test_aviation_weather_empty_response_readable():
    rsps.add(rsps.GET, f"{BASE}/metar", json=[])
    result = aviation_weather("metar", "KJFK", return_readable=True)
    assert result == ""


# ---------------------------------------------------------------------------
# aviation_weather — readable mode
# ---------------------------------------------------------------------------


@rsps.activate
def test_aviation_weather_readable_metar(metar_kjfk):
    rsps.add(rsps.GET, f"{BASE}/metar", json=[metar_kjfk])
    result = aviation_weather("metar", "KJFK", return_readable=True)
    assert isinstance(result, str)
    assert "Station: KJFK" in result
    assert "Temperature: 17.8°C" in result
    assert "Dewpoint: 12.8°C" in result
    assert "Wind: 190° at 3 kt" in result
    assert "Visibility: 10+ statute miles" in result
    assert "Flight category: VFR" in result
    assert "Metar Type: METAR" in result
    assert metar_kjfk["rawOb"] in result


@rsps.activate
def test_aviation_weather_readable_metar_altim_conversion(metar_kjfk):
    # altim in JSON is hPa (1012.3); output must show inHg (29.89)
    rsps.add(rsps.GET, f"{BASE}/metar", json=[metar_kjfk])
    result = aviation_weather("metar", "KJFK", return_readable=True)
    expected_inhg = str(round(metar_kjfk["altim"] * _HPA_TO_INHG, 2))
    assert f"Altimeter: {expected_inhg} inHg" in result


@rsps.activate
def test_aviation_weather_readable_taf(taf_kjfk):
    rsps.add(rsps.GET, f"{BASE}/taf", json=[taf_kjfk])
    result = aviation_weather("taf", "KJFK", return_readable=True)
    assert result == taf_kjfk["rawTAF"]


# ---------------------------------------------------------------------------
# _to_readable — unit tests for specific formatting logic
# ---------------------------------------------------------------------------


def test_to_readable_metar_no_gusts(metar_kjfk):
    result = _to_readable(metar_kjfk, "metar")
    assert "gusts" not in result


def test_to_readable_metar_with_gusts(metar_kjfk_gusts):
    result = _to_readable(metar_kjfk_gusts, "metar")
    assert "gusts 25 kt" in result


def test_to_readable_invalid_source(metar_kjfk):
    with pytest.raises(ValueError, match="Unknown data source"):
        _to_readable(metar_kjfk, "metar_x")


def test_to_readable_taf_returns_raw(taf_kjfk):
    result = _to_readable(taf_kjfk, "taf")
    assert result == taf_kjfk["rawTAF"]


# ---------------------------------------------------------------------------
# _parse_clouds
# ---------------------------------------------------------------------------


def test_parse_clouds_none():
    assert _parse_clouds(None) == ""


def test_parse_clouds_empty_list():
    assert _parse_clouds([]) == ""


def test_parse_clouds_single_layer():
    clouds = [{"cover": "FEW", "base": 2500}]
    assert _parse_clouds(clouds) == "2500AGL: FEW"


def test_parse_clouds_multiple_layers():
    clouds = [
        {"cover": "FEW", "base": 6500},
        {"cover": "SCT", "base": 17000},
        {"cover": "BKN", "base": 25000},
    ]
    result = _parse_clouds(clouds)
    assert result == "6500AGL: FEW, 17000AGL: SCT, 25000AGL: BKN"
