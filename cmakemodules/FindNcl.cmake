set(NCL_INC_FILE "ncl/ncl.h")
set(NCL_LIB_FILE "ncl/${CMAKE_STATIC_LIBRARY_PREFIX}ncl${CMAKE_STATIC_LIBRARY_SUFFIX}")

find_path(PATH_INC_NCL NAMES ${NCL_INC_FILE} PATHS "${CMAKE_SOURCE_DIR}/../install/include" env PATH_INC_NCL)

macro(nclerr filename envvar)
    message(FATAL_ERROR
    "Unable to locate Nexus Class Library: '${filename}' "
    "Either install NCL to a standard location or set the "
    "env variable '${envvar}' to the location of '${filename}'")
endmacro()

# Attempt to find path to the NCL header file on an ad hoc ncl build in the main project directory
if( NOT PATH_INC_NCL )
    find_path(PATH_INC_NCL NAMES ${NCL_INC_FILE} PATHS "${CMAKE_SOURCE_DIR}/../ncl" env PATH_INC_NCL)
endif()

if( NOT PATH_INC_NCL )
    nclerr(${NCL_INC_FILE} "PATH_INC_NCL")
endif()

find_library(PATH_LIB_NCL NAMES ${NCL_LIB_FILE} PATHS "${CMAKE_SOURCE_DIR}/../install/lib" env PATH_LIB_NCL)

# Attempt to see if it has been built in the project directory at another location
# This could address the problem with Windows builds as they don't have unix-like directories
if( NOT PATH_LIB_NCL )
    set(NCL_LIB_FILE "ncl/build/ncl${CMAKE_STATIC_LIBRARY_PREFIX}ncl${CMAKE_STATIC_LIBRARY_SUFFIX}")
    find_library(PATH_LIB_NCL NAMES ${NCL_LIB_FILE} PATHS "${CMAKE_SOURCE_DIR}/../ncl/build/" env PATH_LIB_NCL)
endif()

if( NOT PATH_LIB_NCL )
    nclerr(${NCL_LIB_FILE} "PATH_LIB_NCL")
endif()

message(STATUS "PATH_INC_NCL = \"${PATH_INC_NCL}\"")
message(STATUS "PATH_LIB_NCL = \"${PATH_LIB_NCL}\"")
