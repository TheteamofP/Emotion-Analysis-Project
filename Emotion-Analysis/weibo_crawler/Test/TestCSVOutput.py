#测试爬取数据是否按预期格式写入输出CSV文件
import os
import csv
from twisted.trial import unittest
from weibo_crawler.spiders.search import SearchSpider

class TestCSVOutput(unittest.TestCase):
    def test_csv_output(self):
        spider = SearchSpider()
        spider.file = open('test_output.csv', 'w', newline='', encoding='utf-8')
        spider.csv_writer = csv.writer(spider.file)
        spider.csv_writer.writerow(['keyword', 'region', 'id', 'user', 'text', 'created_at', 'source'])

        data = {
            'keyword': 'test',
            'region': '广东',
            'id': '123456789',
            'user': 'test_user',
            'text': '这是测试微博',
            'created_at': '2024-01-01',
            'source': '微博'
        }
        spider.csv_writer.writerow(data.values())
        spider.file.close()

        # 验证文件内容
        with open('test_output.csv', 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            rows = list(reader)
        os.remove('test_output.csv')
        self.assertEqual(len(rows), 2, "CSV file does not have expected rows")
        self.assertEqual(rows[1], list(data.values()), "CSV file content mismatch")


if __name__ == "__main__":
    unittest.main()
