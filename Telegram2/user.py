import socket
import threading
import time

true1 = True
true2 = True
# Ключ для кодирования сообщений 
key = 123

def contact (name, sock):
    ''' Функция принимает данные от других пользователей, декодируется.
Полученные сервером данные, обрабатываются данной функцией и отображаются как сообщения от пользователей, 
так как сообщения на сервере закодированы, данная функция расшифровывает эти данные.'''
    while true1:
        try:
            while True:
                data, address = sock.recvfrom(2048)
                text = ''
                g = True
                for m in data.decode('utf-8'):
                    if m == ':':
                        g = False
                        text += m
                    elif (g == True) or (m == ' '):
                        text += m
                    else:
                        text += chr(ord(m)^key)
                print(text)
        except:
            pass

# Создание ip-адреса для пользователей , которые подключаются к нашему серверу
host1 = socket.gethostbyname(socket.gethostname())
port = 0 
server = ('10.13.10.1', 8888)
socket1= socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
socket1.bind((host1,port))
# Пользователь может выйти из чата
socket1.setblocking(0)
# Имя пользователя
print('Введите своё имя:')
user = input()
# Обеспечиваем многопоточность, чтобы принимать данные от нескольких пользователей сразу
socket_thread = threading.Thread(target = contact, args = ('RecvThread',socket1) )
socket_thread.start()

while true1 == True:
    if true2 == True:
        # Уведомление о присоединении пользователей с их именем
        timemsg = time.strftime("%H.%M", time.localtime())
        socket1.sendto(( timemsg +' - '+'Пользователь ' + user + ' вошёл в чат').encode("utf-8"),server)
        true2 = False
    else:
        try:
            # Если пользователь уже присоединён к серверу, его сообщения кодируются и отправляются на сервер 
            msg = input()
            txt = ''

            for n in msg:
                txt += chr(ord(n)^key)
            msg = txt
            if msg != '':
                timemsg = time.strftime("%H.%M", time.localtime())
                socket1.sendto((timemsg + ' - ' + user + ' : ' + msg ).encode("utf-8"),server)
        except:
            # Если программа завершается, приходит уведомление о том, что пользователь покинул сервер 
            timemsg = time.strftime("%H.%M", time.localtime())
            socket1.sendto((timemsg + ' - '+ user +' покинул чат').encode("utf-8"),server)
            true1 = False
socket_thread.join()
socket1.close()


