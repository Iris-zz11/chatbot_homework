from receive import rev_msg
import socket    # 一个抽象层，用来发送或接受数据（通信）
import requests  # 需要手动导入，是一个HTTP库
import datetime
import time
import random



# 发送消息
def send_msg(resp_dict):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ip = '192.168.137.1'  #  需要改为本机的ip地址
    client.connect((ip, 5700))
    # 回复类型（群聊/私聊）
    msg_type = resp_dict['msg_type']
    # qq群号
    number = resp_dict['number']
    # 消息
    msg = resp_dict['msg']
    # url编码
    msg = msg.replace(" ", "%20")
    msg = msg.replace("\n", "%0a")

    if msg_type == 'group':
        payload = "GET /send_group_msg?group_id=" + str(
            number) + "&message=" + msg + " HTTP/1.1\r\nHost:" + ip + ":5700\r\nConnection: close\r\n\r\n"
    elif msg_type == 'private':
        payload = "GET /send_private_msg?user_id=" + str(
            number) + "&message=" + msg + " HTTP/1.1\r\nHost:" + ip + ":5700\r\nConnection: close\r\n\r\n"
    print("发送" + payload)
    client.send(payload.encode("utf-8"))
    client.close()
    return 0

#定时发送群聊消息
while True:
    # 群号是可变的，只要机器人在就行
    qq=714553215 # 不过也可以是发送私聊消息，把下面的msg_type改成private就可以
    now = datetime.datetime.now()
    if(now.hour==0 and now.minute==0):   #晚上十二点在群聊里说姐姐们快点睡觉
        send_msg({'msg_type': 'group', 'number': qq, 'msg': '姐姐们快点睡觉！'})
        send_msg({'msg_type': 'group', 'number': qq, 'msg':'[CQ:poke,qq={}]'.format(qq)})
        time.sleep(60)
        continue
    if (now.hour == 20 and now.minute == 24):   # 晚上八点二十四说端午节快乐
        send_msg({'msg_type': 'group', 'number': qq, 'msg': '端午节快乐'})
        send_msg({'msg_type': 'group', 'number': qq, 'msg': '[CQ:poke,qq={}]'.format(qq)})
        time.sleep(60)
        continue
    else:
        continue

#  函数调用
send_msg({"msg_type": "group", "number": 714553215, "msg": '[CQ:face,id=2]'})
