from __future__ import absolute_import

from . import core

from .core import (get_sites, get_site_data)

try:
    from . import pytables
except ImportError:
    from ulmo import util
    pytables = util.module_with_dependency_errors([
        'get_site',
        'get_site_data',
        'get_sites',
        'update_sites',
        'update_site_data',
    ])
