#!/usr/bin/env python 

# portable serial port access with python
# this is a wrapper module for different platform implementations
#
# (C)2001-2002 Chris Liechti <cliechti@gmx.net>
# this is distributed under a free software license, see license.txt

VERSION = '2.5'

import sys

if sys.platform == 'cli':
    from serialcli import *
else:
    import os
    # chose an implementation, depending on os
    if os.name == 'nt': #sys.platform == 'win32':
        from serialwin32 import *
    elif os.name == 'posix':
        from serialposix import *
    elif os.name == 'java':
        from serialjava import *
    else:
        raise Exception("Sorry: no implementation for your platform ('%s') available" % os.name)


def serial_class_for_url(url, *args, **kwargs):
    """Get a native or a RFC2217 implementation of the Serial class, depending
    on port/url. The port is not opened when the keyword parameter
    'do_not_open' is true, by default it is."""
    # check remove extra parameter to not confuse the Serial class
    do_open = 'do_not_open' not in kwargs or not kwargs['do_not_open']
    if 'do_not_open' in kwargs: del kwargs['do_not_open']
    # check port type and get class
    if url.lower().startswith('rfc2217://'):
        import rfc2217  # late import, so that users that don't use it don't have to load it
        klass = rfc2217.Serial # RFC2217 implementation
    else:
        klass = Serial   # 'native' implementation
    # instantiate and open when desired
    instance = klass(None, *args, **kwargs)
    instance.port = url
    if do_open:
        instance.open()
    return instance