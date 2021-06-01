import socket  #导入socket模块
import time #导入time模块
# server 接收端
# 设置服务器默认端口号
# 创建一个套接字socket对象，用于进行通讯
# socket.AF_INET 指明使用INET地址集，进行网间通讯
# socket.SOCK_DGRAM 指明使用数据协议，即使用传输层的udp协议
address_and_port = ('127.0.0.1',4444)
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(address_and_port)  # 为服务器绑定一个固定的地址，ip和端口
server.settimeout(10)  #设置一个时间提示，如果10秒钟没接到数据进行提示    
while True:
	#正常情况下接收数据并且显示，如果10秒钟没有接收数据进行提示（打印 "time out"）
	#当然可以不要这个提示，那样的话把"try:" 以及 "except"后的语句删掉就可以了
    try:  
        now = time.time()  #获取当前时间
		# 接收客户端传来的数据 recvfrom接收客户端的数据，默认是阻塞的，直到有客户端传来数据
		# recvfrom 参数的意义，表示最大能接收多少数据，单位是字节
		# recvfrom返回值说明
		# receive_data表示接受到的传来的数据,是bytes类型
		# client  表示传来数据的客户端的身份信息，客户端的ip和端口，元组
        recv_data, address = server.recvfrom(1024)
        recv_data = recv_data.decode('utf-8')
        if recv_data == 'quit':
            break
        print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(now))) #以指定格式显示时间
        print('来自客户端%s,发送的%s' % (address,recv_data)) #打印接收的内容
    except socket.timeout:  #如果10秒钟没有接收数据进行提示（打印 "time out"）
        print("time out")
server.close()
