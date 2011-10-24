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
import re
import fnmatch

from   liche.log import logger

import liche.utils

class Glob(object):
    def __init__(self, basepath, pattern):
        assert(basepath is not None)
        assert(pattern  is not None)

        self.__inclusive = None

        pattern = pattern.strip()

        if pattern[0] == '!':
            # Inclusive pattern
            self.__inclusive = True
            pattern = pattern[1:]
        else:
            # Exclusive pattern
            self.__inclusive = False

        self.__glob = self.__parse_pattern(basepath, pattern)

    def __str__(self):
        s = "EXCLUSIVE"
        if self.__inclusive:
            s = "INCLUSIVE"
        return "Glob<'%s', %s>" % (self.__glob, s)

    def pattern(self):
        return self.__glob

    def is_inclusive(self):
        return self.__inclusive

    def __parse_pattern(self, base, pattern):
        assert(pattern == pattern.strip())

        glob = None
        if pattern[0] == '/':
            # Absolute glob
            tmp = pattern[1:].strip()
            glob = os.path.join(base, tmp)
        else:
            # Relative glob
            glob = pattern
        assert(glob is not None)

        logger.debug("Demangled glob '%s' is '%s'" % (pattern, glob))

        return glob

    def match(self, string):
        assert(string is not None)

        if fnmatch.fnmatch(string, self.__glob):
            return True
        return False

class GlobsFile(object):
    def __init__(self, path):
        self.__globs = list()

        logger.debug("Got globs file '%s' to handle" % path)

        liche.utils.file_exists_barrier(path)

        fh   = open(path, 'r')
        ln   = 0
        base = os.path.abspath(os.path.dirname(path))

        while True:
            line = fh.readline()
            if len(line) == 0:
                break
            ln = ln + 1

            line = line.rstrip('\n')

            if re.match(r'^[ \t]*#.*$', line) or re.match(r'^[ \t]*$', line):
                #logger.debug("Skipping comment/empty line")
                continue

            self.__globs.append(Glob(base, line))

        fh.close()

        logger.debug("Got %d globs: %s" %
                     (len(self.__globs), map(str, self.__globs)))

    def globs(self):
        return self.__globs

class Walker(object):
    def __init__(self, root, ignore = None):
        assert(root is not None)

        self.__root   = root
        self.__ignore = ignore
        self.__globs  = list()

    def root(self):
        return self.__root

    def __walk(self,
               root,
               file_callback,
               directory_callback,
               globs):

        assert(globs is not None)

        current_dir = os.path.abspath(root)

        logger.debug("Walking directory '%s'" % current_dir)

        entries = os.listdir(current_dir)
        logger.debug("Directory entries are: '%s'" % entries)

        assert("."  not in entries)
        assert(".." not in entries)

        if (self.__ignore is not None) and (self.__ignore in entries):
            p = os.path.join(current_dir, self.__ignore)
            logger.debug("Found ignore file '%s'" % p)

            gf = GlobsFile(p)
            logger.debug("Globs file parsed successfully")

            gl = gf.globs()
            logger.debug("Ignore file '%s' produced %d globs" %
                         (p, len(gl)))

            globs = globs + gl
            logger.debug("Globs are now %d" % len(globs))
            entries.remove(self.__ignore)

        assert(self.__ignore not in entries)
        assert(globs is not None)

        logger.debug("We have %d globs for directory '%s': %s" %
                     (len(globs), current_dir, map(str, globs)))

        for entry in entries:
            rel_path = entry
            abs_path = os.path.abspath(os.path.join(current_dir, rel_path))

            assert(not os.path.isabs(rel_path))
            assert(    os.path.isabs(abs_path))

            skip = False
            for g in globs:
                x = None
                if g.match(rel_path):
                    logger.debug("Relative path '%s' got a match with '%s'" %
                                 (rel_path, g.pattern()))
                    if g.is_inclusive():
                        skip = False
                    else:
                        skip = True
                    continue

                if g.match(abs_path):
                    logger.debug("Absolute path '%s' got a match with '%s'" %
                                 (abs_path, g.pattern()))
                    if g.is_inclusive():
                        skip = False
                    else:
                        skip = True
                    continue
            if skip:
                logger.info("Skipping '%s'" % abs_path)
                continue

            logger.debug("Handling path '%s'" % abs_path)
            liche.utils.path_exists_barrier(abs_path)

            if os.path.isdir(abs_path):
                liche.utils.directory_exists_barrier(abs_path)

                if directory_callback is not None:
                    directory_callback(abs_path)

                self.__walk(abs_path,
                            file_callback,
                            directory_callback,
                            globs)
            elif os.path.isfile(abs_path):
                liche.utils.file_exists_barrier(abs_path)

                if file_callback is not None:
                    file_callback(abs_path)
            elif os.path.ismount(abs_path):
                logger.warning("Skipping '%s' (mount point)" %
                               abs_path)
            else:
                logger.warning("Skipping '%s' (not a file or directory)" %
                               abs_path)

        logger.debug("Completed handling directory '%s' (%d globs)" %
                     (current_dir, len(globs)))

    def run(self, file_callback = None, directory_callback = None):
        logger.debug("Start walking directory '%s'" % self.__root)
        liche.utils.directory_exists_barrier(self.__root)
        self.__walk(self.__root,
                    file_callback,
                    directory_callback,
                    list())
