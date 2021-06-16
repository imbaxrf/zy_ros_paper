import _thread
import os
from multiprocessing import shared_memory
from time import sleep
from urllib.parse import scheme_chars

from utils.baidu_utils import *
from utils.requset_handler import *
from utils.time_system import *

def run_vision_module():
    sleep(5)
    os.system("cd UFLD_YOLO && python main_ufld_yolo.py -ip 127.0.0.1 -port 4444 -shm aaa")

def tcp_req_handler(ip,port):#TODO改成发送 并集成在ufld yolo里 给Python2.7也就是机器人用的
    print("\033[32mRequest Handler Started!\033[0m")
    addr = (ip, port)
    server = socketserver.ThreadingTCPServer(addr, ReqHandlerTCP)
    server.serve_forever() # 永久循环执行


def read_shared_memory():
    sleep(10)
    while True:
        a = shared_memory.ShareableList(name = "aaa")
        print(a)
        if a[6] == "quit":
            print("END")
            break
    a.shm.close()


if __name__ == "__main__":

    shm_a = shared_memory.ShareableList([0,0,0,0,0,0,0],name = "aaa")
    print(get_time_stamp())
    try:
        _thread.start_new_thread( run_vision_module,())
        _thread.start_new_thread( read_shared_memory,())
        _thread.start_new_thread( tcp_req_handler,('127.0.0.1',4444))
    except:
        print("无法启动线程")
        shm_a.shm.close()
        shm_a.shm.unlink()
        
    
    while 1:
        pass