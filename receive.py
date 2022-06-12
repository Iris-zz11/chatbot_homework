import socket
import json


# ListenSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# ListenSocket.bind(('127.0.0.1', 5701))
# ListenSocket.listen(100)
#
# HttpResponseHeader = '''HTTP/1.1 200 OK
# Content-Type: text/html
# '''

# 将信息转换为json格式
def request_to_json(msg):
    for i in range(len(msg)):
        if msg[i]=="{" and msg[-1]=="\n":
            return json.loads(msg[i:])
    return None

def rev_msg():

    ListenSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ListenSocket.bind(('127.0.0.1', 5701))
    ListenSocket.listen(5701)

    HttpResponseHeader = '''HTTP/1.1 200 OK
    Content-Type: text/html
    '''
    Client, Address = ListenSocket.accept()
    Request = Client.recv(1024).decode(encoding='utf-8')
    print(Request)    #  可以选择不打印，打印出来方便调试代码的
    rev_json=request_to_json(Request)
    Client.sendall((HttpResponseHeader).encode(encoding='utf-8'))
    Client.close()
    return rev_json
