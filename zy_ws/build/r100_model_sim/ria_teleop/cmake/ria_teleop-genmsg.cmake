# generated from genmsg/cmake/pkg-genmsg.cmake.em

message(STATUS "ria_teleop: 1 messages, 1 services")

set(MSG_I_FLAGS "-Iria_teleop:/root/zy_ros_paper/zy_ws/src/r100_model_sim/ria_teleop/msg;-Istd_msgs:/opt/ros/kinetic/share/std_msgs/cmake/../msg")

# Find all generators
find_package(gencpp REQUIRED)
find_package(geneus REQUIRED)
find_package(genlisp REQUIRED)
find_package(gennodejs REQUIRED)
find_package(genpy REQUIRED)

add_custom_target(ria_teleop_generate_messages ALL)

# verify that message/service dependencies have not changed since configure



get_filename_component(_filename "/root/zy_ros_paper/zy_ws/src/r100_model_sim/ria_teleop/msg/Num.msg" NAME_WE)
add_custom_target(_ria_teleop_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "ria_teleop" "/root/zy_ros_paper/zy_ws/src/r100_model_sim/ria_teleop/msg/Num.msg" ""
)

get_filename_component(_filename "/root/zy_ros_paper/zy_ws/src/r100_model_sim/ria_teleop/srv/AddTwoInts.srv" NAME_WE)
add_custom_target(_ria_teleop_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "ria_teleop" "/root/zy_ros_paper/zy_ws/src/r100_model_sim/ria_teleop/srv/AddTwoInts.srv" ""
)

#
#  langs = gencpp;geneus;genlisp;gennodejs;genpy
#

### Section generating for lang: gencpp
### Generating Messages
_generate_msg_cpp(ria_teleop
  "/root/zy_ros_paper/zy_ws/src/r100_model_sim/ria_teleop/msg/Num.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/ria_teleop
)

### Generating Services
_generate_srv_cpp(ria_teleop
  "/root/zy_ros_paper/zy_ws/src/r100_model_sim/ria_teleop/srv/AddTwoInts.srv"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/ria_teleop
)

### Generating Module File
_generate_module_cpp(ria_teleop
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/ria_teleop
  "${ALL_GEN_OUTPUT_FILES_cpp}"
)

add_custom_target(ria_teleop_generate_messages_cpp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_cpp}
)
add_dependencies(ria_teleop_generate_messages ria_teleop_generate_messages_cpp)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/root/zy_ros_paper/zy_ws/src/r100_model_sim/ria_teleop/msg/Num.msg" NAME_WE)
add_dependencies(ria_teleop_generate_messages_cpp _ria_teleop_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/root/zy_ros_paper/zy_ws/src/r100_model_sim/ria_teleop/srv/AddTwoInts.srv" NAME_WE)
add_dependencies(ria_teleop_generate_messages_cpp _ria_teleop_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(ria_teleop_gencpp)
add_dependencies(ria_teleop_gencpp ria_teleop_generate_messages_cpp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS ria_teleop_generate_messages_cpp)

### Section generating for lang: geneus
### Generating Messages
_generate_msg_eus(ria_teleop
  "/root/zy_ros_paper/zy_ws/src/r100_model_sim/ria_teleop/msg/Num.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/ria_teleop
)

### Generating Services
_generate_srv_eus(ria_teleop
  "/root/zy_ros_paper/zy_ws/src/r100_model_sim/ria_teleop/srv/AddTwoInts.srv"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/ria_teleop
)

### Generating Module File
_generate_module_eus(ria_teleop
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/ria_teleop
  "${ALL_GEN_OUTPUT_FILES_eus}"
)

add_custom_target(ria_teleop_generate_messages_eus
  DEPENDS ${ALL_GEN_OUTPUT_FILES_eus}
)
add_dependencies(ria_teleop_generate_messages ria_teleop_generate_messages_eus)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/root/zy_ros_paper/zy_ws/src/r100_model_sim/ria_teleop/msg/Num.msg" NAME_WE)
add_dependencies(ria_teleop_generate_messages_eus _ria_teleop_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/root/zy_ros_paper/zy_ws/src/r100_model_sim/ria_teleop/srv/AddTwoInts.srv" NAME_WE)
add_dependencies(ria_teleop_generate_messages_eus _ria_teleop_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(ria_teleop_geneus)
add_dependencies(ria_teleop_geneus ria_teleop_generate_messages_eus)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS ria_teleop_generate_messages_eus)

### Section generating for lang: genlisp
### Generating Messages
_generate_msg_lisp(ria_teleop
  "/root/zy_ros_paper/zy_ws/src/r100_model_sim/ria_teleop/msg/Num.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/ria_teleop
)

### Generating Services
_generate_srv_lisp(ria_teleop
  "/root/zy_ros_paper/zy_ws/src/r100_model_sim/ria_teleop/srv/AddTwoInts.srv"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/ria_teleop
)

### Generating Module File
_generate_module_lisp(ria_teleop
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/ria_teleop
  "${ALL_GEN_OUTPUT_FILES_lisp}"
)

add_custom_target(ria_teleop_generate_messages_lisp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_lisp}
)
add_dependencies(ria_teleop_generate_messages ria_teleop_generate_messages_lisp)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/root/zy_ros_paper/zy_ws/src/r100_model_sim/ria_teleop/msg/Num.msg" NAME_WE)
add_dependencies(ria_teleop_generate_messages_lisp _ria_teleop_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/root/zy_ros_paper/zy_ws/src/r100_model_sim/ria_teleop/srv/AddTwoInts.srv" NAME_WE)
add_dependencies(ria_teleop_generate_messages_lisp _ria_teleop_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(ria_teleop_genlisp)
add_dependencies(ria_teleop_genlisp ria_teleop_generate_messages_lisp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS ria_teleop_generate_messages_lisp)

### Section generating for lang: gennodejs
### Generating Messages
_generate_msg_nodejs(ria_teleop
  "/root/zy_ros_paper/zy_ws/src/r100_model_sim/ria_teleop/msg/Num.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/ria_teleop
)

### Generating Services
_generate_srv_nodejs(ria_teleop
  "/root/zy_ros_paper/zy_ws/src/r100_model_sim/ria_teleop/srv/AddTwoInts.srv"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/ria_teleop
)

### Generating Module File
_generate_module_nodejs(ria_teleop
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/ria_teleop
  "${ALL_GEN_OUTPUT_FILES_nodejs}"
)

add_custom_target(ria_teleop_generate_messages_nodejs
  DEPENDS ${ALL_GEN_OUTPUT_FILES_nodejs}
)
add_dependencies(ria_teleop_generate_messages ria_teleop_generate_messages_nodejs)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/root/zy_ros_paper/zy_ws/src/r100_model_sim/ria_teleop/msg/Num.msg" NAME_WE)
add_dependencies(ria_teleop_generate_messages_nodejs _ria_teleop_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/root/zy_ros_paper/zy_ws/src/r100_model_sim/ria_teleop/srv/AddTwoInts.srv" NAME_WE)
add_dependencies(ria_teleop_generate_messages_nodejs _ria_teleop_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(ria_teleop_gennodejs)
add_dependencies(ria_teleop_gennodejs ria_teleop_generate_messages_nodejs)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS ria_teleop_generate_messages_nodejs)

### Section generating for lang: genpy
### Generating Messages
_generate_msg_py(ria_teleop
  "/root/zy_ros_paper/zy_ws/src/r100_model_sim/ria_teleop/msg/Num.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/ria_teleop
)

### Generating Services
_generate_srv_py(ria_teleop
  "/root/zy_ros_paper/zy_ws/src/r100_model_sim/ria_teleop/srv/AddTwoInts.srv"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/ria_teleop
)

### Generating Module File
_generate_module_py(ria_teleop
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/ria_teleop
  "${ALL_GEN_OUTPUT_FILES_py}"
)

add_custom_target(ria_teleop_generate_messages_py
  DEPENDS ${ALL_GEN_OUTPUT_FILES_py}
)
add_dependencies(ria_teleop_generate_messages ria_teleop_generate_messages_py)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/root/zy_ros_paper/zy_ws/src/r100_model_sim/ria_teleop/msg/Num.msg" NAME_WE)
add_dependencies(ria_teleop_generate_messages_py _ria_teleop_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/root/zy_ros_paper/zy_ws/src/r100_model_sim/ria_teleop/srv/AddTwoInts.srv" NAME_WE)
add_dependencies(ria_teleop_generate_messages_py _ria_teleop_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(ria_teleop_genpy)
add_dependencies(ria_teleop_genpy ria_teleop_generate_messages_py)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS ria_teleop_generate_messages_py)



if(gencpp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/ria_teleop)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/ria_teleop
    DESTINATION ${gencpp_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_cpp)
  add_dependencies(ria_teleop_generate_messages_cpp std_msgs_generate_messages_cpp)
endif()

if(geneus_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/ria_teleop)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/ria_teleop
    DESTINATION ${geneus_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_eus)
  add_dependencies(ria_teleop_generate_messages_eus std_msgs_generate_messages_eus)
endif()

if(genlisp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/ria_teleop)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/ria_teleop
    DESTINATION ${genlisp_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_lisp)
  add_dependencies(ria_teleop_generate_messages_lisp std_msgs_generate_messages_lisp)
endif()

if(gennodejs_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/ria_teleop)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/ria_teleop
    DESTINATION ${gennodejs_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_nodejs)
  add_dependencies(ria_teleop_generate_messages_nodejs std_msgs_generate_messages_nodejs)
endif()

if(genpy_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/ria_teleop)
  install(CODE "execute_process(COMMAND \"/usr/bin/python2\" -m compileall \"${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/ria_teleop\")")
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/ria_teleop
    DESTINATION ${genpy_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_py)
  add_dependencies(ria_teleop_generate_messages_py std_msgs_generate_messages_py)
endif()
