#TODO 当前GPS坐标
from math import atan2
from utils.baidu_utils import *

import numpy as np

lat = 0.0 #纬度
lng = 0.0 #经度

#/mavros/global_position/compass_hdg下始终指向正北方的角，假设
NORTH_RADIAN = 300 * np.pi / 180

def turn_to_north_radian():
    #to ros
    pass#first turn

def get_current_compass_hdg():
    angle = 0.0
    pass
    return angle


def get_current_turn_angle(file_name):
    """
    获取相对于百度地图规划出bd09mc坐标系的路线正北方向的角度
    """
    fr = open(file_name,"r")
    lines = fr.readlines()
    rad = []
    for i in range(len(lines)-1):
        b = lines[i+1].split(",")
        a = lines[i].split(",")
        rad.append(atan2((float(b[1])-float(a[1])) , (float(b[0])-float(a[0]))))
    print(rad)
    return rad


def get_ublox_gps():
    pass
    return lat,lng
            

if __name__ == "__main__":


    get_current_turn_angle("coords.txt")

