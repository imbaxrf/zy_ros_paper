
import time
import _thread
import os 

from utils.baidu_utils import *
from utils.requset_handler import *


def run_vision_module():
    os.system("cd UFLD_YOLO && python main_ufld_yolo.py")

def tcp_req_handler(ip,port):#TODO改成发送 并集成在ufld yolo里
    server = socketserver.ThreadingTCPServer((ip,port), ReqHandlerTCP)
    server.serve_forever() # 永久循环执行

def print_time( threadName, delay):
    count = 0
    while count < 100:
        time.sleep(delay)
        count += 1
        print ("%s: %s" % ( threadName, time.ctime(time.time()) ))


if __name__ == "__main__":
    try:
        _thread.start_new_thread( run_vision_module,())
        _thread.start_new_thread( tcp_req_handler,("127.0.0.1",4444))
    except:
        print("无法启动线程")
    
    while 1:
        pass