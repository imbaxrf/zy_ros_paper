import socket
import time

#client 发送端
address_and_port = ('127.0.0.1',4444) # 接收方 服务器的ip地址和端口号
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    start = time.time()  #获取当前时间
    print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(start)))  #以指定格式显示当前时间
    send_data = input("请输入要发送的内容：")  
    client.sendto(send_data.encode('utf-8'), address_and_port) #将msg内容发送给指定接收方
    now = time.time() #获取当前时间
    run_time = now-start #计算时间差，即运行时间
    print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(now)))
    print("run_time: %d seconds\n" %run_time)
    if send_data == 'quit':
        break
client.close()