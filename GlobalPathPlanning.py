import requests
import json
from urllib.request import urlopen
import urllib

ak = 'ts61soG2UcAhPP00rMq0KixlCMKX4z9M'

def getPosition(address):
    url = 'http://api.map.baidu.com/geocoding/v3/?address={inputAddress}&output=json&ak={myAk}'.format(inputAddress=address,myAk=ak)
    res = requests.get(url)
    json_data = json.loads(res.text)
    if json_data['status'] == 0:
        lat = json_data['result']['location']['lat'] #纬度
        lng = json_data['result']['location']['lng'] #经度
    else:
        print("Error output!")
        return json_data['status']
    return lat,lng

def getPathInfo(origin,destination,i=0):
    path_info={}
    olat,olng = getPosition(origin)
    dlat,dlng = getPosition(destination)
    url = 'http://api.map.baidu.com/directionlite/v1/driving?origin={olat},{olng}&destination={dlat},{dlng}&ak={myAk}'.format(olat=olat, olng=olng, dlat=dlat, dlng=dlng, myAk=ak) 
    req = urlopen(url)
    print(url)
    res = req.read().decode()
    json_data = json.loads(res)
    if json_data['status']!=0:
        return -1
    try:
        origin_lng = json_data['result']['origin']['lng']
        origin_lat = json_data['result']['origin']['lat']
        destination_lng = json_data['result']['destination']['lng']
        destination_lat = json_data['result']['destination']['lat']
        total_distance = json_data['result']['routes'][0]['distance']
        total_duration = json_data['result']['routes'][0]['duration']
        leg_index = json_data['result']['routes'][0]['steps'][i]['leg_index']
        direction = json_data['result']['routes'][0]['steps'][i]['direction']
        turn = json_data['result']['routes'][0]['steps'][i]['turn']
        distance = json_data['result']['routes'][0]['steps'][i]['distance']
        duration = json_data['result']['routes'][0]['steps'][i]['duration']
        road_types = json_data['result']['routes'][0]['steps'][i]['road_types']
        instruction = json_data['result']['routes'][0]['steps'][i]['instruction']
        start_loaction_lng = json_data['result']['routes'][0]['steps'][i]['start_location']['lng']
        start_loaction_lat = json_data['result']['routes'][0]['steps'][i]['start_location']['lat']
        end_loaction_lng = json_data['result']['routes'][0]['steps'][i]['end_location']['lng']
        end_loaction_lat = json_data['result']['routes'][0]['steps'][i]['end_location']['lat']
        path = json_data['result']['routes'][0]['steps'][i]['path']
        traffic_condition_status = json_data['result']['routes'][0]['steps'][i]['traffic_condition'][0]['status']
        traffic_condition_geo_cnt = json_data['result']['routes'][0]['steps'][i]['traffic_condition'][0]['geo_cnt']
        
        path_info = {'origin_lng':origin_lng,'origin_lat':origin_lat,'destination_lng':destination_lng,'destination_lat':destination_lat,'total_distance':total_distance,'total_duration':total_duration,'leg_index':leg_index,'direction':direction,'turn':turn,'distance':distance,'duration':duration,'road_types':road_types,'instruction':instruction,'start_loaction_lng':start_loaction_lng,'start_loaction_lat':start_loaction_lat,'end_loaction_lng':end_loaction_lng,'end_loaction_lat':end_loaction_lat,'path':path,'traffic_condition_status':traffic_condition_status,'traffic_condition_geo_cnt':traffic_condition_geo_cnt}
        
    except Exception as e:
        print("触发异常:",e)
        return -1
    return path_info

if __name__ == "__main__":
    add = '南京理工大学-4号门'
    lat,lng = getPosition(add)
    dist = getPathInfo("南京理工大学","天安门广场",1)
    print(dist['distance'])
    print("运单地址：{0}|经度:{1}|纬度:{2}.".format(add,lng,lat))