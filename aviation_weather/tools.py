import argparse
from lxml import html
import requests

def aviation_xml(data_source, station, hours_before_now: int=24, most_recent: bool=True):
    """ get metars or tafs from aviationweather.gov """
    uri = ('https://aviationweather.gov/adds/dataserver_current/httpparam?dataSource={0}'+
           '&requestType=retrieve&format=xml&stationString={1}&hoursBeforeNow={2}' +
           '&mostRecentForEachStation={3}').format(data_source, station,
                                                   hours_before_now, most_recent)
    page = requests.get(uri)
    return page.content

def aviation_weather(data_source, station, hours_before_now: int=24, most_recent: bool=True):
    """ get metars or tafs from aviationweather.gov """
    page = aviation_xml(data_source, station, hours_before_now, most_recent)
    tree = html.fromstring(page)
    text = tree.xpath('//raw_text//text()')
    return text


if __name__ == '__main__':
    PARSER = argparse.ArgumentParser(description='Get metars or tafs for the specified stations')
    PARSER.add_argument('--hours-before-now', required=False, default=24,
                        help='hours before now')
    PARSER.add_argument('--most-recent', '-r', required=False, default=False, action='store_true',
                        help='Only return most recent metars or tafs for the stations')
    PARSER.add_argument('data_source', choices=['metars', 'tafs'])
    PARSER.add_argument('stations', nargs='+',
                        help='station code or short code for multiple stations')
    ARGS = PARSER.parse_args()
    STATIONS = ','.join(ARGS.stations)
    RESULT = aviation_weather(ARGS.data_source, STATIONS,
                              ARGS.hours_before_now, ARGS.most_recent)
    if len(RESULT) > 0:
        print('\n'.join(RESULT))
