import requests

# 获取群成员信息，打印出群昵称和QQ号
def get_group(id):
    response = requests.post('http://192.168.137.1:5700/get_group_member_list?group_id='+str(id)).json()
    for i in response['data']:
        if(i['card']!=''):
            print(i['card']+str(i['user_id']))
        else:
            print(i['nickname']+str(i['user_id']))   #  没有群昵称就打印QQ昵称


get_group(714553215)