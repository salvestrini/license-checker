# Process this file with autoconf to produce a configure script.

#
# configure.ac for liche
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

AC_INIT([LIchense CHEcker],
        m4_esyscmd([build-aux/git-version-gen .tarball-version]),
        [salvestrini@gmail.com],
        [liche],
        [http://github.com/salvestrini/liche])

# Check for a recent version of autoconf
AC_PREREQ([2.67])

# Place/find all autotools related files in the following directories
AC_CONFIG_AUX_DIR([build-aux])
AC_CONFIG_MACRO_DIR([m4])
AC_CONFIG_SRCDIR([src/liche.in])

#
# For automake options (AM_INIT_AUTOMAKE options) see Makefile.am
# file, AUTOMAKE_OPTIONS variable
#
AM_INIT_AUTOMAKE([1.11.1 foreign std-options -Wall color-tests])

#
# Build related programs
#
AC_PROG_INSTALL
AC_PROG_MAKE_SET
AC_PROG_LN_S
AC_PROG_GREP
AC_PROG_SED

AM_PATH_PYTHON([2.7.0],[],[
  AC_MSG_ERROR([Python interpreter >= 2.7.0 is missing])
])

AX_PYTHON_MODULE([sys],       [ AC_MSG_ERROR([Cannot find required module]) ])
AX_PYTHON_MODULE([argparse],  [ AC_MSG_ERROR([Cannot find required module]) ])
AX_PYTHON_MODULE([os],        [ AC_MSG_ERROR([Cannot find required module]) ])
AX_PYTHON_MODULE([fnmatch],   [ AC_MSG_ERROR([Cannot find required module]) ])
AX_PYTHON_MODULE([re],        [ AC_MSG_ERROR([Cannot find required module]) ])
AX_PYTHON_MODULE([traceback], [ AC_MSG_ERROR([Cannot find required module]) ])
AX_PYTHON_MODULE([string],    [ AC_MSG_ERROR([Cannot find required module]) ])

AC_CONFIG_FILES([
	Makefile
	data/Makefile
	src/Makefile
])

AC_OUTPUT
