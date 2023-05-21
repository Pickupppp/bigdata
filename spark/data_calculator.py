# -*- coding: utf-8 -*-
import logging

import findspark

findspark.init()

from pyspark import SparkConf, SparkContext
from pyspark.sql import SparkSession
import settings
import jieba

# 设置logging的等级以及打印格式
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')


class Calculator:

    def __init__(self):
        # spark 配置
        self._conf = SparkConf() \
            .setAppName('data-calculator') \
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
        self._hdfs = settings.HDFS_URL + '/result'

    def ip_count(self):
        """ 统计ip """
        logging.info('统计 post ip 开始')
        post_df = self._spark.read.jdbc(url=self._url, properties=self._prop, table='clean_post')
        post_df = post_df.groupBy('ip').count()
        post_df = post_df.withColumnRenamed('ip', 'name').withColumnRenamed('count', 'value')
        post_df.show()
        post_df.write.json(self._hdfs + '/post_ip.json', mode='overwrite')
        logging.info('统计 post ip 结束')

    def wordcount(self):
        # 中文分词 去除停用词 这里使用到了集合运算
        def get_word(line):
            return set(jieba.cut(line, cut_all=False)) - stop_words

        # 最终结果为 (word, num) 格式,需要根据num排序
        def sort_result(elem):
            return elem[1]

        # 处理词云
        def generate(dataframe, pos):
            word_list = dataframe.rdd \
                .flatMap(lambda x: get_word(x[pos])) \
                .map(lambda word: (word, 1)) \
                .reduceByKey(lambda x, y: x + y).collect()
            word_list.sort(key=sort_result, reverse=True)
            word_df = self._spark.createDataFrame(word_list, ['word', 'num'])
            return word_df

        # 加载停动词词库
        stop_word_rdd = self._sc.textFile(self._hdfs + '/cn_stopwords.txt')
        stop_words = set(stop_word_rdd.collect())
        logging.info('加载停用词结束')

        # 加载 thread
        thread_df = self._spark.read.jdbc(url=self._url, properties=self._prop, table='clean_thread')
        thread_title_word_df = generate(thread_df, 3)
        thread_title_word_df = thread_title_word_df.withColumnRenamed('word', 'name').withColumnRenamed('num', 'value')
        thread_title_word_df.show()
        thread_title_word_df.write.json(self._hdfs + '/thread_wordcount.json', mode='overwrite')
        logging.info('生成 thread wordcount 结束')

        # 加载 comment
        comment_df = self._spark.read.jdbc(url=self._url, properties=self._prop, table='clean_comment')
        comment_word_df = generate(comment_df, 4)
        comment_word_df = comment_word_df.withColumnRenamed('word', 'name').withColumnRenamed('num', 'value')
        comment_word_df.show()
        comment_word_df.write.json(self._hdfs + '/comment_wordcount.json', mode='overwrite')
        logging.info('生成 comment wordcount 结束')

        # 加载 post
        post_df = self._spark.read.jdbc(url=self._url, properties=self._prop, table='clean_post')
        post_word_df = generate(post_df, 5)
        post_word_df = post_word_df.withColumnRenamed('word', 'name').withColumnRenamed('num', 'value')
        post_word_df.show()
        post_word_df.write.json(self._hdfs + '/post_wordcount.json', mode='overwrite')
        logging.info('生成 post wordcount 结束')


def main():
    calculator = Calculator()
    calculator.ip_count()
    calculator.wordcount()


if __name__ == '__main__':
    main()
