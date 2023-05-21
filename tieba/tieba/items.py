import scrapy


class ThreadItem(scrapy.Item):
    name = 'thread'
    thread_id = scrapy.Field()  # thread id 唯一标识帖子
    first_post_id = scrapy.Field()  # 帖子一楼id
    thread_title = scrapy.Field()  # 帖子标题
    reply_num = scrapy.Field()  # 回复数


class PostItem(scrapy.Item):
    name = 'post'
    post_id = scrapy.Field()  # post id 唯一标识一块
    thread_id = scrapy.Field()  # 所属thread
    content = scrapy.Field()  # 该块帖子内容
    comment_num = scrapy.Field()  # 评论数
    time = scrapy.Field()  # 回复时间
    ip = scrapy.Field()  # ip地址


class CommentItem(scrapy.Item):
    name = 'comment'
    comment_id = scrapy.Field()  # 评论id
    thread_id = scrapy.Field()  # 所属帖子
    post_id = scrapy.Field()  # 所属post
    content = scrapy.Field()  # 评论内容
    time = scrapy.Field()  # 评论时间
