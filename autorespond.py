from receive import rev_msg
import xingzuo
import socket
import requests
import random
import urllib.request
from urllib.parse import quote
import string
# 发送消息
def send_msg(resp_dict):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ip = '192.168.137.1'
    client.connect((ip, 5700))
    # 回复类型（群聊/私聊）
    msg_type = resp_dict['msg_type']
    # qq号
    number = resp_dict['number']
    # 消息
    msg = resp_dict['msg']
    # url编码
    msg = msg.replace(" ", "%20")
    msg = msg.replace("\n", "%0a")

    if msg_type == 'group':  #  基础传输 HTTP GET 可以参考文档
        payload = "GET /send_group_msg?group_id=" + str(
            number) + "&message=" + msg + " HTTP/1.1\r\nHost:" + ip + ":5700\r\nConnection: close\r\n\r\n"
    elif msg_type == 'private':
        payload = "GET /send_private_msg?user_id=" + str(
            number) + "&message=" + msg + " HTTP/1.1\r\nHost:" + ip + ":5700\r\nConnection: close\r\n\r\n"
    print("发送" + payload)
    client.send(payload.encode("utf-8"))
    client.close()
    return 0

while True:
    try:
        rev = rev_msg()
        print(rev)
        if rev == None:
            continue
    except:
        continue
    # 端口信息类型为message，表示接收到了消息
    if rev["post_type"] == "message":
        # 私聊
        if rev["message_type"] == "private": #私聊
            message = rev['raw_message']
            if 'face' in message:   #  重复表情
                qq = rev['sender']['user_id']
                img = rev['raw_message']
                send_msg({'msg_type': 'private', 'number': qq, 'msg': img})
            elif 'image' in message:   #  重复图片
                qq = rev['sender']['user_id']
                img = rev['raw_message']
                send_msg({'msg_type': 'private', 'number': qq, 'msg': img})
            elif '星座运势' in message:
                try:
                    constellation = message.split(' ')[1]
                    text = xingzuo.xingzuo(constellation)
                    qq = rev['sender']['user_id']
                    send_msg({'msg_type': 'private', 'number': qq, 'msg': text})
                except:
                    qq = rev['sender']['user_id']
                    send_msg({'msg_type': 'private', 'number': qq, 'msg': '笨蛋忘了星座前面的空格啦'})

            else:       #  智能回复api
                url = 'http://api.qingyunke.com/api.php?key=free&appid=0&msg=' + message
                s = quote(url, safe=string.printable)
                try:  # 异常处理
                    with urllib.request.urlopen(s) as response:
                        html = response.read()
                        # 将获取到的响应内容进行解码，并将json字符串内容转换为python字典格式
                        # 通过下标取到机器人回复的内容
                        qq = rev['sender']['user_id']
                        send_msg({'msg_type': 'private', 'number': qq,
                                  'msg': eval(html.decode("utf-8"))["content"].replace('{br}', '\n')})
                except:
                    qq = rev['sender']['user_id']
                    send_msg({'msg_type': 'private', 'number': qq, 'msg': '我好笨听不懂诶'})
        #  群聊
        elif rev["message_type"] == "group":  # 群聊

            groupqq = rev['group_id']

            qq = rev["self_id"]

            if f"[CQ:at,qq={qq}]" in rev["raw_message"]:
                message = rev['raw_message']
                if 'face' in message:  # 重复表情
                    img = '不懂你在说什么欸'
                    send_msg({'msg_type': 'group', 'number': groupqq, 'msg': img})
                elif 'image' in message:  # 重复图片，这个功能只能pc端使用，手移动端不能同时艾特+图片欸
                    img = '可以私聊给我发图片试试哦'
                    send_msg({'msg_type': 'group', 'number': groupqq, 'msg': img})
                else:  # 智能回复api
                    message = rev["message"].replace(f"[CQ:at,qq={qq}]", "")
                    print("rev", message)
                    url = f'http://api.qingyunke.com/api.php?key=free&appid=0&msg={message}'
                    # print("requests.get(url)", requests.get(url).json())

                    html = requests.get(url).json()
                    send_msg({'msg_type': 'group', 'number': groupqq,
                              'msg': html["content"].replace('{br}', '\n')})
        else:
            continue
    else:  # rev["post_type"]=="meta_event":
        continue