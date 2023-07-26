cmake_minimum_required(VERSION 3.15)
project("libzt-conan-test-package" CXX)

find_package(libzt CONFIG REQUIRED)

add_executable(${PROJECT_NAME} src/test.cpp)
target_link_libraries(${PROJECT_NAME} libzt::libzt)
