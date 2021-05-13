#!/bin/sh

if [ -n "$DESTDIR" ] ; then
    case $DESTDIR in
        /*) # ok
            ;;
        *)
            /bin/echo "DESTDIR argument must be absolute... "
            /bin/echo "otherwise python's distutils will bork things."
            exit 1
    esac
fi

echo_and_run() { echo "+ $@" ; "$@" ; }

echo_and_run cd "/root/zy_ros_paper/zy_ws/src/rqt_joint_trajectory_controller"

# ensure that Python install destination exists
echo_and_run mkdir -p "$DESTDIR/root/zy_ros_paper/zy_ws/install/lib/python2.7/dist-packages"

# Note that PYTHONPATH is pulled from the environment to support installing
# into one location when some dependencies were installed in another
# location, #123.
echo_and_run /usr/bin/env \
    PYTHONPATH="/root/zy_ros_paper/zy_ws/install/lib/python2.7/dist-packages:/root/zy_ros_paper/zy_ws/build/lib/python2.7/dist-packages:$PYTHONPATH" \
    CATKIN_BINARY_DIR="/root/zy_ros_paper/zy_ws/build" \
    "/usr/bin/python2" \
    "/root/zy_ros_paper/zy_ws/src/rqt_joint_trajectory_controller/setup.py" \
     \
    build --build-base "/root/zy_ros_paper/zy_ws/build/rqt_joint_trajectory_controller" \
    install \
    --root="${DESTDIR-/}" \
    --install-layout=deb --prefix="/root/zy_ros_paper/zy_ws/install" --install-scripts="/root/zy_ros_paper/zy_ws/install/bin"
