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

program_name    = 'liche'
ignore_filename = "." + program_name + "ignore"

import sys

try:
    import argparse
    import os
    import re
    import traceback
except Exception, e:
    print("%s: Cannot import required system module(s) (%s)" %
          (program_name, str(e)))
    sys.exit(1)

try:
    import liche.settings
    import liche.log

    liche.log.setup(program_name)
    from   liche.log      import logger

    import liche.job
    import liche.license
except Exception, e:
    print("%s: Cannot import required package module(s) (%s)" %
          (program_name, str(e)))
    sys.exit(1)

program_bugreport = liche.settings.package_bugreport

def main(argv):
    parser = argparse.ArgumentParser(description =
                                     "A source-file LIcense CHEcker.",
                                     epilog      = "Report bugs to " +
                                     "<" + program_bugreport + ">",
                                     add_help    = True,
                                     prog        = program_name)

    #parser.add_argument('-V', '--version',
    #                    action = 'version',
    #                    version = '%(prog)s ' +
    #                    liche.settings.package_version,
    #                    help    = "print version number, then exit")
    parser.add_argument('-V', '--version',
                        action = 'store_true',
                        dest   = 'show_version',
                        help    = "print version number, then exit")
    parser.add_argument('-v', '--verbose',
                        action = 'store_true',
                        dest   = 'want_verbose',
                        help   = 'produce verbose output')
    parser.add_argument('-d', '--debug',
                        action = 'store_true',
                        dest   = 'want_debug',
                        help   = 'produce debugging output')

    parser.add_argument('--quiet',
                        action = 'store_true',
                        dest   = 'quiet',
                        help   = 'perform actions quietly')
    parser.add_argument('--dry-run',
                        action = 'store_true',
                        dest   = 'dry_run',
                        help   = 'do not perform checks')
    parser.add_argument('--licenses',
                        action = 'store_true',
                        dest   = 'show_licenses',
                        help   = 'show licenses')
    #parser.add_argument('--exclude',
    #                    nargs   = 1,
    #                    action  = 'append',
    #                    dest    = 'exclude',
    #                    metavar = 'PATH',
    #                    help    = 'exclude paths, given as PATTERN')

    parser.add_argument('DIRECTORY',
                        nargs   = '*',
                        action  = 'store',
                        default = ".",
                        help    = 'input directory')

    args = parser.parse_args()
    #print args.__dict__

    if args.show_version:
        print("%s (%s) %s" %
              (program_name,
               liche.settings.package_name,
               liche.settings.package_version))
        return 0

    if not args.want_debug:
        liche.log.debug_off()

    if not args.want_verbose:
        liche.log.info_off()

    logger.debug("%s %s" % (program_name, liche.settings.package_version))

    licenses_filename = os.path.join(liche.settings.pkgdatadir, "licenses.txt")
    licenses_factory  = liche.license.LicensesFactory(licenses_filename)

    logger.debug("License factory contains %d licenses: %s" %
                 (len(licenses_factory.licenses()),
                  map(str, licenses_factory.licenses())))

    if args.show_licenses:
        for l in licenses_factory.licenses():
            #print("%s: %s" % (str(l),  map(str, l.compatibles()).join(' ')))
            print("%s" % str(l))
        return 0

    tags = set()
    licenses = licenses_factory.licenses()
    for l in licenses:
        tags = set.union(tags, l.tags())

    logger.debug("There are %d known tags: %s" % (len(tags), map(str, tags)))

    paths = set()
    for path in args.DIRECTORY:
        logger.debug("Adding path '%s'" % path)
        paths.add(os.path.abspath(path))
    logger.debug("Paths are: '%s'" % str(paths))

    jobs = set()
    for path in paths:
        jobs.add(liche.job.Job(path, licenses, ignore_filename))
    logger.debug("Jobs are: '%s'" % str(jobs))

    if args.quiet:
        s = None
    else:
        s = sys.stdout

    rets = map(lambda obj: obj.run(stream = s,
                                   dry    = args.dry_run), jobs)
    logger.debug("%d jobs completed" % len(rets))

    retval = 0
    if False in rets:
        logger.warning("Got problems")
        retval = 1

    logger.debug("Everything seems ok")

    return retval

if __name__ == "__main__":
    retval = 1
    try:
        retval = main(sys.argv[1:])
    except KeyboardInterrupt, e:
        logger.info("Bye bye ...\n")
        retval = 0
    except AssertionError, e:
        print("%s: Assertion error" % program_name)
        if len(str(e)) != 0:
            print("%s: Value is '%s'" % (program_name, str(e)))
        traceback.print_tb(sys.exc_info()[2], file = sys.stdout)
        print("Please report to <" + program_bugreport + ">")
    except Exception, e:
        print("%s: %s" % (program_name, str(e)))
    sys.exit(retval)
sys.exit(0)
