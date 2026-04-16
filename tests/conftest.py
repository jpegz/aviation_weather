"""Shared fixtures matching the real aviationweather.gov API response shapes.

JSON fixtures reflect the actual field names and types from /api/data/metar
and /api/data/taf with format=json.

XML fixtures reflect the actual response from those endpoints with format=xml,
which uses the legacy field names (altim_in_hg, station_id, etc.) regardless
of which endpoint version is called.
"""

import pytest

# ---------------------------------------------------------------------------
# JSON fixtures (used by aviation_weather / _fetch_json)
# ---------------------------------------------------------------------------

METAR_KJFK = {
    "icaoId": "KJFK",
    "receiptTime": "2024-01-15T12:54:13.000Z",
    "obsTime": 1705316400,
    "reportTime": "2024-01-15T13:00:00.000Z",
    "temp": 17.8,
    "dewp": 12.8,
    "wdir": 190,
    "wspd": 3,
    "visib": "10+",
    "altim": 1012.3,  # hPa — converted to inHg in _to_readable
    "slp": 1012.1,
    "qcField": 4,
    "metarType": "METAR",
    "rawOb": "METAR KJFK 160451Z 19003KT 10SM FEW065 SCT170 BKN250 18/13 A2989",
    "lat": 40.6392,
    "lon": -73.7639,
    "elev": 3,
    "name": "New York/JF Kennedy Intl, NY, US",
    "cover": "BKN",
    "clouds": [
        {"cover": "FEW", "base": 6500},
        {"cover": "SCT", "base": 17000},
        {"cover": "BKN", "base": 25000},
    ],
    "fltCat": "VFR",
}

# Same station with gusts — wgst is absent from the API when there are no gusts,
# so we add it explicitly here to test that branch.
METAR_KJFK_GUSTS = {
    **METAR_KJFK,
    "wspd": 15,
    "wgst": 25,
    "rawOb": "METAR KJFK 160451Z 18015G25KT 10SM FEW065 BKN250 18/13 A2989",
}

METAR_KLAX = {
    **METAR_KJFK,
    "icaoId": "KLAX",
    "rawOb": "METAR KLAX 160451Z 27010KT 10SM SKC 20/10 A2995",
    "name": "Los Angeles Intl, CA, US",
}

TAF_KJFK = {
    "icaoId": "KJFK",
    "bulletinTime": "2024-01-15T11:31:00.000Z",
    "issueTime": "2024-01-15T11:31:00.000Z",
    "rawTAF": "TAF KJFK 151130Z 1512/1618 18010KT P6SM FEW025 BKN250",
    "lat": 40.6392,
    "lon": -73.7639,
    "elev": 3,
    "name": "New York/JF Kennedy Intl",
}

# ---------------------------------------------------------------------------
# XML fixtures (used by aviation_xml)
# The new API returns the legacy XML schema when format=xml is requested,
# with field names like altim_in_hg, station_id, sky_condition, etc.
# ---------------------------------------------------------------------------

METAR_XML = (
    b'<?xml version="1.0" encoding="UTF-8"?>'
    b'<response version="2.0">'
    b'<data num_results="1">'
    b"<METAR>"
    b"<raw_text>"
    b"METAR KJFK 160451Z 19003KT 10SM FEW065 SCT170 BKN250 18/13 A2989"
    b"</raw_text>"
    b"<station_id>KJFK</station_id>"
    b"<observation_time>2024-01-15T13:00:00.000Z</observation_time>"
    b"<temp_c>17.8</temp_c>"
    b"<dewpoint_c>12.8</dewpoint_c>"
    b"<wind_dir_degrees>190</wind_dir_degrees>"
    b"<wind_speed_kt>3</wind_speed_kt>"
    b"<visibility_statute_mi>10+</visibility_statute_mi>"
    b"<altim_in_hg>29.89</altim_in_hg>"
    b"<sea_level_pressure_mb>1012.1</sea_level_pressure_mb>"
    b'<sky_condition sky_cover="FEW" cloud_base_ft_agl="6500"/>'
    b'<sky_condition sky_cover="SCT" cloud_base_ft_agl="17000"/>'
    b'<sky_condition sky_cover="BKN" cloud_base_ft_agl="25000"/>'
    b"<flight_category>VFR</flight_category>"
    b"<metar_type>METAR</metar_type>"
    b"<elevation_m>3</elevation_m>"
    b"</METAR>"
    b"</data>"
    b"</response>"
)

TAF_XML = (
    b'<?xml version="1.0" encoding="UTF-8"?>'
    b'<response version="1.1">'
    b'<data num_results="1">'
    b"<TAF>"
    b"<raw_text>"
    b"<![CDATA[TAF KJFK 151130Z 1512/1618 18010KT P6SM FEW025 BKN250]]>"
    b"</raw_text>"
    b"<station_id>KJFK</station_id>"
    b"<issue_time>2024-01-15T11:31:00.000Z</issue_time>"
    b"<valid_time_from>2024-01-15T12:00:00.000Z</valid_time_from>"
    b"<valid_time_to>2024-01-16T18:00:00.000Z</valid_time_to>"
    b"<latitude>40.6392</latitude>"
    b"<longitude>-73.7639</longitude>"
    b"<elevation_m>3.0</elevation_m>"
    b"</TAF>"
    b"</data>"
    b"</response>"
)


@pytest.fixture
def metar_kjfk():
    return METAR_KJFK


@pytest.fixture
def metar_kjfk_gusts():
    return METAR_KJFK_GUSTS


@pytest.fixture
def two_metars():
    return [METAR_KJFK, METAR_KLAX]


@pytest.fixture
def taf_kjfk():
    return TAF_KJFK


# Older record first, newer record second — deliberately reversed to verify
# that most_recent picks by reportTime, not by position.
METAR_KJFK_OLDER = {
    **METAR_KJFK,
    "reportTime": "2024-01-15T12:00:00.000Z",
    "rawOb": "METAR KJFK 160351Z 19003KT 10SM FEW065 18/13 A2988",
}
METAR_KJFK_NEWER = {
    **METAR_KJFK,
    "reportTime": "2024-01-15T13:00:00.000Z",
    "rawOb": "METAR KJFK 160451Z 19003KT 10SM FEW065 SCT170 BKN250 18/13 A2989",
}


@pytest.fixture
def metars_out_of_order():
    """Older record at index 0, newer at index 1 — reverse of API convention."""
    return [METAR_KJFK_OLDER, METAR_KJFK_NEWER]
