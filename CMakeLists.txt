cmake_minimum_required (VERSION 3.1)
project (morphy)

set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} "${CMAKE_SOURCE_DIR}/cmakemodules")

# Find gsl, libedit, and ncl
FIND_PACKAGE(Libedit REQUIRED)
FIND_PACKAGE(Ncl REQUIRED)
FIND_PACKAGE(R)

# Crank up the warning levels
if(MSVC)
  # Force to always compile with W4
  if(CMAKE_CXX_FLAGS MATCHES "/W[0-4]")
    string(REGEX REPLACE "/W[0-4]" "/W4" CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS}")
  else()
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} /W4")
  endif()
else()
  # Update if necessary
  set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall -fPIC")
  set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -Wall -fPIC")
  set(CMAKE_CXX_FLAGS_DEBUG "${CMAKE_CXX_FLAGS_DEBUG} -DDEBUG")
  set(CMAKE_C_FLAGS_DEBUG "${CMAKE_C_FLAGS_DEBUG} -DDEBUG")
  if(COVERAGE)
      message(STATUS "coverage enabled")
      set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} --coverage")
      set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} --coverage")
  else()
      message(STATUS "coverage disabled")
  endif()
endif()

set(CMAKE_INSTALL_PREFIX "${CMAKE_SOURCE_DIR}/../install")
add_subdirectory (${CMAKE_SOURCE_DIR}/../pcl ${CMAKE_CURRENT_BINARY_DIR}/pcl)
add_subdirectory (${CMAKE_SOURCE_DIR}/../morphylib ${CMAKE_CURRENT_BINARY_DIR}/morphyLib)
add_subdirectory (${CMAKE_SOURCE_DIR}/../PAWM ${CMAKE_CURRENT_BINARY_DIR}/PAWM)
add_subdirectory (${CMAKE_SOURCE_DIR}/../nui ${CMAKE_CURRENT_BINARY_DIR}/nui)

