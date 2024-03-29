
cmake_minimum_required(VERSION 3.8 FATAL_ERROR)

project(crispr-cuda LANGUAGES CXX CUDA)


find_package(CUDA REQUIRED)

set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
set(CMAKE_COLOR_MAKEFILE ON)
set(VERBOSE_BUILD ON)
set(CMAKE_CXX_STANDARD 11)
set(DEFAULT_BUILD_TYPE "Release")


set_property(GLOBAL PROPERTY USE_FOLDERS ON)

include(CTest)

add_executable(crispr-cuda
  main.cu
  common/fmt.hpp
  common/catch.hpp
  common/clara.hpp
  common/utils.hpp
)


# CUDA_SELECT_NVCC_ARCH_FLAGS(CUDA_ARCH_FLAGS Auto)

# Request that crispr-cuda be built with -std=c++11
# As this is a public compile feature anything that links to particles
# will also build with -std=c++11
target_compile_features(crispr-cuda PUBLIC cxx_std_11)

# We need to explicitly state that we need all CUDA files in the particle
# library to be built with -dc as the member functions could be called by
# other libraries and executables
set_target_properties( crispr-cuda PROPERTIES
                       # CUDA_SEPARABLE_COMPILATION ON
                       CUDA_RESOLVE_DEVICE_SYMBOLS ON
                      )

target_link_libraries(crispr-cuda ${CUDA_LIBRARIES})


include_directories(crispr-cuda
  ${PROJECT_SOURCE_DIR}/src
  ${CUDA_INCLUDE_DIRS}
)

set(CMAKE_CUDA_FLAGS "${CMAKE_CUDA_FLAGS} -O3 -lineinfo -g -use_fast_math")

if(APPLE)
  # We need to add the default path to the driver (libcuda.dylib) as an rpath,
  # so that the static cuda runtime can find it at runtime.
  set_property(TARGET crispr-cuda PROPERTY BUILD_RPATH ${CMAKE_CUDA_IMPLICIT_LINK_DIRECTORIES})
endif()
