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

import os

def path_exists_barrier(path):
    if not os.path.exists(path):
        raise Exception("Path '%s' does not exist" % path)

def file_exists_barrier(path):
    path_exists_barrier(path)
    if not os.path.isfile(path):
        raise Exception("Path '%s' is not a file" % path)

def directory_exists_barrier(path):
    path_exists_barrier(path)
    if not os.path.isdir(path):
        raise Exception("Path '%s' is not a directory" % path)

def string_replace_all(string, mappings):
    for key, value in mappings.iteritems():
        string = string.replace(key, value)
    return string
