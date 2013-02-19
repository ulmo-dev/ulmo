from bs4 import BeautifulSoup
import requests


def get_stations():
    stations_url = 'http://www.swt-wc.usace.army.mil/shefids.htm'

    req = requests.get(stations_url)
    soup = BeautifulSoup(req.text)
    pre = soup.find('pre')
    links = pre.find_all('a')
    stations = [
        _parse_station_link(link) for link in links
    ]

    return dict([
        (station['code'], station)
        for station in stations
    ])

    return stations


def _parse_station_link(link):
    return {
        'code': link.text,
        'description': link.next_sibling.strip(),
    }
