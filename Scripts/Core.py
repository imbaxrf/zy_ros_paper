# -*- coding: utf-8 -*-

import _thread
import os
import sys
os.chdir(sys.path[0])
sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')
from multiprocessing import shared_memory

from utils.baidu_utils import *
from utils.requset_handler import *
from utils.time_system import *



def run_vision_module():
    os.system("cd UFLD_YOLO && python main_ufld_yolo.py -ip 127.0.0.1 -port 4444 -shm aaa -shmid 0 -testmode=True")


def tcp_req_handler(ip,port):
    addr = (ip, port)
    print("\033[32mRequest handler started at %s.\033[0m"%str(addr))
    server = socketserver.ThreadingTCPServer(addr, ReqHandlerTCP)
    server.serve_forever() # 永久循环执行

def fake_vehicle(ip,port):
    addr = (ip, port)
    print("\033[33mFake car started at %s.\033[0m"%str(addr))
    server = socketserver.ThreadingTCPServer(addr, ReqHandlerTCP)
    server.serve_forever()

def read_shared_memory():
    while True:
        a = shared_memory.ShareableList(name = "aaa")
        #print(a)
        if a[0] == "quit":
            print("END")
            break
    a.shm.close()


if __name__ == "__main__":

    shm_a = shared_memory.ShareableList([0,0,0,0,0,0,0],name = "aaa")

    print(get_time_stamp())
    try:
        _thread.start_new_thread( run_vision_module,())
        _thread.start_new_thread( read_shared_memory,())
        _thread.start_new_thread( fake_vehicle,('127.0.0.1',4444)) #实际上这应该是小车，这里做的是环回测试，故使用4444
        _thread.start_new_thread( tcp_req_handler,('127.0.0.1',5555)) 
    except:
        print("无法启动线程")
        #shm_a.shm.close()
        #shm_a.shm.unlink()    
    while 1:
        a = shared_memory.ShareableList(name = "aaa")
        #print(a)
        if a[0] == "quit":
            print("END")
            break
    a.shm.close()
    shm_a.shm.close()
    shm_a.shm.unlink()