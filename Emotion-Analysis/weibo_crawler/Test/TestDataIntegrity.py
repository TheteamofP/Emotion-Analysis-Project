#是否爬取包含完整字段数据
import unittest
from scrapy.http import HtmlResponse, Request
from weibo_crawler.spiders.search import SearchSpider

class TestDataIntegrity(unittest.TestCase):
    def test_data_fields(self):
        # 创建爬虫实例
        spider = SearchSpider()
        spider.settings.set('KEYWORD_LIST', ['jennie'])  # 设置测试关键词

        # 模拟一个包含微博数据的响应
        body = '''
        <div class="card-wrap">
            <a class="from" href="#">来自：test_user</a>
            <span class="created_at">2024-01-01</span>
            <p class="text">这是一个测试微博</p>
        </div>
        '''
        request = Request(url="https://s.weibo.com/weibo?q=test", meta={'keyword': 'jennie'})
        response = HtmlResponse(url="https://s.weibo.com/weibo?q=test", body=body, encoding='utf-8', request=request)

        # 调用爬虫的 parse 方法来处理响应
        result = list(spider.parse(response))

        # 检查每个结果是否包含预期的字段
        expected_keys = ["keyword", "region", "id", "user", "text", "created_at", "source"]

        for item in result:
            self.assertTrue(all(key in item for key in expected_keys), f"Data fields are missing in: {item}")

if __name__ == "__main__":
    unittest.main()
