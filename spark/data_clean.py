# -*- coding: utf-8 -*-
import findspark

findspark.init()
from pyspark import SparkConf, SparkContext
from pyspark.sql import SparkSession
import settings
import pyspark.sql.functions as F
from pyspark.sql.functions import col
import logging

# 设置logging的等级以及打印格式
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')


def remove_all_whitespace(col):
    return F.regexp_replace(col, '\\s+', '')


class JsonCleaner:
    def __init__(self):
        # spark 配置
        self._conf = SparkConf() \
            .setAppName('data-clean') \
            .setMaster(settings.SPARK_MASTER)
        self._sc = SparkContext(conf=self._conf)
        self._sc.setLogLevel('WARN')
        self._spark = SparkSession \
            .Builder() \
            .config(conf=self._conf) \
            .getOrCreate()

        # 数据库配置
        self._url = settings.MYSQL_URL
        self._prop = {
            'user': settings.USERNAME,
            'password': settings.PASSWORD,
            'driver': settings.DRIVER_CLASS
        }

        # hadoop 路径配置
        self._data_dir = settings.HDFS_URL + '/data'

    def clean_thread(self):
        """处理 json 数据"""
        logging.info('thread 清洗开始')
        threads = self._spark.read.json(self._data_dir + '/*thread*')
        result = threads \
            .dropDuplicates(subset=['thread_id']) \
            .withColumn('trim_title', remove_all_whitespace('thread_title')) \
            .filter('length(trim_title) >= 5') \
            .drop('thread_title') \
            .withColumnRenamed('trim_title', 'thread_title')
        result.write.jdbc(self._url, table='clean_thread', properties=self._prop, mode='overwrite')
        result.show(50, truncate=False)
        logging.info('thread 清洗结束')

    def clean_post(self):
        logging.info('post 清洗开始')
        posts = self._spark.read.json(self._data_dir + '/*post*')
        result = posts \
            .dropDuplicates(subset=['post_id']) \
            .filter(~posts.content.contains('<div')) \
            .filter(~posts.content.contains('<img')) \
            .withColumn('trim_content', remove_all_whitespace(col('content'))) \
            .filter('length(trim_content) >= 3') \
            .drop('content') \
            .withColumnRenamed('trim_content', 'content')
        result.write.jdbc(self._url, table='clean_post', properties=self._prop, mode='overwrite')
        result.show(50)
        logging.info('post 清洗结束')

    def clean_comment(self):
        logging.info('comment 清洗开始')
        comments = self._spark.read.json(self._data_dir + '/*comment*')
        result = comments \
            .dropDuplicates(subset=['comment_id']) \
            .filter(~comments.content.contains('<div')) \
            .filter(~comments.content.contains('<img')) \
            .withColumn('trim_content', remove_all_whitespace(col('content'))) \
            .where('length(trim_content) >= 3') \
            .drop('content') \
            .withColumnRenamed('trim_content', 'content')

        result.write.jdbc(self._url, table='clean_comment', properties=self._prop, mode='overwrite')
        result.show(50)
        logging.info('comment 清洗结束')


def main():
    cleaner = JsonCleaner()
    cleaner.clean_thread()
    cleaner.clean_post()
    cleaner.clean_comment()


if __name__ == '__main__':
    main()
