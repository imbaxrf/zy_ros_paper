# -*- coding: utf-8 -*-
#from __future__ import print_function
#from urllib import urlopen
from urllib.request import urlopen
import requests
import json
import sys


ak = 'ts61soG2UcAhPP00rMq0KixlCMKX4z9M'


def get_coords(address, ret_coordtype='bd09ll'):
    """
    获取某一地点名称对应的坐标
    ret_coordtype:
    bd09ll（百度经纬度坐标）
    gcj02ll（国测局坐标）
    bd09mc（百度墨卡托坐标）
    """
    url = 'http://api.map.baidu.com/geocoding/v3/?address={inputAddress}&output=json&ak={ak}&ret_coordtype={ret_coordtype}'.format(inputAddress=address,ak=ak,ret_coordtype=ret_coordtype)
    res = requests.get(url)
    json_data = json.loads(res.text)
    if json_data['status'] == 0:
        lat = json_data['result']['location']['lat'] #纬度
        lng = json_data['result']['location']['lng'] #经度
    else:
        print("\033[31mRequest Failed in function %s().\033[0m" %(sys._getframe().f_code.co_name))
        return -1,-1    
    return lat,lng


def get_DirectionLite_driving_json_data(*args, in_coordtype='bd09ll',ret_coordtype='bd09ll'):
    """
    轻量级路线规划服务（又名DirectionLite API ）
    For 2 arguments: origin, destination
    For 4 arguments: origin_lat, origin_lng, destination_lat, destination_lng
    in_coordtype:
    bd09ll：百度经纬度坐标
    bd09mc：百度墨卡托坐标
    gcj02：国测局加密坐标
    wgs84：gps设备获取的坐标
    ret_coordtype:
    bd09ll：百度经纬度坐标
    gcj02：国测局加密坐标
    """    
    if len(args) == 2:
        origin = args[0]
        destination = args[1]
        olat,olng = get_coords(origin)
        dlat,dlng = get_coords(destination)
        print("\033[32mPlanning Path from '%s' to '%s'.\033[0m"%(origin,destination))
        print("\033[32mPlanning Path from '%s,%s' to '%s,%s' in %s coordinate system.\033[0m"%(olat,olng,dlat,dlng,ret_coordtype))
    elif len(args) == 4:
        olat = args[0]
        olng = args[1]
        dlat = args[2]
        dlng = args[3]
        print("\033[32mPlanning Path from '%s,%s' to '%s,%s' in %s coordinate system.\033[0m"%(olat,olng,dlat,dlng,ret_coordtype))
    url = 'http://api.map.baidu.com/directionlite/v1/driving?origin={olat},{olng}&destination={dlat},{dlng}&ak={ak}&coord_type={in_coordtype}&ret_coordtype={ret_coordtype}'.format(olat=olat, olng=olng, dlat=dlat, dlng=dlng, ak=ak, in_coordtype=in_coordtype, ret_coordtype=ret_coordtype) 
    req = urlopen(url)
    res = req.read().decode()
    json_data = json.loads(res)
    if json_data['status']!=0:
        print("\033[31mRequest Failed in function %s().\033[0m" %(sys._getframe().f_code.co_name))
    else:
        print("\033[32mGet Json successfully from '%s,%s' to '%s,%s' in %s coordinate system.\033[0m"%(olat,olng,dlat,dlng,ret_coordtype))
    return json_data


def get_path_info(json_data,index):
    path_info={}
    path_ERR = {'origin_lng':"-1",'origin_lat':"-1",'destination_lng':"-1",'destination_lat':"-1",'total_distance':"-1",'total_duration':"-1",'leg_index':"-1",'direction':"-1",'turn':"-1",'distance':"-1",'duration':"-1",'road_types':"-1",'instruction':"-1",'start_loaction_lng':"-1",'start_loaction_lat':"-1",'end_loaction_lng':"-1",'end_loaction_lat':"-1",'path':"-1",'traffic_condition_status':"-1",'traffic_condition_geo_cnt':"-1"}
    try:
        origin_lng = json_data['result']['origin']['lng']
        origin_lat = json_data['result']['origin']['lat']
        destination_lng = json_data['result']['destination']['lng']
        destination_lat = json_data['result']['destination']['lat']
        total_distance = json_data['result']['routes'][0]['distance']
        total_duration = json_data['result']['routes'][0]['duration']
        leg_index = json_data['result']['routes'][0]['steps'][index]['leg_index']
        direction = json_data['result']['routes'][0]['steps'][index]['direction']
        turn = json_data['result']['routes'][0]['steps'][index]['turn']
        distance = json_data['result']['routes'][0]['steps'][index]['distance']
        duration = json_data['result']['routes'][0]['steps'][index]['duration']
        road_types = json_data['result']['routes'][0]['steps'][index]['road_types']
        instruction = json_data['result']['routes'][0]['steps'][index]['instruction']
        start_loaction_lng = json_data['result']['routes'][0]['steps'][index]['start_location']['lng']
        start_loaction_lat = json_data['result']['routes'][0]['steps'][index]['start_location']['lat']
        end_loaction_lng = json_data['result']['routes'][0]['steps'][index]['end_location']['lng']
        end_loaction_lat = json_data['result']['routes'][0]['steps'][index]['end_location']['lat']
        path = json_data['result']['routes'][0]['steps'][index]['path']
        traffic_condition_status = json_data['result']['routes'][0]['steps'][index]['traffic_condition'][0]['status']
        traffic_condition_geo_cnt = json_data['result']['routes'][0]['steps'][index]['traffic_condition'][0]['geo_cnt']
        
        path_info = {'origin_lng':origin_lng,'origin_lat':origin_lat,'destination_lng':destination_lng,'destination_lat':destination_lat,'total_distance':total_distance,'total_duration':total_duration,'leg_index':leg_index,'direction':direction,'turn':turn,'distance':distance,'duration':duration,'road_types':road_types,'instruction':instruction,'start_loaction_lng':start_loaction_lng,'start_loaction_lat':start_loaction_lat,'end_loaction_lng':end_loaction_lng,'end_loaction_lat':end_loaction_lat,'path':path,'traffic_condition_status':traffic_condition_status,'traffic_condition_geo_cnt':traffic_condition_geo_cnt}   
    
    except Exception as e:
        print("\033[31mCatch Exception: \033[0m",e)
        return path_ERR
    return path_info


def get_steps_num(json_data):
    """
    计算路径的分段数
    """
    steps = 0
    try:
        while True:
            json_data['result']['routes'][0]['steps'][steps]
            steps = steps + 1
    except Exception:
        return steps  


def print_coords_to_file(json_data, file_name, pure_waypoint = True):
    '''
    pure_waypoint参数用来打印连续不间断的路径点
    '''
    steps = get_steps_num(json_data)
    fw = open(file_name,"w")
    for i in range(steps):
        dist = get_path_info(json_data,i)
        print(dist["path"]+";",file=fw)
    fw.close()
    fr = open(file_name,"r")
    lines = fr.readlines()
    fw = open(file_name,"w")
    for i,line in enumerate(lines):
        line = line.replace(";","\n")
        if pure_waypoint == True:
            line = line.replace("\n",";")
            line = line.replace(";;",";")
            line = line.replace(";","\n")
        fw.write(line)
    fw.close()
    fr.close()
        
    if pure_waypoint == True: 
        fr = open(file_name,"r")
        lines = fr.readlines()
        fw = open(file_name,"w")
        for i in range(len(lines)):
            if i < len(lines) - 1:
                if lines[i] == lines[i+1]:
                    lines[i] = ""
            fw.write(lines[i])          
        fw.close()
        fr.close()
    print("\033[32mCreated " + file_name + " for MATLAB.\033[0m")


def coords_trans(lat,lng,coords_from=1,coords_to=5):
    """
    坐标转换
    源坐标类型：
    1：GPS标准坐标;
    2：sogou地图坐标;
    3：amap、tencent和mapabc地图坐标
    4：3中列举的地图坐标对应的墨卡托平面坐标;
    5：百度地图采用的经纬度坐标（bd09ll）；
    6：百度地图采用的墨卡托平面坐标（bd09mc）;
    7：mapbar地图坐标;
    8：51地图坐标
    目标坐标类型：
    5：bd09ll(百度经纬度坐标);
    6：bd09mc(百度墨卡托平面坐标
    """
    url = "http://api.map.baidu.com/geoconv/v1/?coords={lng},{lat}&from={coords_from}&to={coords_to}&ak={ak}".format(lat=lat, lng=lng, coords_from=coords_from, coords_to=coords_to, ak=ak)
    res = requests.get(url)
    json_data = json.loads(res.text)
    if json_data['status'] == 0:   
        lng = json_data['result'][0]['x'] #经度
        lat = json_data['result'][0]['y'] #纬度
    else:
        print("\033[31mRequest Failed in function %s().\033[0m" %(sys._getframe().f_code.co_name))
        return -1,-1    
    return lat,lng

def trans_to_bd09mc_file(file_name):
    fr = open(file_name,"r")
    lines = fr.readlines()
    print("\033[32m"+str(len(lines))+" coords in total.\033[0m")
    fw = open(file_name,"w")
    for i,line in enumerate(lines):
        lat,lng = coords_trans(line.split(",")[1],line.split(",")[0],1,6)
        print("\033[32m"+str(i+1)+" coords transfered.\033[0m",end='\r')
        line = str(lat)+","+str(lng)+'\n'
        fw.write(line)
    fw.close()
    fr.close()
    print("\033[32mTransfered " + file_name + " in bd09mc.\033[0m")



if __name__ == "__main__":
    json_data = get_DirectionLite_driving_json_data("孝陵卫地铁站","下马坊地铁站")
    print_coords_to_file(json_data, "../coords.txt")
    trans_to_bd09mc_file("../coords.txt")
    lat,lng = get_coords("下马坊-地铁站")
    print("bd09ll:  lat: %s , lng: %s "%(lat,lng))
    lat,lng = get_coords("下马坊-地铁站","gcj02ll")
    print("gcj02ll: lat: %s , lng: %s "%(lat,lng))
    lat,lng = coords_trans(lat,lng,3,5)
    print("bd09ll:  lat: %s , lng: %s "%(lat,lng))
    

#bd09ll:      lat:  32.04413425286225 lng:  118.85276141456676
