""" Convenience module for getting METARS information from AviationWeather.gov """
import argparse
from .tools import aviation_xml, aviation_weather

def metars_xml(station, hours_before_now=24, most_recent=True):
    """ get metars from aviationweather.gov """
    return aviation_xml("metars", station, hours_before_now, most_recent)

def metars(station, hours_before_now=24, most_recent=True):
    """ get metars from aviationweather.gov """
    return aviation_weather('metars', station, hours_before_now, most_recent)
