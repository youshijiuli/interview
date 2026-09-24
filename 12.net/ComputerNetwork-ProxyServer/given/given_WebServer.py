#import socket module
from socket import *
serverSocket = socket(AF_INET, SOCK_STREAM) 
#Prepare a sever socket 
serverSocket.bind(('', 80)) # 将TCP欢迎套接字绑定到指定端口
serverSocket.listen(5) # 最大连接数为5

while True:
	#Establish the connection
	print('Ready to serve on port 80...')
	connectionSocket, addr = serverSocket.accept() # 接收到客户连接请求后，建立新的TCP连接套接字
	try:
		message = connectionSocket.recv(1024).decode() # 获取客户发送的报文
		print('message from client =',message)
		filename = message.split()[1]
		print('filename0=',filename)
		if('http' in filename ):
			filename='/'+filename.split('//')[1].partition('/')[2]
		print('filename=',filename)
		f = open(filename[1:])
		outputdata = f.read()
		
		#Send one HTTP header line into socket
		header = 'HTTP/1.1 200 OK\nConnection: close\nContent-Type: text/html\nContent-Length: %d\n\n' % (len(outputdata))
		out= header.encode('utf-8')
		#connectionSocket.send(header.encode('utf-8'))

		#Send the content of the requested file to the client
		for i in range(0, len(outputdata)):
			out+=outputdata[i].encode()
			#connectionSocket.send(outputdata[i].encode())
		print('outdata = ',out)
		connectionSocket.send(out)
		connectionSocket.close()
		print('send file ok')
	except IOError:
		#Send response message for file not found
		header = ' HTTP/1.1 404 Not Found'
		connectionSocket.send(header.encode())
		print('cannot find file')		
		#Close client socket
		connectionSocket.close()
serverSocket.close()
