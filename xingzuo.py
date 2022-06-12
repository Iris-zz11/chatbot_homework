import requests

def xingzuo(constellation):
    url = "http://web.juhe.cn/constellation/getAll?" + f'consName={constellation}&type=today&key=a82e5aeb45f03f8863fa89e9f3f6596d'
    # 发送get请求
    r = requests.get(url)
    print("响应->" , r)
    # 获取返回的json数据
    result = '综合指数 '+ r.json()['all']+'\n'+'幸运色 '+ r.json()['color']+'\n'\
             +'爱情指数 '+ r.json()['love']+'\n'+'今日概述 '+ r.json()['summary']
    print(result)
    return result

#xingzuo('摩羯座')