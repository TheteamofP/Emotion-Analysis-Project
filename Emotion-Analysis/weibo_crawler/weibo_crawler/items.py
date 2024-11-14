# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WeiboItem(scrapy.Item):
    import scrapy

    class WeiboItem(scrapy.Item):
        id = scrapy.Field()  # 微博 ID
        bid = scrapy.Field()  # 帖子 ID
        user_id = scrapy.Field()  # 用户 ID
        screen_name = scrapy.Field()  # 用户昵称
        text = scrapy.Field()  # 微博正文内容
        article_url = scrapy.Field()  # 头条文章链接
        location = scrapy.Field()  # 发布位置
        at_users = scrapy.Field()  # @ 用户
        topics = scrapy.Field()  # 话题
        reposts_count = scrapy.Field()  # 转发数
        comments_count = scrapy.Field()  # 评论数
        attitudes_count = scrapy.Field()  # 点赞数
        created_at = scrapy.Field()  # 发布时间
        source = scrapy.Field()  # 发布工具
        pics = scrapy.Field()  # 图片 URL 列表
        video_url = scrapy.Field()  # 视频 URL
        retweet_id = scrapy.Field()  # 转发的微博 ID

