# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WeiboItem(scrapy.Item):
    import scrapy

    class WeiboItem(scrapy.Item):
        keyword = scrapy.Field()
        id = scrapy.Field()  # 微博 ID
        bid = scrapy.Field()  # 帖子 ID
        user_id = scrapy.Field()  # 用户 ID
        screen_name = scrapy.Field()  # 用户昵称
        text = scrapy.Field()  # 微博正文内容
        location = scrapy.Field()  # 发布位置
        created_at = scrapy.Field()  # 发布时间
        source = scrapy.Field()  # 发布工具
        retweet_id = scrapy.Field()  # 转发的微博 ID

