import get_emotion
import pymysql
import datetime
import json
import time
from scrapy.exporters import JsonItemExporter


class MysqlPipeline:
    mysql = None
    cursor = None

    def open_spider(self, spider):
        self.mysql = pymysql.Connect(
            host='101.42.44.139',
            user='root',
            password='qwe123',
            port=3306,
            charset='utf8mb4',
            database='cloud'
        )
        self.cursor = self.mysql.cursor()

    def process_item(self, item, spider):
        query = None
        args = None
        if item.name == 'thread':
            emotion = 0
            if item['thread_title']:
                emotion = get_emotion.get_emotion_snownlp(item['thread_title'])
            emotion = str(emotion)
            query = 'replace into thread(thread_id, first_post_id, thread_title,reply_num,emotion)' \
                    'values(%s, %s, %s, %s,%s)'

            args = (
                item['thread_id'], item['first_post_id'], item['thread_title'],
                item['reply_num'], emotion)
        elif item.name == 'post':
            emotion = 0
            if item['content']:
                emotion = get_emotion.get_emotion_snownlp(item['content'])
            emotion = str(emotion)
            query = 'replace into post(post_id,thread_id, content, comment_num, time, ip,emotion)' \
                    'values(%s, %s, %s, %s, %s, %s,%s)'
            args = (item['post_id'], item['thread_id'], item['content'], item['comment_num'],
                    datetime.datetime.strptime(item['time'], '%Y-%m-%d %H:%M'), item['ip'], emotion)
        elif item.name == 'comment':
            emotion = 0
            if item['content']:
                emotion = get_emotion.get_emotion_snownlp(item['content'])
            emotion = str(emotion)
            print(emotion)
            query = 'replace into comment(comment_id, thread_id,post_id, content, time,emotion)' \
                    'values(%s, %s, %s, %s, %s,%s)'
            args = (item['comment_id'], item['thread_id'], item['post_id'], item['content'],
                    datetime.datetime.strptime(item['time'], '%Y-%m-%d %H:%M'), emotion)

        if query and args:
            try:
                self.cursor.execute(query, args)
                self.mysql.commit()
            except Exception as e:
                print(f'{item.name} 操作异常！！！', e)
                self.mysql.rollback()
        return item

    def close_spider(self, spider):
        self.cursor.close()
        self.mysql.close()


class JsonPipeline:
    def __init__(self):
        self.date = time.strftime('%Y-%m-%d', time.localtime())
        self.thread = open('./data/{}-thread.json'.format(self.date), 'wb')
        self.comment = open('./data/{}-comment.json'.format(self.date), 'wb')
        self.post = open('./data/{}-post.json'.format(self.date), 'wb')

    def process_item(self, item, spider):
        fn_map = {'thread': self.thread, 'post': self.post, 'comment': self.comment}
        line = json.dumps(dict(item)) + "\n"
        fn_map[item.name].write(line.encode('utf-8'))
        return item

    def close_spider(self, spider):
        self.thread.close()
        self.comment.close()
        self.post.close()
