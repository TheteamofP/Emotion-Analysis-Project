import unittest
from weibo_crawler.spiders.search import SearchSpider

class TestRegionParsing(unittest.TestCase):
    def test_region_url(self):
        spider = SearchSpider()
        # 设置爬虫的配置
        spider.settings.set('KEYWORD_LIST', ['jennie', 'blackpink', 'kimjenni'])
        spider.settings.set('START_DATE', '2024-01-01')
        spider.settings.set('END_DATE', '2024-01-03')
        spider.regions = ['广东']

        # 模拟的地区映射
        region_dict = {
            '广东': {'code': '44'}
        }

        # 生成的请求
        requests = list(spider.start_requests())

        # 动态生成预期 URL
        start_date = '2024-01-01'
        end_date = '2024-01-04'
        expected_urls = [
            f"https://s.weibo.com/weibo?q={keyword}&region=custom:{region_dict['广东']['code']}:10000&timescope=custom:{start_date}:{end_date}"
            for keyword in ['jennie', 'blackpink', 'kimjenni']
        ]

        # 检查生成的每个 URL 是否在预期范围内
        for expected_url in expected_urls:
            self.assertTrue(
                any(request.url == expected_url for request in requests),
                f"Region URL generation failed for URL: {expected_url}"
            )

if __name__ == "__main__":
    unittest.main()
