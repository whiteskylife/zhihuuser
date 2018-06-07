# -*- coding: utf-8 -*-
import scrapy
from scrapy import Spider, Request
from zhihuuser.items import UserItem
import json


class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['https://www.zhihu.com/']

    start_user = 'excited-vczh'

    user_url = 'https://www.zhihu.com/api/v4/members/{user}?include={include}'
    user_query = 'allow_message,is_followed,is_following,is_org,is_blocking,employments,answer_count,follower_count,articles_count,gender,badge[?(type=best_answerer)].topics'

    followees_url = 'https://www.zhihu.com/api/v4/members/{user}/followees?include={include}&offset={offset}&limit={limit}'
    follows_query = 'data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics'

    followers_url = 'https://www.zhihu.com/api/v4/members/{user}/followers?include={include}&offset={offset}&limit={limit}'

    def start_requests(self):
        # 请求用户url
        yield Request(url=self.user_url.format(user=self.start_user, include=self.user_query), callback=self.parse_user)

        # 请求关注列表url
        yield Request(
            url=self.followees_url.format(user=self.start_user, include=self.follows_query, offset=0, limit=20),
            callback=self.parse_follows)

        # 请求粉丝列表url
        yield Request(
            url=self.followers_url.format(user=self.start_user, include=self.follows_query, offset=0, limit=20),
            callback=self.parse_follows         # 粉丝列表回调函数暂且使用parse_follows
        )


    def parse_user(self, response):
        """
            分析用户信息，入库
            根据用户关注列表获取token，生成关注列表请求url
            根据用户粉丝列表获取token，生成粉丝列表请求url
        """
        result = json.loads(response.text)
        item = UserItem()

        # if result.get('employments'):
        #     item['company_name'] = result.get('employments')[0].get('company').get('name')
        #     item['company_excerpt'] = result.get('employments')[0].get('company').get('excerpt')
        #     item['company_introduction'] = result.get('employments')[0].get('company').get('introduction')
        #
        #     item['job_excerpt'] = result.get('employments')[0].get('job').get('excerpt')
        #     item['job_introduction'] = result.get('employments')[0].get('job').get('introduction')
        #     item['job_name'] = result.get('employments')[0].get('job').get('name')

        for field in item.fields:
            if field in result.keys():
                item[field] = result.get(field)
        yield item
        # 请求关注列表
        yield Request(
            url=self.followees_url.format(user=result.get('url_token'), include=self.follows_query, limit=20, offset=0),
            callback=self.parse_follows
            )
        # 请求粉丝列表
        yield Request(
            url=self.followers_url.format(user=result.get('url_token'), include=self.follows_query, limit=20, offset=0),
            callback=self.parse_follows
            )

    def parse_follows(self, response):
        """解析关注列表、粉丝列表，获取url_token，根据url_token爬取新的用户信息"""
        results = json.loads(response.text)
        if 'data' in results.keys():
            for result in results.get('data'):
                yield Request(url=self.user_url.format(user=result.get('url_token'), include=self.user_query),
                              callback=self.parse_user
                              )
        # 翻页：
        if 'paging' in results.keys() and results.get('paging').get('is_end') == False:
            next_page = results.get('paging').get('next')
            yield Request(url=next_page, callback=self.parse_follows)
