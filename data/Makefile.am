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

licenses_data =					\
	all_rights_reserved-f.txt		\
	apache-1.0.txt				\
	apache-1.1.txt				\
	apache-2.0-l.txt			\
	apache-2.0-s.txt			\
	artistic.txt				\
	bsd-sun.txt				\
	bsd.txt					\
	cddl-1.0.txt				\
	cpl-1.0.txt				\
	dual-bsd-gpl-k.txt			\
	dual-mpl-gpl-k.txt			\
	eclipse-1.0.txt				\
	gpl-2.0-LK-+-k.txt			\
	gpl-2.0-l.txt				\
	gpl-2.0-m-classpath.txt			\
	gpl-2.0-only-s.txt			\
	gpl-2.0-s.txt				\
	ipl-1.0.txt				\
	lgpl-2.1-l.txt				\
	lgpl-2.1-s.txt				\
	mit.txt					\
	module_license-f.txt			\
	mpl-1.0-l.txt				\
	mpl-1.0-s.txt				\
	mpl-1.1-l.txt				\
	mpl-1.1-s.txt				\
	ms-cl.txt				\
	ms-lcl.txt				\
	ms-pl.txt				\
	ms-rl.txt				\
	nokos-1.0a-l.txt			\
	nokos-1.0a-s.txt			\
	not_for_commercial_use-f.txt		\
	osl-3.0.txt				\
	patented-f.txt				\
	patent_pending-f.txt			\
	perlartistic.txt			\
	php-3.0-l.txt				\
	php-3.0-s.txt				\
	shareware-f.txt				\
	sleepycat-bdb.txt			\
	sleepycat.txt

licenses_meta =					\
	all_rights_reserved-f.meta		\
	apache-1.0.meta				\
	apache-1.1.meta				\
	apache-2.0-l.meta			\
	apache-2.0-s.meta			\
	artistic.meta				\
	bsd.meta				\
	bsd-sun.meta				\
	cddl-1.0.meta				\
	cpl-1.0.meta				\
	dual-bsd-gpl-k.meta			\
	dual-mpl-gpl-k.meta			\
	eclipse-1.0.meta			\
	gpl-2.0-LK-+-k.meta			\
	gpl-2.0-l.meta				\
	gpl-2.0-m-classpath.meta		\
	gpl-2.0-only-s.meta			\
	gpl-2.0-s.meta				\
	ipl-1.0.meta				\
	lgpl-2.1-l.meta				\
	lgpl-2.1-s.meta				\
	mit.meta				\
	module_license-f.meta			\
	mpl-1.0-l.meta				\
	mpl-1.0-s.meta				\
	mpl-1.1-l.meta				\
	mpl-1.1-s.meta				\
	ms-cl.meta				\
	ms-lcl.meta				\
	ms-pl.meta				\
	ms-rl.meta				\
	nokos-1.0a-l.meta			\
	nokos-1.0a-s.meta			\
	not_for_commercial_use-f.meta		\
	osl-3.0.meta				\
	patented-f.meta				\
	patent_pending-f.meta			\
	perlartistic.meta			\
	php-3.0-l.meta				\
	php-3.0-s.meta				\
	shareware-f.meta			\
	sleepycat-bdb.meta			\
	sleepycat.meta

licenses.txt: Makefile
	rm -f $@ $@.tmp
	for i in $(licenses_meta) ; do \
	  echo "$$i" | @SED@ 's,\.meta,,' >> $@.tmp ; \
	done
	chmod -x $@.tmp
	chmod a-w $@.tmp
	mv $@.tmp $@

DISTCLEANFILES = licenses.txt

pkgdata_DATA =					\
	licenses.txt

dist_pkgdata_DATA =				\
	$(licenses_meta)			\
	$(licenses_data)
