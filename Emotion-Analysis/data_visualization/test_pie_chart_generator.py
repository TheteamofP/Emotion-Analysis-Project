import unittest
import csv
import os
from pie_chart_generator import pie_chart_generator


class TestPieChartGenerator(unittest.TestCase):

    def setUp(self):
        # 创建测试文件和目录
        with open('predicted_results.csv', 'w', encoding='utf-8-sig') as file:
            writer = csv.writer(file)
            writer.writerow(['sentiment_label'])
            writer.writerow(['1'])  # 正面情感
            writer.writerow(['0'])  # 负面情感

    def tearDown(self):
        # 清理生成的图像和CSV文件
        pie_chart_path = ("E:\\github_repositories\\Emotion-Analysis-Project"
                          "\\Emotion-Analysis\\static\\wordclouds"
                          "\\pie_chart.png")
        csv_output_path = ("'E:\\github_repositories\\Emotion-Analysis-Project"
                           "\\Emotion-Analysis\\data_visualization"
                           "\\sentiment_percentages.csv")
        if os.path.exists(pie_chart_path):
            os.remove(pie_chart_path)
        if os.path.exists(csv_output_path):
            os.remove(csv_output_path)

    def test_pie_chart_generator(self):
        # 调用函数
        pie_chart_generator()

        # 检查饼图是否生成
        pie_chart_path = ("E:\\github_repositories\\Emotion-Analysis-Project"
                          "\\Emotion-Analysis\\static\\wordclouds"
                          "\\pie_chart.png")
        self.assertTrue(os.path.exists(pie_chart_path))

        # 检查百分比数据是否保存到CSV文件
        csv_output_path = ("E:\\github_repositories\\Emotion-Analysis-Project"
                           "\\Emotion-Analysis\\data_visualization"
                           "\\sentiment_percentages.csv")
        self.assertTrue(os.path.exists(csv_output_path))
        with open(csv_output_path, 'r', encoding='utf-8-sig') as csvfile:
            reader = csv.reader(csvfile)
            data = list(reader)
            self.assertEqual(data[0], ['Sentiment', 'Percentage'])
            self.assertEqual(data[1][0], '正面')
            self.assertEqual(data[2][0], '负面')


if __name__ == '__main__':
    unittest.main()
