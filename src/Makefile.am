##
## Input file for automake
##
## Copyright (C) 2008, 2009 Francesco Salvestrini
##
## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License along
## with this program; if not, write to the Free Software Foundation, Inc.,
## 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
##

AUTOMAKE_OPTIONS = subdir-objects

SUBDIRS    =
EXTRA_DIST =
CLEANFILES =

do_subst = @SED@ \
	-e 's|@bindir[@]|$(bindir)|g' \
	-e 's|@pkgdatadir[@]|$(pkgdatadir)|g' \
	-e 's|@pythondir[@]|$(pythondir)|g' \
	-e 's|@pkgpythondir[@]|$(pkgpythondir)|g' \
	-e 's|@localstatedir[@]|$(localstatedir)|g' \
	-e 's|@sysconfdir[@]|$(sysconfdir)|g' \
	-e 's|@SHELL[@]|$(SHELL)|g' \
	-e 's|@PYTHON[@]|$(PYTHON)|g' \
	-e 's|@PACKAGE_NAME[@]|$(PACKAGE_NAME)|g' \
	-e 's|@PACKAGE_VERSION[@]|$(PACKAGE_VERSION)|g' \
	-e 's|@PACKAGE_BUGREPORT[@]|$(PACKAGE_BUGREPORT)|g' \
	-e 's|@prefix[@]|$(prefix)|g'

settings.py: settings.py.in Makefile
	$(do_subst) < $(srcdir)/settings.py.in > settings.py

#settings.py: Makefile
#	rm -f $@ $@.tmp
#	srcdir=''; \
#	  test -f ./$@.in || srcdir=$(srcdir)/; \
#	  $(edit) $${srcdir}$@.in >$@.tmp
#	chmod a-w $@.tmp
#	mv $@.tmp $@
#
#settings.py: $(srcdir)/settings.py.in

CLEANFILES += settings.py
EXTRA_DIST += settings.py.in

liche: liche.in Makefile
	$(do_subst) < $(srcdir)/liche.in > liche
	chmod +x liche

#liche: Makefile
#	rm -f $@ $@.tmp
#	srcdir=''; \
#	  test -f ./$@.in || srcdir=$(srcdir)/; \
#	  $(edit) $${srcdir}$@.in >$@.tmp
#	chmod +x $@.tmp
#	chmod a-w $@.tmp
#	mv $@.tmp $@
#
#liche: $(srcdir)/liche.in

CLEANFILES += liche
EXTRA_DIST += liche.in

bin_SCRIPTS = liche

pkgpython_PYTHON =				\
	__init__.py				\
	main.py					\
	directory.py				\
	stream.py				\
	file.py					\
	license.py				\
	job.py					\
	log.py					\
	utils.py				\
	settings.py
