#
# Copyright (C) 2008, 2009 Francesco Salvestrini
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#

import sys
import logging

logger  = None
handler = None

def debug_off():
    logging.disable(logging.DEBUG)

def info_off():
    logging.disable(logging.INFO)

def setup(prefix):
    global logger

    logger = logging.getLogger(prefix)
    assert(logger is not None)

    logger.setLevel(logging.DEBUG)

    handler = logging.StreamHandler(sys.stdout)
    assert(handler is not None)

    handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter("%(levelname)s: %(message)s")
    assert(formatter is not None)

    handler.setFormatter(formatter)
    logger.addHandler(handler)
