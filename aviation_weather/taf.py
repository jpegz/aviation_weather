"""Convenience module for getting TAF information from AviationWeather.gov."""

from .tools import aviation_weather, aviation_xml


def tafs_xml(
    station: str, hours_before_now: int = 24, most_recent: bool = True
) -> bytes:
    """Fetch raw TAF XML from aviationweather.gov."""
    return aviation_xml("taf", station, hours_before_now, most_recent)


def tafs(
    station: str, hours_before_now: int = 24, most_recent: bool = True
) -> str | list[str]:
    """Fetch TAFs from aviationweather.gov."""
    return aviation_weather("taf", station, hours_before_now, most_recent)
