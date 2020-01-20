find_package(PkgConfig REQUIRED)
pkg_check_modules(LIBEDIT REQUIRED libedit)
message(STATUS "libedit required libraries: ${LIBEDIT_LIBRARIES}")

set(PATH_LIB_EDIT ${LIBEDIT_LIBRARIES})
