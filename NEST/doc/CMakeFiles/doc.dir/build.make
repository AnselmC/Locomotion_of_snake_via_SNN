# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.5

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:


#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:


# Remove some rules from gmake that .SUFFIXES does not remove.
SUFFIXES =

.SUFFIXES: .hpux_make_needs_suffix_list


# Suppress display of executed commands.
$(VERBOSE).SILENT:


# A target that is always out of date.
cmake_force:

.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/bin/cmake

# The command to remove a file.
RM = /usr/bin/cmake -E remove -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/christoph/nest-simulator-2.14.0-src

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/christoph/Documents/bachelor-thesis/Locomotion_of_snake_via_SNN

# Utility rule file for doc.

# Include the progress variables for this target.
include doc/CMakeFiles/doc.dir/progress.make

doc/CMakeFiles/doc:
	cd /home/christoph/Documents/bachelor-thesis/Locomotion_of_snake_via_SNN/doc && /usr/bin/cmake -E echo Doxygen\ is\ not\ found\ on\ your\ system.\ Cannot\ build\ documentation.

doc: doc/CMakeFiles/doc
doc: doc/CMakeFiles/doc.dir/build.make

.PHONY : doc

# Rule to build all files generated by this target.
doc/CMakeFiles/doc.dir/build: doc

.PHONY : doc/CMakeFiles/doc.dir/build

doc/CMakeFiles/doc.dir/clean:
	cd /home/christoph/Documents/bachelor-thesis/Locomotion_of_snake_via_SNN/doc && $(CMAKE_COMMAND) -P CMakeFiles/doc.dir/cmake_clean.cmake
.PHONY : doc/CMakeFiles/doc.dir/clean

doc/CMakeFiles/doc.dir/depend:
	cd /home/christoph/Documents/bachelor-thesis/Locomotion_of_snake_via_SNN && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/christoph/nest-simulator-2.14.0-src /home/christoph/nest-simulator-2.14.0-src/doc /home/christoph/Documents/bachelor-thesis/Locomotion_of_snake_via_SNN /home/christoph/Documents/bachelor-thesis/Locomotion_of_snake_via_SNN/doc /home/christoph/Documents/bachelor-thesis/Locomotion_of_snake_via_SNN/doc/CMakeFiles/doc.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : doc/CMakeFiles/doc.dir/depend

