import os
import unittest
from unittest.mock import patch, mock_open  # unittest.mock用于编写和运行测试用例
from data_visualization.wordcloud_generator import (load_text_data,
                                                    generate_wordcloud,
                                                    save_wordcloud,
                                                    beautify_images)


class TestWordCloudModule(unittest.TestCase):

    # 设置测试环境
    def setUp(self):
        # 设置测试数据文件和停用词文件的路径
        self.test_data_path = 'test_data.csv'
        self.test_stopwords_path = 'test_stopwords.txt'
        # 创建测试数据文件和停用词文件
        with open(self.test_data_path, 'w', encoding='utf-8-sig') as f:
            f.write('这是对词云生成功能的测试用例')
        with open(self.test_stopwords_path, 'w', encoding='utf-8-sig') as f:
            f.write('测试\n文本')

    # 清理测试环境
    def tearDown(self):
        # 删除测试数据文件和停用词文件
        os.remove(self.test_data_path)
        os.remove(self.test_stopwords_path)

    # 测试load_text_data函数是否正确读取文件内容
    def test_load_text_data(self):
        # 模拟文件打开操作
        with patch('builtins.open', mock_open(read_data='这是对词云生成功能'
                                                        '的测试用例')):
            result = load_text_data('test_data.txt')
            self.assertEqual(result, '这是对词云生成功能的测试用例')

    # 测试load_text_data函数在文件不存在时的行为
    def test_load_text_data_file_not_found(self):
        # 模拟文件打开时抛出FileNotFoundError异常
        with patch('builtins.open', side_effect=FileNotFoundError):
            result = load_text_data('non_existent_file.txt')
            self.assertIsNone(result)

    # 测试generate_wordcloud函数是否正确生成词云对象
    def test_generate_wordcloud(self):
        text = '你好测试'
        font_path = 'simkai.ttf'
        mask = None
        image_color = None
        wc = generate_wordcloud(text, font_path, mask, image_color)
        self.assertIsNotNone(wc)

    # 测试save_wordcloud函数是否正确保存词云图像
    def test_save_wordcloud(self):
        # 测试保存词云图函数
        wc = generate_wordcloud('你好测试', 'simkai.ttf',
                                None,None)
        save_wordcloud(wc, 'test_wordcloud', 300,
                       '')
        self.assertTrue(os.path.exists('test_wordcloud.png'))

    # 测试beautify_images函数是否正确保存美化的词云图像
    def test_beautify_images(self):
        wc = generate_wordcloud('你好测试', 'simkai.ttf',
                                None,None)
        save_wordcloud(wc, 'test_wordcloud', 300,
                       '')
        beautify_images('test_wordcloud', '')
        self.assertTrue(os.path.exists('test_wordcloud.png'))


if __name__ == '__main__':
    unittest.main()
