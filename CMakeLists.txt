cmake_minimum_required(VERSION 3.12)
project(matrix-multiplication VERSION 0.1.0 LANGUAGES C CXX)

include(CTest)
enable_testing()

# Znajdź pakiet MPI
find_package(MPI REQUIRED)

# Ustawienia kompilatora
if (MSVC)
    add_compile_options(/W4 /WX)
else()
    add_compile_options(-Wall -Wextra -pedantic -Werror)
endif()

# Ustawienia standardu C++
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# Dodaj executable
add_executable(matrix-multiplication main.cpp)

# Połącz z MPI
target_link_libraries(matrix-multiplication PRIVATE MPI::MPI_CXX)

# Dodaj ścieżki include dla MPI
target_include_directories(matrix-multiplication PRIVATE ${MPI_CXX_INCLUDE_PATH})

# Dodaj flagi kompilacji dla MPI
if(MPI_CXX_COMPILE_FLAGS)
    set_target_properties(matrix-multiplication PROPERTIES
        COMPILE_FLAGS "${MPI_CXX_COMPILE_FLAGS}")
endif()

# Dodaj flagi linkowania dla MPI
if(MPI_CXX_LINK_FLAGS)
    set_target_properties(matrix-multiplication PROPERTIES
        LINK_FLAGS "${MPI_CXX_LINK_FLAGS}")
endif()

# Konfiguracja pakietu
set(CPACK_PROJECT_NAME ${PROJECT_NAME})
set(CPACK_PROJECT_VERSION ${PROJECT_VERSION})
include(CPack)