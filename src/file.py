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

from   liche.log      import logger

import liche.utils

class File(object):
    def __init__(self, path):
        liche.utils.file_exists_barrier(path)

        self.__path = path
        self.__lines = []

    def line_cleaner(self, line):
        return line

    def path(self):
        return self.__path

    def slurp(self, max_lines, line_cleaner = None):
        assert(max_lines is not None)
        assert(max_lines > 0)

        logger.debug("Slurping max %d lines from '%s'" %
                     (max_lines, self.__path))

        assert(max_lines >= 0)

        fh = open(self.__path, 'r')
        ln = 0
        while ln < max_lines:
            line = fh.readline()
            ln   = ln + 1
            if len(line) == 0:
                break
            if line_cleaner is not None:
                line = line_cleaner(line)
            self.__lines.append(line)
        fh.close()

        logger.debug("Slurped %d lines from '%s'" % (ln, self.__path))

    def tokens(self):
        return self.__lines

class TextFile(File):
    def __init__(self, path):
        super(TextFile, self).__init__(path)

class HashCommentedFile(File):
    def __init__(self, path):
        super(HashCommentedFile, self).__init__(path)

    def line_cleaner(self, line):
        m = re.match(r'^[ \t]*\#(.*)$')
        if len(m.groups()) == 1:
            return r.group(1)
        return line

class ShellFile(HashCommentedFile):
    def __init__(self, path):
        super(ShellFile, self).__init__(path)

class PerlFile(HashCommentedFile):
    def __init__(self, path):
        super(PerlFile, self).__init__(path)

class PythonFile(HashCommentedFile):
    def __init__(self, path):
        super(PythonFile, self).__init__(path)

class RubyFile(ShellFile):
    def __init__(self, path):
        super(RubyFile, self).__init__(path)

class LuaFile(ShellFile):
    def __init__(self, path):
        super(LuaFile, self).__init__(path)

class M4File(ShellFile):
    def __init__(self, path):
        super(M4File, self).__init__(path)

class FileFactory(object):
    def __init__(self):
        pass

    def get_by_extension(self, path):
        extension = os.path.splitext(path)[1][1:].lower()

        if extension is None or len(extension) <= 0:
            return None

        logger.debug("File '%s' extension is '%s'" % (path, extension))

        mappings = {
            "txt" : TextFile,
            "log" : TextFile,
            "lua" : LuaFile,
            "pl"  : PerlFile,
            "py"  : PythonFile,
            "rb"  : RubyFile,
            "sh"  : ShellFile,
            "m4"  : M4File,
            }

        if extension not in mappings:
            return None
        return mappings[extension](path)

    def get_by_mime(self, path):
        return None

    def get(self, path):
        f = self.get_by_extension(path)
        if f is not None:
            return f
        f = self.get_by_mime(path)
        if f is not None:
            return f
        return TextFile(path)
