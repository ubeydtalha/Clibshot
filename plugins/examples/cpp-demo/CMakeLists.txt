cmake_minimum_required(VERSION 3.15)
project(cpp_demo_plugin)

# Set C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Find Python
find_package(Python3 COMPONENTS Interpreter Development REQUIRED)

# Find pybind11
find_package(pybind11 CONFIG REQUIRED)

# Create the Python module
pybind11_add_module(cpp_demo_plugin 
    src/plugin.cpp
)

# Set target properties
target_compile_definitions(cpp_demo_plugin PRIVATE VERSION_INFO="1.0.0")

# Install target
install(TARGETS cpp_demo_plugin LIBRARY DESTINATION .)
