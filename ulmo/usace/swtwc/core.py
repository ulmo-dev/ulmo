from bs4 import BeautifulSoup


def get_stations():
    stations_url = 'http://www.swt-wc.usace.army.mil/shefids.htm'
    path = os.path.join(USACE_SWTWC_DIR, 'shefids.htm')

    with util.open_file_for_url(stations_url, path) as f:
        soup = BeautifulSoup(f)
        pre = soup.find('pre')
        links = pre.find_all('a')
        stations = [
            _parse_station_link(link) for link in links
        ]

    return dict([
        (station['code'], station)
        for station in stations
    ])


def _parse_station_link(link):
    return {
        'code': link.text,
        'description': link.next_sibling.strip(),
    }
