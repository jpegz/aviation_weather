""" Convenience module for getting TAFS information from AviationWeather.gov """
import argparse
from .tools import aviation_xml, aviation_weather

def tafs_xml(station, hours_before_now=24, most_recent=True):
    """ get tafs from aviationweather.gov """
    return aviation_xml("tafs", station, hours_before_now, most_recent)

def tafs(station, hours_before_now=24, most_recent=True):
    """ get tafs from aviationweather.gov """
    return aviation_weather('tafs', station, hours_before_now, most_recent)


if __name__ == '__main__':
    PARSER = argparse.ArgumentParser(description='Get tafs for the specified stations')
    PARSER.add_argument('--hours-before-now', required=False, default=24,
                        help='hours before now')
    PARSER.add_argument('--most-recent', '-r', required=False, default=False, action='store_true',
                        help='Only return most recent tafs for the stations')
    PARSER.add_argument('stations', nargs='+',
                        help='station code or short code for multiple stations')
    ARGS = PARSER.parse_args()
    STATIONS = ','.join(ARGS.stations)
    RESULT = tafs(STATIONS, ARGS.hours_before_now, ARGS.most_recent)
    if len(RESULT) > 0:
        print('\n'.join(RESULT))
