"""Convenience module for getting METARS information from AviationWeather.gov"""

from .tools import aviation_weather, aviation_xml


def metars_xml(station, hours_before_now=24, most_recent=True):
    """get metars from aviationweather.gov"""
    return aviation_xml("metars", station, hours_before_now, most_recent)


def metars(station, hours_before_now=24, most_recent=True):
    """get metars from aviationweather.gov"""
    return aviation_weather("metars", station, hours_before_now, most_recent)
