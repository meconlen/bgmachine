AC_PREREQ(2.61)
AC_INIT([bgmachine], [0.1], [mike@conlen.org])
AC_CONFIG_SRCDIR([src/test.cpp])
AC_CONFIG_HEADERS([config.h])
AC_CANONICAL_HOST
AM_INIT_AUTOMAKE([-Wall -Werror])
AC_PROG_CC
AC_PROG_CXX
AC_PROG_CPP
#AC_PROG_AR
AC_HEADER_STDC

CXXFLAGS="$CXXFLAGS --std=c++11 -Wall -Werror"
LDFLAGS="$LDFLAGS"

XXFLAGS="$CXXFLAGS --std=c++11 -Wall -Werror"
LDFLAGS="$LDFLAGS"

case $host_os in
   darwin* )
      # I include this to find MacPorts installed libraries
      CFLAGS="$CFLAGS -I/opt/local/include"
      CXXFLAGS="$CXXFLAGS -I/opt/local/include"
      CPPFLAGS="$CPPFLAGS -I/opt/local/include"
      LDFLAGS="$LDFLAGS -L/opt/local/lib"
   ;;
   linux*)
      # Do something specific for Linux
   ;;
   *BSD*)
      # Do something specific for BSD
   ;;
   *)
      #Default Case
   ;;
esac



AC_CHECK_HEADERS([stdio.h])
AC_CHECK_HEADERS([stdlib.h])
AC_CHECK_HEADERS([malloc.h])
AC_CHECK_HEADERS([sys/malloc.h])
AC_CHECK_HEADERS([malloc/malloc.h])
AC_FUNC_MALLOC
AC_FUNC_MMAP
AC_CHECK_FUNCS([fstat])
AC_CONFIG_FILES([Makefile
	src/Makefile])
AC_OUTPUT
