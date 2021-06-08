
import time
import _thread
import os 

from utils.baidu_utils import *
from utils.requset_handler import *


def run_UFLD():
    os.system("cd UFLD && python main_ufld.py")

def run_YOLO():
    os.system("cd YOLO && python main_yolo.py")

def tcp_req_handler(ip,port):
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
        _thread.start_new_thread(run_UFLD,())
        _thread.start_new_thread(run_YOLO,())
        _thread.start_new_thread( tcp_req_handler,("127.0.0.1",4444))
    except:
        print("无法启动线程")
    
    while 1:
        pass