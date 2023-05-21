from snownlp import SnowNLP


def get_emotion_snownlp(data):
    """
    使用snownlp库，基于贝叶斯算法，数据来自商店评论，处理其他语料时泛化程度不足，准确率偏低
    :param data: 需要进行分析的string文本
    :return: 0~1，返回值越高表明文本积极性越高，反之消极性更高，据此可以将文本分为积极、消极或中立
    """
    return SnowNLP(data).sentiments


if __name__ == '__main__':
    txt1 = "这是我遇见的最棒的一家店，种类多，价格低，更喜欢的是服务质量很好"
    txt2 = "我不是很喜欢"
    print("txt1测试结果：", get_emotion_snownlp(txt1))
    print("txt2测试结果：", get_emotion_snownlp(txt2))
