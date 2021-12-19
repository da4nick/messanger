import socket, time

host1 = socket.gethostbyname(socket.gethostname())
port = 8888
# С помощью списка серверов, какой-либо пользователь не сможет получить своё же сообщение
all_users = []

socket1 = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
socket1.bind((host1,port))

p = True
print("Сервер запущен!")

while p:
	try:
		# Основная часть сервера, которая отвечает за принятие и отправку данных
		data, address = socket1.recvfrom(2048)

		if address not in all_users:
			all_users.append(address)

		timemsg = time.strftime("%H.%M", time.localtime())

		print(str(address[1])+" - " +timemsg+ " : " ,end="")
		print(data.decode("utf-8"))
    
		for user in all_users:
			if address != user:
				socket1.sendto(data,user)
	except:	
		print("Сервер остановлен!")
		p = False
		
socket1.close()