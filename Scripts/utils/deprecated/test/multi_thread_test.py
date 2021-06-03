import _thread as th
import time

def print_time( threadName, delay):
   count = 0
   while count < 5:
      time.sleep(delay)
      count += 1
      print ("%s: %s" % ( threadName, time.ctime(time.time()) ))

# 创建两个线程
try:
   th.start_new_thread( print_time, ("Thread-1", 2 ) )
   th.start_new_thread( print_time, ("Thread-2", 4 ) )
except:
   print ("Error: 无法启动线程")

while 1:
   pass
