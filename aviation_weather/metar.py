"""Convenience module for getting METAR information from AviationWeather.gov."""

from .tools import aviation_weather, aviation_xml


def metars_xml(
    station: str, hours_before_now: int = 24, most_recent: bool = True
) -> bytes:
    """Fetch raw METAR XML from aviationweather.gov."""
    return aviation_xml("metar", station, hours_before_now, most_recent)


def metars(
    station: str, hours_before_now: int = 24, most_recent: bool = True
) -> str | list[str]:
    """Fetch METARs from aviationweather.gov."""
    return aviation_weather("metar", station, hours_before_now, most_recent)
