set(NCL_INC_FILE "ncl/ncl.h")
set(NCL_LIB_FILE "ncl/${CMAKE_STATIC_LIBRARY_PREFIX}ncl${CMAKE_STATIC_LIBRARY_SUFFIX}")

find_path(PATH_INC_NCL NAMES ${NCL_INC_FILE} PATHS "${CMAKE_SOURCE_DIR}/../install/include" env PATH_INC_NCL)

macro(nclerr filename envvar)
    message(FATAL_ERROR
    "Unable to locate Nexus Class Library: '${filename}' "
    "Either install NCL to a standard location or set the "
    "env variable '${envvar}' to the location of '${filename}'")
endmacro()

if( NOT PATH_INC_NCL )
    nclerr(${NCL_INC_FILE} "PATH_INC_NCL")
endif()

find_library(PATH_LIB_NCL NAMES ${NCL_LIB_FILE} PATHS "${CMAKE_SOURCE_DIR}/../install/lib" env PATH_LIB_NCL)

if( NOT PATH_LIB_NCL )
    nclerr(${NCL_LIB_FILE} "PATH_LIB_NCL")
endif()

message(STATUS "PATH_INC_NCL = \"${PATH_INC_NCL}\"")
message(STATUS "PATH_LIB_NCL = \"${PATH_LIB_NCL}\"")
