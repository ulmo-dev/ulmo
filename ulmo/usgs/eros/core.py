"""
    ulmo.usgs.eros.core
    ~~~~~~~~~~~~~~~~~~~~~

    This module provides access to data provided by the `United States Geological
    Survey`_ `Earth Resources Observation and Science (EROS) Center`_ application 
    services web site.

    The `DCP message format`_ includes some header information that is parsed and
    the message body, with a variable number of characters. The format of the
    message body varies widely depending on the manufacturer of the transmitter,
    data logger, sensors, and the technician who programmed the DCP. The body can
    be simple ASCII, sometime with parameter codes and time-stamps embedded,
    sometimes not. The body can also be in 'Pseudo-Binary' which is character
    encoding of binary data that uses 6 bits of every byte and guarantees that
    all characters are printable.


    .. _United States Geological Survey: http://www.usgs.gov/
    .. _Earth Resources Observation and Science (EROS) Center: http://nimbus.cr.usgs.gov/app_services.php

"""

import logging
import requests
import shutil
from ulmo import util


# eros services base urls
EROS_INVENTORY_URL = 'http://nimbus.cr.usgs.gov/index_service/Index_Service_JSON2.asmx'

# default file path (appended to default ulmo path)
DEFAULT_FILE_PATH = 'usgs/eros/'

# configure logging
LOG_FORMAT = '%(message)s'
logging.basicConfig(format=LOG_FORMAT)
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


def list_themes():
    url = EROS_INVENTORY_URL + '/return_Themes'
    return _call_service(url, {})


def _call_service(url, payload):
    payload['callback'] = ''
    r = requests.get(url, params=payload)
    return r.json()
