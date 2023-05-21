import scrapy
import json
from tieba.items import ThreadItem, PostItem, CommentItem
from scrapy.selector import Selector


class TiebaSpider(scrapy.Spider):
    name = 'spider'
    start_urls = ['https://tieba.baidu.com/f?kw=985&ie=utf-8']
    cur_page = 1
    end_page = 999

    def parse(self, response, **kwargs):
        """
        解析帖子列表页，获取每个帖子的信息
        :param response:
        :param kwargs:
        :return:
        """
        html = response.text.replace(r'<!--', '').replace(r'-->', '')  # 返回数据都被注释，去除注释
        selector = Selector(text=html)
        thread_list = selector.xpath('//li[contains(@class, "j_thread_list")]')
        for thread in thread_list:
            data = json.loads(thread.xpath('@data-field').extract_first())
            thread_item = ThreadItem()
            thread_item['thread_id'] = data['id']
            thread_item['first_post_id'] = data['first_post_id']
            thread_item['reply_num'] = data['reply_num']
            thread_item['thread_title'] = thread.xpath(
                './/div[contains(@class, "threadlist_title")]/a/@title').extract_first()

            print(dict(thread_item))
            yield thread_item

            # 爬取该帖子所有楼层
            meta = {'thread_id': data['id'], 'post_pn': 1}  # 制作元数据，需要thread_id和页数
            url = f'https://tieba.baidu.com/p/{data["id"]}'
            yield scrapy.Request(url, callback=self.parse_post, meta=meta)  # 查询该帖子详情数据
        next_page = response.xpath('//a[@class="next pagination-item "]/@href')
        self.cur_page += 1
        if next_page:
            if self.cur_page <= self.end_page:
                yield scrapy.Request(f'https:{next_page.extract_first()}')  # 查询下一页帖子列表

    def parse_post(self, response):
        """
        解析具体的每个帖子信息
        :param response:
        :return:
        """
        meta = response.meta  # 获取元数据 帖子id 当前页数pn
        floors = response.xpath('//div[contains(@class, "l_post")]')
        for floor in floors:
            print('正在解析楼层信息')
            has_comment = False
            data = json.loads(floor.xpath('@data-field').extract_first())
            post_item = PostItem()
            post_item['post_id'] = data['content']['post_id']  # 每层的id
            post_item['thread_id'] = meta['thread_id']
            post_item['ip'] = data['content']['ip_address']  # ip归属地
            comment_num = data['content']['comment_num']  # 相当于楼中楼回复
            if comment_num > 0:
                has_comment = True  # 有楼中楼需要继续爬取数据
            post_item['comment_num'] = comment_num
            content = floor.xpath(".//div[contains(@class,'j_d_post_content')]/text()").extract_first().strip()
            post_item['content'] = content  # 内容
            post_item['time'] = data['content']['date']  # 回复时间

            yield post_item

            if has_comment:
                url = "https://tieba.baidu.com/p/comment?tid=%d&pid=%d&pn=1" % (
                    meta['thread_id'], data['content']['post_id'])
                # 爬取楼中楼
                meta['post_id'] = data['content']['post_id']  # 对应post_id
                meta['comment_pn'] = 1  # 楼中楼页数，从1开始
                yield scrapy.Request(url, callback=self.parse_comment, meta=meta)
        next_page = response.xpath(u".//ul[@class='l_posts_num']//a[text()='下一页']/@href")
        if next_page:
            meta['post_pn'] += 1
            url = response.urljoin(next_page.extract_first())
            yield scrapy.Request(url, callback=self.parse_post, meta=meta)

    def parse_comment(self, response):
        """
        解析某个帖子其余的楼中楼回复
        :param response:
        :return:
        """
        meta = response.meta
        comment_list = response.xpath('body/li')
        for i in range(len(comment_list) - 1):
            comment = comment_list[i]
            data = json.loads(comment.attrib['data-field'])
            comment_item = CommentItem()
            comment_item['comment_id'] = data['spid']
            comment_item['thread_id'] = meta['thread_id']
            comment_item['post_id'] = meta['post_id']
            comment_item['content'] = comment.css('.lzl_content_main').xpath('./text()').get().strip()
            comment_item['time'] = comment.css('.lzl_time').xpath('./text()').get()
            yield comment_item

        next_page = comment_list[-1].xpath('//p/a[text()="下一页"]')
        if next_page:
            meta['comment_pn'] += 1
            url = "https://tieba.baidu.com/p/comment?tid=%d&pid=%d&pn=%d" % (
                meta['thread_id'], meta['post_id'], meta['comment_pn'])
            yield scrapy.Request(url, callback=self.parse_comment, meta=meta)
