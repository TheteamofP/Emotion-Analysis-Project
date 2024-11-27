#测试是否在起止日期设置错误时程序正常退出
from twisted.trial import unittest
from weibo_crawler.spiders.search import SearchSpider

class TestDateValidation(unittest.TestCase):
    def test_date_boundary(self):
        spider = SearchSpider()
        spider.settings.set('START_DATE', '2024-01-02')
        spider.settings.set('END_DATE', '2024-01-01')
        # 捕获 SystemExit 异常
        with self.assertRaises(SystemExit):
            list(spider.start_requests())

if __name__ == "__main__":
    unittest.main()
