from lxml import html
import requests

def aviation_xml(data_source, station, hours_before_now=24, most_recent=True):
    """ get metars or tafs from aviationweather.gov """
    uri = ('https://aviationweather.gov/adds/dataserver_current/httpparam?dataSource={0}'+
           '&requestType=retrieve&format=xml&stationString={1}&hoursBeforeNow={2}' +
           '&mostRecentForEachStation={3}').format(data_source, station,
                                                   hours_before_now, most_recent)
    page = requests.get(uri)
    return page.content

def aviation_weather(data_source, station, hours_before_now=24, most_recent=True):
    """ get metars or tafs from aviationweather.gov """
    page = aviation_xml(data_source, station, hours_before_now, most_recent)
    tree = html.fromstring(page)
    text = tree.xpath('//raw_text//text()')
    return text
