cmake_minimum_required(VERSION 3.1)
project("libzt-conan-test-package" CXX)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

add_executable(${PROJECT_NAME} test.cpp)
target_link_libraries(${PROJECT_NAME} ${CONAN_LIBS})
