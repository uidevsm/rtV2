from socket import *
import datetime

# إعدادات الخادم
serverPort = 12000
# AF_INET هو لـ IPv4 - SOCK_STREAM هو لـ TCP
serverSocket = socket(AF_INET, SOCK_STREAM) 
serverSocket.bind(('', serverPort))
serverSocket.listen(5)  # زيادة عدد الاتصالات المسموح بها

print(f'The server is listening on localhost : {serverPort}')
print('-----------------------------------------------------')

while True:
    try:
        connectionSocket, addr = serverSocket.accept()
        print('Client connected from', addr)
        
        while True:
            try:
                sentence = connectionSocket.recv(1024)
                if not sentence:
                    break  # إذا لم يتم استلام أي بيانات، نغلق الاتصال
                numOfCharacters = len(sentence)
                connectionSocket.send(str(numOfCharacters).encode())
                print(f'--> message received and processed on {datetime.datetime.now()}')
            except Exception as e:
                print(f'Error during data reception: {e}')
                break

        connectionSocket.close()
        print('Connection closed with', addr)
        print('-----------------------------------------------------')

    except Exception as e:
        print(f'Error: {e}')