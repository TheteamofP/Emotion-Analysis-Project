import csv
import unittest
from unittest.mock import patch, mock_open
from PIL import Image
import os
from io import BytesIO

# 被测试模块
from data_visualization.wordcloud_generator import (
    load_text_data,
    generate_wordcloud,
    save_wordcloud,
    beautify_images,
    wordcloud_generator,
    wordclouds_generator
)


class TestWordCloudModule(unittest.TestCase):

    def setUp(self):
        # 创建测试数据文件
        self.test_data_path = 'test_data.csv'
        with open(self.test_data_path, 'w', encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            writer.writerow(['这是对词云生成功能的测试用例'])

        self.test_font_path = 'simkai.ttf'
        self.test_mask = None
        self.test_image_color = None

    def tearDown(self):
        # 删除测试数据文件
        os.remove(self.test_data_path)

    def test_load_text_data(self):
        # 测试是否正确读取文件内容
        result = load_text_data(self.test_data_path)
        self.assertEqual(result, '这是对词云生成功能的测试用例')

    @patch('builtins.open', side_effect=FileNotFoundError)
    def test_load_text_data_file_not_found(self, mock_open):
        # 测试文件不存在时的行为
        result = load_text_data('non_existent_file.txt')
        self.assertIsNone(result)

    def test_generate_wordcloud(self):
        text = '你好测试'
        wc = generate_wordcloud(text, self.test_font_path, self.test_mask, self.test_image_color)
        self.assertIsNotNone(wc)

    def test_save_wordcloud(self):
        wc = generate_wordcloud('你好测试', self.test_font_path, self.test_mask, self.test_image_color)
        save_wordcloud(wc, 'test_wordcloud', 300)
        self.assertTrue(os.path.exists('test_wordcloud.png'))

    def test_beautify_images(self):
        wc = generate_wordcloud('你好测试', self.test_font_path, self.test_mask, self.test_image_color)
        save_wordcloud(wc, 'test_wordcloud', 300)
        beautify_images('test_wordcloud')
        self.assertTrue(os.path.exists('test_wordcloud.png'))


if __name__ == '__main__':
    unittest.main()
