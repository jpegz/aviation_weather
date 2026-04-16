import requests

_VALID_SOURCES = {"metar", "taf"}
_BASE_URL = "https://aviationweather.gov/api/data"
_HPA_TO_INHG = 0.02953


def _validate_source(data_source: str) -> None:
    if data_source not in _VALID_SOURCES:
        raise ValueError(
            f"Unknown data source: {data_source!r}. Must be 'metar' or 'taf'."
        )


def _fetch_json(
    data_source: str, station: str, hours_before_now: int = 24
) -> list[dict]:
    _validate_source(data_source)
    url = (
        f"{_BASE_URL}/{data_source}?ids={station}&hours={hours_before_now}&format=json"
    )
    r = requests.get(url, headers={"accept": "application/json"})
    r.raise_for_status()
    return r.json()


def aviation_xml(
    data_source: str,
    station: str,
    hours_before_now: int = 24,
    most_recent: bool = True,  # kept for backward compat, unused by new API
) -> bytes:
    """Fetch raw XML for metar or taf from aviationweather.gov."""
    _validate_source(data_source)
    url = f"{_BASE_URL}/{data_source}?ids={station}&hours={hours_before_now}&format=xml"
    r = requests.get(url, headers={"accept": "*/*"})
    r.raise_for_status()
    return r.content


def aviation_weather(
    data_source: str,
    station: str,
    hours_before_now: int = 24,
    most_recent: bool = True,
    return_readable: bool = False,
) -> str | list[str]:
    """Fetch metar or taf from aviationweather.gov.

    Returns a formatted string when return_readable=True and most_recent=True,
    otherwise a list of raw text strings (one per record).
    """
    records = _fetch_json(data_source, station, hours_before_now)
    if not records:
        return "" if return_readable else []
    if return_readable and most_recent:
        return _to_readable(records[0], data_source)
    raw_field = "rawOb" if data_source == "metar" else "rawTAF"
    raw_texts = [r.get(raw_field, "") for r in records]
    return raw_texts[:1] if most_recent else raw_texts


def _parse_clouds(clouds: list[dict] | None) -> str:
    if not clouds:
        return ""
    parts = [f"{c.get('base', '')}AGL: {c.get('cover', '')}" for c in clouds]
    return ", ".join(parts)


def _to_readable(record: dict, data_source: str) -> str:
    if data_source == "metar":
        wind = f"{record.get('wdir', '')}° at {record.get('wspd', '')} kt"
        if record.get("wgst"):
            wind += f" (gusts {record['wgst']} kt)"

        altim = record.get("altim")
        altim_str = str(round(altim * _HPA_TO_INHG, 2)) if altim is not None else ""

        return "\n".join(
            [
                f"Station: {record.get('icaoId', '')}",
                f"Observation Time: {record.get('reportTime', '')}",
                f"Latitude: {record.get('lat', '')}",
                f"Longitude: {record.get('lon', '')}",
                f"Temperature: {record.get('temp', '')}°C",
                f"Dewpoint: {record.get('dewp', '')}°C",
                f"Wind: {wind}",
                f"Visibility: {record.get('visib', '')} statute miles",
                f"Altimeter: {altim_str} inHg",
                f"Pressure: {record.get('slp', '')} mb",
                f"Sky conditions: {_parse_clouds(record.get('clouds'))}",
                f"Flight category: {record.get('fltCat', '')}",
                f"Metar Type: {record.get('metarType', '')}",
                f"Elevation: {record.get('elev', '')}m",
                f"Raw: {record.get('rawOb', '')}",
            ]
        )
    elif data_source == "taf":
        return record.get("rawTAF", str(record))
    raise ValueError(f"Unknown data source: {data_source!r}")


# Backward-compatible aliases
xml_to_readable = _to_readable
parse_sky_condition = _parse_clouds
