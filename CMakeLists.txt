cmake_minimum_required(VERSION 3.12)
project(matrix-multiplication VERSION 0.1.0 LANGUAGES C CXX)

include(CTest)
enable_testing()

if (MSVC)
    add_compile_options(/W4 /WX)
else()
    add_compile_options(-Wall -Wextra -pedantic -Werror)
endif()

add_executable(matrix-multiplication main.cpp)

set(CMAKE_CXX_FLAGS "-std=c++20")
set(CMAKE_CXX_STANDARD 20)
set(CPACK_PROJECT_NAME ${PROJECT_NAME})
set(CPACK_PROJECT_VERSION ${PROJECT_VERSION})
include(CPack)
