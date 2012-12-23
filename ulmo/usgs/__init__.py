from __future__ import absolute_import

from . import core

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
