import unittest
import csv
import os
from classification import classifcation  # 确保从你的模块中导入classifcation函数

FILE_DIR = ('E:\\github_repositories\\Emotion-Analysis-Project'
            '\\Emotion-Analysis\\data_visualization\\test_utils\\')


class TestClassifcation(unittest.TestCase):

    def setUp(self):
        # 创建测试文件和目录
        self.file_path = FILE_DIR + 'test_predicted_results.csv'
        self.csv_files = {
            'positive': FILE_DIR + 'test_positive_words.csv',
            'negative': FILE_DIR + 'test_negative_words.csv'
        }
        for filename in self.csv_files.values():
            open(filename, 'a').close()

    def tearDown(self):
        # 删除测试文件
        for filename in self.csv_files.values():
            if os.path.exists(filename):
                os.remove(filename)
        if os.path.exists(self.file_path):
            os.remove(self.file_path)

    def test_classifcation(self):
        # 测试项：确保函数能正确分类情感文本并保存到CSV文件。
        with open('predicted_results.csv', 'w', encoding='utf-8-sig') as file:
            writer = csv.writer(file)
            # 清空文件内容
            file.truncate()
            # 写入测试数据
            writer.writerow(['sentiment_label', 'text'])
            writer.writerow(['1', '开心'])
            writer.writerow(['0', '难受'])
            writer.writerow(['0', ' '])

        classifcation()  # 运行分类函数

        # 检查正面情感文本文件
        with (open('positive_words.csv', 'r', encoding='utf-8-sig') as
              file):
            reader = csv.reader(file)
            positive_results = list(reader)
            self.assertEqual(positive_results, [['开心'], []])

        # 检查负面情感文本文件
        with (open('negative_words.csv', 'r', encoding='utf-8-sig') as
              file):
            reader = csv.reader(file)
            negative_results = list(reader)
            self.assertEqual(negative_results, [['难受'], []])


if __name__ == '__main__':
    unittest.main()
