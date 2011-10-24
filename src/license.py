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
import re
import string

from   liche.log import logger

import liche.utils

class LicenseMeta(object):
    def __parse(self, filename):
        logger.debug("Parsing license meta from '%s'" % filename)

        liche.utils.file_exists_barrier(filename)

        ln = 0
        fh = open(filename, 'r')
        while True:
            line = fh.readline()
            ln   = ln + 1
            if len(line) == 0:
                break
            line = line.strip()

            #logger.debug("Handling line '%s'" % line)

            if (re.match(r'^#.*$', line) or re.match(r'^$', line)):
                #logger.debug("Skipping comment/empty line")
                continue

            r = re.match(r'^isCompatible[ \t]*:[ \t]*(.*)$', line)
            if r is not None and len(r.groups()) == 1:
                #logger.debug("Got compatibility list '%s'" % r.group(1))
                licenses = r.group(1).split()
                licenses = map(lambda obj: obj.strip(), licenses)
                self.__compatibles = self.__compatibles.union(set(licenses))
                continue

            r = re.match(r'^tags[ \t]*:[ \t]*(.*)$', line)
            if r is not None and len(r.groups()) == 1:
                #logger.debug("Got tag list '%s'" % r.group(1))
                tags = r.group(1).split()
                tags = map(lambda obj: obj.strip(), tags)
                self.__tags = self.__tags.union(set(tags))

                logger.debug("Checking tags")
                for tag in tags:
                    if not re.match(r'<[a-zA-Z0-9_\-]+>', tag):
                        raise Exception("Tag '%s' is invalid (%s:%d)" %
                                        (tag, filename, ln))
                continue

            raise Exception("Malformed line (%s:%d)" % (filename, ln))

        fh.close()

    def __init__(self, filename):
        self.__tags        = set()
        self.__compatibles = set()

        self.__parse(filename)

        logger.debug("License uses tags:          %s" %
                     map(str, self.__tags))
        logger.debug("License is compatible with: %s" %
                     map(str, self.__compatibles))

    def tags(self):
        return self.__tags

    def compatibles(self):
        return self.__compatibles

class LicenseToken(object):
    def __init__(self, value):
        self.__value = value.strip()

    def __str__(self):
        return self.__value

class LicenseTag(LicenseToken):
    pass

class LicenseText(object):
    def __parse(self, filename, tags):
        logger.debug("Parsing license text from '%s'" % filename)

        liche.utils.file_exists_barrier(filename)

        punct_mappings = {
            "`" : " ` ",
            "'" : " ' ",
            ";" : " ; ",
            "." : " . ",
            "," : " , ",
            ":" : " : ",
            "[" : " [ ",
            "]" : " ] ",
            "(" : " ( ",
            ")" : " ) ",
            "{" : " } ",
            "}" : " } ",
            "<" : " < ",
            ">" : " > ",
            "*" : " * ",
            "/" : " / ",
            "-" : " - ",
            }

        ln = 0
        fh = open(filename, 'r')
        while True:
            line = fh.readline()
            ln   = ln + 1
            if len(line) == 0:
                break

            words = line.split()
            #logger.debug("Words in line: %s" % str(words))

            tmp = list()
            for word in words:
                if word in tags:
                    #logger.debug("Word '%s' is a tag" % str(word))
                    tmp.append(LicenseTag(word))
                else:
                    #logger.debug("Word '%s' is not a tag" % str(word))
                    tokens = liche.utils.string_replace_all(word,
                                                            punct_mappings)
                    #logger.debug("Re-phrased word is '%s'" % str(word))
                    for token in tokens.split():
                        tmp.append(LicenseToken(token))
            self.__text = self.__text + tmp
        fh.close()

        self.__lines = ln

    def __init__(self, filename, tags):
        self.__text = list()
        self.__lines = 0

        self.__parse(filename, tags)

        logger.debug("License text is %d lines long" % self.__lines)

    def lines(self):
        return self.__lines

    def match(self, fileobject):
        logger.debug("Looking for file '%s' confidence against license '%s'" %
                     (fileobject.path(), self.name()))

        tl = self.__text
        tf = fileobject.tokens()

        logger.debug("Tokens: file %d, license %d" % (len(tf), len(tl)))

        confidence = 0

        if len(tf) < len(tl):
            logger.debug("File is shorter than license (%d < %d))" %
                         (len(tf), len(tl)))
            return confidence

        i          = 0
        hits       = 0
        misses     = 0

        for i in range(0, len(tl)):
            logger.debug("tf[%d] = '%s', tl[%d] = '%s'" % (i, tf[i], i, tl[i]))
            if tf[i] == tl[i]:
                hits = hits + 1
            else:
                misses = misses + 1

        confidence = hits/(misses + hits)

        logger.debug("Hits %d / Missees %d -> Confidence %f" %
                     (hits, misses, confidence))

        return confidence

class License(LicenseMeta, LicenseText):
    def __init__(self, name, basepath):
        self.__name = name

        logger.debug("License '%s' base path is '%s'" %
                     (self.__name, basepath))

        meta_filename = basepath + os.path.extsep + "meta"
        text_filename = basepath + os.path.extsep + "txt"

        LicenseMeta.__init__(self, meta_filename)
        LicenseText.__init__(self, text_filename, LicenseMeta.tags(self))

    def __str__(self):
        return self.__name

    def name(self):
        return self.__name

class LicensesFactory(object):
    def __cross_check_barrier(self):
        logger.debug("Cross-checking all licenses")

        assert(self.__licenses is not None)

        names = set(map(lambda obj: obj.name(), self.__licenses))
        logger.debug("Known licenses: %s" % names)

        for l in self.__licenses:
            #logger.debug("compatibles for '%s': %s" % (l, l.compatibles()))

            missing = l.compatibles().difference(names)
            if (len(missing) > 0):
                logger.debug("Got problems with '%s' license" % l)
                raise Exception("There are %d missing license(s) referenced "
                                "by '%s' (%s)" %
                                (len(missing),
                                 l,
                                 string.join(list(missing), ', ')))

    def __init__(self, filename):
        logger.debug("Reading licenses from '%s'" % filename)

        liche.utils.file_exists_barrier(filename)

        names = set()
        fh    = open(filename, 'r')
        c     = 0
        while True:
            line = fh.readline()
            if len(line) == 0:
                break
            c = c + 1

            line = line.strip()

            if (re.match(r'^#.*$', line) or re.match(r'^$', line)):
                logger.debug("Skipping comment/empty line")
                continue

            tmp = re.match(r'^[ \t]*([0-9A-Za-z_\-\+\.]+)[ \t]*$', line)
            if tmp is not None and len(tmp.groups()) == 1:
                names.add(tmp.group(1))
                continue

            raise Exception("Malformed line %d in licenses file '%s'" %
                            (c, filename))
        fh.close()

        logger.debug("Read %d lines, got %d licenses: '%s'" %
                     (c, len(names), names))

        self.__licenses = set()
        directory       = os.path.dirname(filename)
        for name in names:
            basepath = os.path.join(directory, name)
            self.__licenses.add(License(name, basepath))

        self.__cross_check_barrier()

        logger.debug("Created %d licenses" % len(self.__licenses))

    def licenses(self):
        return self.__licenses
