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
CMAKE_SOURCE_DIR = /root/zy_ros_paper/zy_ws/src

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /root/zy_ros_paper/zy_ws/build

# Utility rule file for clean_test_results_joint_trajectory_controller.

# Include the progress variables for this target.
include joint_trajectory_controller/CMakeFiles/clean_test_results_joint_trajectory_controller.dir/progress.make

joint_trajectory_controller/CMakeFiles/clean_test_results_joint_trajectory_controller:
	cd /root/zy_ros_paper/zy_ws/build/joint_trajectory_controller && /usr/bin/python2 /opt/ros/kinetic/share/catkin/cmake/test/remove_test_results.py /root/zy_ros_paper/zy_ws/build/test_results/joint_trajectory_controller

clean_test_results_joint_trajectory_controller: joint_trajectory_controller/CMakeFiles/clean_test_results_joint_trajectory_controller
clean_test_results_joint_trajectory_controller: joint_trajectory_controller/CMakeFiles/clean_test_results_joint_trajectory_controller.dir/build.make

.PHONY : clean_test_results_joint_trajectory_controller

# Rule to build all files generated by this target.
joint_trajectory_controller/CMakeFiles/clean_test_results_joint_trajectory_controller.dir/build: clean_test_results_joint_trajectory_controller

.PHONY : joint_trajectory_controller/CMakeFiles/clean_test_results_joint_trajectory_controller.dir/build

joint_trajectory_controller/CMakeFiles/clean_test_results_joint_trajectory_controller.dir/clean:
	cd /root/zy_ros_paper/zy_ws/build/joint_trajectory_controller && $(CMAKE_COMMAND) -P CMakeFiles/clean_test_results_joint_trajectory_controller.dir/cmake_clean.cmake
.PHONY : joint_trajectory_controller/CMakeFiles/clean_test_results_joint_trajectory_controller.dir/clean

joint_trajectory_controller/CMakeFiles/clean_test_results_joint_trajectory_controller.dir/depend:
	cd /root/zy_ros_paper/zy_ws/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /root/zy_ros_paper/zy_ws/src /root/zy_ros_paper/zy_ws/src/joint_trajectory_controller /root/zy_ros_paper/zy_ws/build /root/zy_ros_paper/zy_ws/build/joint_trajectory_controller /root/zy_ros_paper/zy_ws/build/joint_trajectory_controller/CMakeFiles/clean_test_results_joint_trajectory_controller.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : joint_trajectory_controller/CMakeFiles/clean_test_results_joint_trajectory_controller.dir/depend

