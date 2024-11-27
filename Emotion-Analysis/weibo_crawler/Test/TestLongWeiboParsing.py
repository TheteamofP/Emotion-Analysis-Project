#测试是否正确解析长微博的完整内容
import unittest
from scrapy.http import HtmlResponse, Request
from weibo_crawler.spiders.search import SearchSpider


class TestLongWeiboParsing(unittest.TestCase):
    def test_long_weibo(self):
        spider = SearchSpider()

        # 模拟长微博的 HTML 内容
        body = """
        <div class="card-wrap">
            <p class="txt" node-type="feed_list_content">这是长微博的内容...</p>
        </div>
        """

        # 模拟请求对象并包含 meta 信息
        request = Request(
            url="https://s.weibo.com/weibo?q=test",
            meta={'keyword': 'test'}
        )

        # 模拟响应对象
        response = HtmlResponse(
            url="https://s.weibo.com/weibo?q=test",
            body=body,
            encoding='utf-8',
            request=request
        )

        # 调用爬虫的 parse_weibo 方法
        result = list(spider.parse_weibo(response))

        # 检查是否正确解析长微博
        self.assertEqual(result[0]['text'], "这是长微博的内容...", "Long weibo parsing failed")


if __name__ == "__main__":
    unittest.main()
