#测试按小时细分逻辑是否正确实现
import unittest
from scrapy.http import HtmlResponse, Request
from weibo_crawler.spiders.search import SearchSpider


class TestPagination(unittest.TestCase):
    def test_pagination_handling(self):
        spider = SearchSpider()
        # 设置爬虫配置
        spider.settings.set('KEYWORD_LIST', ['test'])
        spider.settings.set('START_DATE', '2024-01-01')
        spider.settings.set('END_DATE', '2024-01-02')

        # 模拟一个包含分页链接的响应对象
        body = '<a class="next" href="/page/2">下一页</a>'
        request = Request(
            url="https://s.weibo.com/weibo?q=test",
            meta={'keyword': 'test'}
        )
        response = HtmlResponse(
            url="https://s.weibo.com/weibo?q=test",
            body=body,
            encoding='utf-8',
            request=request
        )

        # 调用 parse 方法
        requests = list(spider.parse(response))

        # 预期的分页 URL
        expected_url = "https://s.weibo.com/page/2"

        # 验证是否正确生成了分页的请求
        self.assertTrue(
            any(request.url == expected_url for request in requests),
            "Pagination failed: next page URL not found"
        )


if __name__ == "__main__":
    unittest.main()
