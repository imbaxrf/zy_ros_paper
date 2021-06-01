from utils.baidu_utils import *
import time

origin = "南京理工大学"
destination = "南京农业大学"

while True:
    now = time.time()
    print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(now)))
json_data = get_DirectionLite_driving_json_data(origin,destination)
print_coords_to_file(json_data,"coords.txt")
