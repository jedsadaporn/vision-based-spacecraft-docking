cmake_minimum_required(VERSION 3.8)
project(docking_gazebo)

# Find ROS 2 / ament
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(gazebo_ros REQUIRED)
# This is Gazebo library/dependency not ROS 2 ament dependency
find_package(gazebo REQUIRED)

# Output is libspacecraft_cmd_vel_plugin.so
add_library(spacecraft_cmd_vel_plugin SHARED
    plugins/spacecraft_cmd_vel_plugin.cpp
)

# Link spacecraft_cmd_vel_plugin with Gazebo libraries
target_link_libraries(
    spacecraft_cmd_vel_plugin
    ${GAZEBO_LIBRARIES}
)

# What is Ros2 dependencies this library link to
ament_target_dependencies(
    spacecraft_cmd_vel_plugin
    rclcpp
    geometry_msgs
    gazebo_ros
)

install(TARGETS
  spacecraft_cmd_vel_plugin
  DESTINATION lib
)

install(
  DIRECTORY models worlds launch
  DESTINATION share/${PROJECT_NAME}
)

ament_package()