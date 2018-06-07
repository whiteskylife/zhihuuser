# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field

class UserItem(scrapy.Item):
    # define the fields for your item here like:
    id = Field()
    name = Field()
    avatar_url = Field()
    headline = Field()
    url_token = Field()
    gender = Field()
    type = Field()
    user_type = Field()
    badge = Field()

    answer_count = Field()
    articles_count = Field()
    follower_count = Field()

    employments = Field()
    # company_name = Field()
    # company_excerpt = Field()
    # company_introduction = Field()
    #
    # job_excerpt = Field()
    # job_introduction = Field()
    # job_name = Field()