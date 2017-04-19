#coding: utf-8
import music_mysql
import comment
import user

# 添加想要抓取的歌曲的ID
songs_name_data = [446945324, 417596830, 446945324, 34723470, 5239883, 461011, 432506345, 410042104, 350760, 33378384, 459793871, 229072, 31517361]


def spider_start():
    # 遍历想要爬取的歌曲，并将其（id,name,comment）添加到user_comment数据中
    for id in songs_name_data:
        comment.get_comment(id)
    # 从user_comment数据库中获取用户的个人（id，name）
    user_data = music_mysql.get_user_id_mysql()
    # 遍历得到的用户数据，并将其的（id，name，听歌排行中的前100首）歌添加到user_love_songs数据库中
    for user_data in user_data:
        uid = user_data['id']
        user_name = user_data['name']
        user.get_user_music(uid, user_name)

if __name__ == '__main__':
    spider_start()