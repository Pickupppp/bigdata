# -*- coding: utf-8 -*-
import findspark

findspark.init()

from pyspark import SparkConf, SparkContext
from pyspark.sql import SparkSession
import settings
import pymysql
from dbutils.pooled_db import PooledDB
import datetime
import time


class Dao:

    def __init__(self):
        # spark 配置
        conf = SparkConf().setAppName('data-getter').setMaster(settings.SPARK_MASTER)
        sc = SparkContext(conf=conf)
        sc.setLogLevel('WARN')
        self._spark = SparkSession.Builder().config(conf=conf).getOrCreate()
        # 数据库配置
        prop = {
            'host': settings.HOST,
            'port': settings.PORT,
            'database': settings.DATABASE,
            'user': settings.USERNAME,
            'password': settings.PASSWORD,
            'charset': 'utf8mb4',
            'maxconnections': 10,  # 连接池允许的最大连接数
            'blocking': True  # 连接数达到最大时，新连接是否可阻塞。默认False，即达到最大连接数时，再取新连接将会报错
        }
        self._pool = PooledDB(pymysql, **prop)
        # hdfs 配置
        self._hdfs = settings.HDFS_URL + '/result'

    def read_json(self, path):
        df = self._spark.read.json(self._hdfs + path, encoding='utf8').collect()
        return df

    # 获取连接、游标
    def get_conn(self):
        conn = self._pool.connection()
        curs = conn.cursor()
        return conn, curs

    # 关闭游标、连接
    def close_conn(self, curs, conn):
        curs.close()
        conn.close()

    def exe_sql(self, sql, args=None, way=None, get_affect=False):
        conn, curs = self.get_conn()
        try:
            affect = curs.execute(sql, args=args)
            conn.commit()
        except Exception as e:
            conn.rollback()
            print("错误  ==>  exe_sql  ==>  {}".format(e))
            return False
        else:
            if way == 1:
                return curs.fetchone()
            elif way == 2:
                return curs.fetchall()
            elif get_affect is True:
                return affect
            else:
                return True
        finally:
            self.close_conn(curs, conn)


dao = Dao()


def get_thread_wordcount():
    return dao.read_json('/thread_wordcount.json')


def get_post_wordcount():
    return dao.read_json('/post_wordcount.json')


def get_post_ip():
    return dao.read_json('/post_ip.json')


def get_comment_wordcount():
    return dao.read_json('/comment_wordcount.json')


def get_yesterday_post():
    """过去24小时新增帖子"""
    yesterday = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
    sql = 'select count(*) from clean_post where date(time) = %s'
    args = yesterday
    res = dao.exe_sql(sql, args, way=1)
    return res[0]


def get_yesterday_comment():
    """过去24小时新增评论"""
    yesterday = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
    sql = 'select count(*) from clean_comment where date(time) = %s'
    args = yesterday
    res = dao.exe_sql(sql, args, way=1)
    return res[0]


if __name__ == '__main__':
    print(get_yesterday_post())
    print(get_yesterday_comment())
