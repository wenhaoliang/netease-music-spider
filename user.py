#coding: utf-8
import requests
import json
import music_mysql
import pymysql
# header
headers = {
    'Referer': 'http://music.163.com/',
    'Cookie': 'appver=1.5.0.75771;MUSIC_U=e954e2600e0c1ecfadbd06b365a3950f2fbcf4e9ffcf7e2733a8dda4202263671b4513c5c9ddb66f1b44c7a29488a6fff4ade6dff45127b3e9fc49f25c8de500d8f960110ee0022abf122d59fa1ed6a2;',
}
# post的数据
user_data = {
    'uid': '107948356',
    'type': '0',
    'params': 'vRlMDmFsdQgApSPW3Fuh93jGTi/ZN2hZ2MhdqMB503TZaIWYWujKWM4hAJnKoPdV7vMXi5GZX6iOa1aljfQwxnKsNT+5/uJKuxosmdhdBQxvX/uwXSOVdT+0RFcnSPtv',
    'encSecKey': '46fddcef9ca665289ff5a8888aa2d3b0490e94ccffe48332eca2d2a775ee932624afea7e95f321d8565fd9101a8fbc5a9cadbe07daa61a27d18e4eb214ff83ad301255722b154f3c1dd1364570c60e3f003e15515de7c6ede0ca6ca255e8e39788c2f72877f64bc68d29fac51d33103c181cad6b0a297fe13cd55aa67333e3e5'
}
# 添加用户id、名字、以及喜欢的歌曲到user_love_songs数据库中


def get_user_music(uid,user_name):
    data = []
    url = 'http://music.163.com/weapi/v1/play/record?csrf_token='
    user_data['uid'] = uid
    user_data['type'] = '0'
    response = requests.post(url, headers=headers, data=user_data)
    response = response.content
    json_text= json.loads(response.decode("utf-8"))
    try:
        json_all_data = json_text['allData']
        for json_music in json_all_data:
            json_song = json_music['song']
            json_song_name = json_song['name']   # 歌曲名字
            # print(json_song_name, end="")
            # print('---', end="")
            # 演唱者名字
            ar = json_song['ar']
            length = len(ar)
            songer_name = ''
            for songer in range(0, length):
                songer_name = songer_name + ar[songer]['name']
                # print(ar[songer]['name'], end="")
                # if (songer != length - 1):
                #     print('/', end="")
                # if (songer == length - 1):
                #     print('')
            # print(songer_name)
            song = json_song_name + '---' + songer_name
            data.append(song)
        # 添加用户id、名字、以及喜欢的歌曲到数据库中
        music_mysql.insert_user(uid, user_name, data=data)
    except pymysql.err.IntegrityError:
        print('id为', end="")
        print(uid, end="")
        print('的用户已经添加到user_luve_songs数据库中啦~')
    except KeyError:
        print('id为', end="")
        print(uid, end="")
        print('的用户听歌排行不可查看~')
    except Exception as e:
        print('出现错误啦~错误是:', e)