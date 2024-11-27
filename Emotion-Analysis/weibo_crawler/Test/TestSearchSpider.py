#测试是否生成符合预期的URL
import unittest
from datetime import datetime, timedelta

from weibo_crawler.spiders.search import SearchSpider

class TestSearchSpider(unittest.TestCase):
    def test_url_construction(self):
        # 初始化爬虫对象
        spider = SearchSpider()
        spider.settings.set('KEYWORD_LIST', ['jennie', 'blackpink', 'kimjenni'])
        spider.settings.set('START_DATE', '2024-01-01')
        spider.settings.set('END_DATE', '2024-05-21')
        spider.regions = ['广东']  # 动态传入的 region 值

        # 动态生成预期的 URL 列表
        region_dict = {
            '广东': 'custom:44:10000',  # 假设 region_dict 中的映射
        }
        start_date = '2024-01-01'
        end_date = '2024-05-21'
        adjusted_end_date = (datetime.strptime(end_date, '%Y-%m-%d') + timedelta(days=1)).strftime('%Y-%m-%d')
        expected_urls = [
             f"https://s.weibo.com/weibo?q={keyword}&region={region_dict['广东']}&timescope=custom:{start_date}:{adjusted_end_date}"
            for keyword in ['jennie', 'blackpink', 'kimjenni']
        ]

        # 调用 start_requests 方法获取生成的请求
        requests = list(spider.start_requests())

        # 遍历预期的 URL，验证是否生成
        for expected_url in expected_urls:
            self.assertTrue(
                any(request.url == expected_url for request in requests),
                f"Expected URL not found: {expected_url}"
            )

if __name__ == '__main__':
    unittest.main()
