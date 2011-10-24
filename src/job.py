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
import os
import fnmatch
import string

from   liche.log       import logger

import liche.utils
import liche.file
import liche.directory

class Job(object):
    def __init__(self, path, licenses, ignore_filename = None):
        logger.debug("Initializing job for path '%s'" % path)

        liche.utils.directory_exists_barrier(path)

        self.__filefactory = liche.file.FileFactory()
        self.__licenses    = licenses
        self.__walker      = liche.directory.Walker(path, ignore_filename)
        self.__stream      = None

        logger.debug("Job ready")

    def __repr__(self):
        return "Job<%s>" % self.__walker.root()

    def __check_file(self, filename):
        logger.debug("Checking file '%s'" % filename)

        f = self.__filefactory.get(filename)
        f.slurp(self.__slurp_lines)

        confidencies = dict()
        for l in self.__licenses:
            confidencies[l.name()] = l.match(f)

        assert(self.__stream is not None)

        format = list()
        for c in confidencies.keys():
            d = confidencies[c]
            assert(d >= 0)
            if d == 0:
                continue
            format.append("%s (%02.02f)" % (c, d))
        if len(format) == 0:
            format.append("?")

        self.__stream.write("%s: %s\n" %
                            (f.path(), string.join(format, ", ")))

    def __show_file(self, filename):
        logger.debug("Showing file '%s'" % filename)

        f = self.__filefactory.get(filename)

        assert(self.__stream is not None)

        self.__stream.write("%s\n" % f.path())

    def __run(self, stream, dry):
        callback = None
        if dry:
            logger.info("Dry-running job for path '%s'" % self.__walker.root())

            callback = self.__show_file
        else:
            logger.info("Running job for path '%s'" % self.__walker.root())

            max_lines = 0
            for l in self.__licenses:
                max_lines          = max(max_lines, l.lines())
                self.__slurp_lines = 2 * max_lines

            logger.debug("Slurping %d maximum lines for each file" %
                         self.__slurp_lines)

            callback = self.__check_file
        assert(callback is not None)

        self.__stream = stream
        self.__walker.run(file_callback = callback)
        self.__stream = None

    def run(self, stream, dry = False):
        #try:
        self.__run(stream, dry)
        #except Exception, e:
        #    logger.error("%s" % str(e))
        #    return False
        return True
