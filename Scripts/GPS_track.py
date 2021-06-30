from math import atan2
import numpy as np

from utils.baidu_utils import *


#/mavros/global_position/compass_hdg下始终指向正北方的角，假设
NORTH_RADIAN = 213 * np.pi / 180


def turn_to_north_radian():
    #to ros
    pass#first turn


def get_current_compass_hdg():
    angle = 0.0
    pass
    return angle


def get_current_ublox_gps():
    lat = 0.0 #纬度
    lng = 0.0 #经度
    pass
    return lat,lng


def get_turn_radian(file_name,saved_name):
    """
    获取相对于百度地图规划出bd09mc坐标系的路线正北方向的角度
    """
    fr = open(file_name,"r")
    lines = fr.readlines()
    fw = open(saved_name,"w")
    rad = []
    for i in range(len(lines)-1):
        b = lines[i+1].split(",")
        a = lines[i].split(",")
        rad.append(atan2((float(b[1])-float(a[1])) , (float(b[0])-float(a[0]))))
        fw.write(str(atan2((float(b[1])-float(a[1])) , (float(b[0])-float(a[0]))))+"\n")
    fw.close()
    fr.close()
    return rad
            

if __name__ == "__main__":

    rad = get_turn_radian("coords_bd09mc.txt",'coords_turn_rad.txt')
    print(rad)

