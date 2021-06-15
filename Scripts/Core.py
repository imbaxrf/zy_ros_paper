import _thread
import os

from utils.baidu_utils import *
from utils.requset_handler import *
from utils.time_system import *

def run_vision_module():
    os.system("cd UFLD_YOLO && python main_ufld_yolo.py -ip 127.0.0.1 -port 4444 -shm aaa -onlinemode True")

def tcp_req_handler(ip,port):#TODO改成发送 并集成在ufld yolo里 给Python2.7也就是机器人用的
    server = socketserver.ThreadingTCPServer((ip,port), ReqHandlerTCP)
    server.serve_forever() # 永久循环执行



if __name__ == "__main__":


    print(get_time_stamp())
    try:
        _thread.start_new_thread( run_vision_module,())
        #_thread.start_new_thread( tcp_req_handler,("127.0.0.1",4444))
    except:
        print("无法启动线程")
    
    while 1:
        pass