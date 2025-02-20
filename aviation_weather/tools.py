from typing import OrderedDict
from lxml import html
import requests
import xmltodict


def aviation_xml(data_source, station, hours_before_now=24, most_recent=True):
    """ get metars or tafs from aviationweather.gov """
    uri = ('https://aviationweather.gov/api/data/dataserver?requestType=retrieve&dataSource={0}'+
           '&stationString={1}&hoursBeforeNow={2}&format=xml' +
           '&mostRecent={3}').format(data_source, station,
                                    hours_before_now, most_recent)
    page = requests.get(uri, headers={'accept': '*/*'})
    return page.content


def aviation_weather(data_source,
                     station,
                     hours_before_now=24,
                     most_recent=True,
                     return_readable=False):
    """ get metars or tafs from aviationweather.gov """
    page = aviation_xml(data_source, station, hours_before_now, most_recent)
    if return_readable and most_recent:
        return xml_to_readable(page, data_source)
    tree = html.fromstring(page)
    text = tree.xpath('//raw_text//text()')
    return text


def xml_to_readable(xml_page, data_source):
    odict = xmltodict.parse(xml_page, encoding='utf-8', process_namespaces=True)
    response = odict['response']['data']
    if data_source == 'metars':
        info = response['METAR']
        # Handle both single METAR and list of METARs
        if isinstance(info, list):
            info = info[0]  # Take the most recent one
        
        # Handle visibility with '+' symbol
        visibility = info.get('visibility_statute_mi', '')
        if visibility.endswith('+'):
            visibility = visibility.rstrip('+') + '+'
        
        # Handle wind information
        wind_info = f"{info.get('wind_dir_degrees', '')}° at {info.get('wind_speed_kt', '')} kt"
        if info.get('wind_gust_kt'):
            wind_info += f" (gusts {info.get('wind_gust_kt')} kt)"

        sky_cond_readable = parse_sky_condition(info.get('sky_condition', None))
        altimeter_rounded = round(float(info.get('altim_in_hg', '-1000')), 2)
        info_list = [f"Station: {info.get('station_id', '')}",
                     f"Observation Time: {info.get('observation_time', '')}",
                     f"Latitude: {info.get('latitude', '')}",
                     f"Longitude: {info.get('longitude', '')}",
                     f"Temperature: {info.get('temp_c', '')}°C",
                     f"Dewpoint: {info.get('dewpoint_c', '')}°C",
                     f"Wind: {wind_info}",
                     f"Visibility: {visibility} statute miles",
                     f"Altimeter: {altimeter_rounded} inHg",
                     f"Pressure: {info.get('sea_level_pressure_mb', '')} mb",
                     f"Sky conditions: {sky_cond_readable}",
                     f"Flight category: {info.get('flight_category', '')}",
                     f"Metar Type: {info.get('metar_type', '')}",
                     f"Elevation: {info.get('elevation_m', '')}m",
                     f"Raw: {info.get('raw_text', '')}"]
        formatted_info = '\n'.join(info_list)
    elif data_source == 'tafs':
        info = response['TAF']
        if isinstance(info, list):
            info = info[0]  # Take the most recent one
        formatted_info = info.get('raw_text', info)
    else:
        raise ValueError(f'Unknown data source {data_source}')

    return formatted_info


def parse_sky_condition(sky_cond):
    if sky_cond is None:
        return ''
    sky_cond_list = []
    # Handle formatting for unnested single observation.
    if isinstance(sky_cond, OrderedDict):
        sky_cond = [sky_cond]
    for lvl in sky_cond:
        altitude = lvl.get('@cloud_base_ft_agl', '')
        sky_cover = lvl.get('@sky_cover', '')
        altitude_text = f'{altitude}'
        if altitude_text != '':
            altitude_text += "AGL:"
        text = f'{altitude_text} {sky_cover}'
        sky_cond_list.append(text)
    sky_cond_readable = ', '.join(sky_cond_list)
    return sky_cond_readable
