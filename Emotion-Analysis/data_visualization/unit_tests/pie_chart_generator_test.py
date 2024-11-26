import csv
import os
import unittest
from unittest.mock import patch, mock_open
from io import StringIO
import matplotlib.pyplot as plt
from data_visualization.pie_chart_generator import pie_chart_generator


class TestPieChartGenerator(unittest.TestCase):

    def setUp(self):
        # 创建测试数据和文件
        self.test_file_path = 'predicted_results.csv'
        with open(self.test_file_path, 'w', encoding='utf-8-sig') as file:
            writer = csv.writer(file)
            writer.writerow(['sentiment_label'])
            writer.writerow(['1'])  # 正面
            writer.writerow(['0'])  # 负面

    def tearDown(self):
        # 删除测试文件
        import os
        os.remove(self.test_file_path)
        # 删除生成的饼图文件
        if os.path.exists('../static/wordclouds/pie_chart.png'):
            os.remove('../static/wordclouds/pie_chart.png')

    @patch('matplotlib.pyplot.pie')
    def test_pie_chart_generator_pie_called(self, mock_pie):
        # 测试饼图函数是否被调用
        pie_chart_generator()
        mock_pie.assert_called()

    @patch('matplotlib.pyplot.savefig')
    def test_pie_chart_generator_savefig_called(self, mock_savefig):
        # 测试保存饼图函数是否被调用
        pie_chart_generator()
        mock_savefig.assert_called()


if __name__ == '__main__':
    unittest.main()